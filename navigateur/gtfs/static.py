"""Lecture GTFS statique, sans altérer les anciennes données du projet.

Les durées GTFS sont des secondes depuis minuit du *jour de service*.
Un horaire 25:15:00 appartient donc au service du jour précédent.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

TIMEZONE = "Europe/Paris"


def gtfs_seconds(value: str) -> int:
    parts = value.split(":")
    if len(parts) != 3 or not all(p.isdecimal() for p in parts):
        raise ValueError(f"Heure GTFS invalide : {value!r}")
    h, m, s = map(int, parts)
    if not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError(f"Heure GTFS invalide : {value!r}")
    return h * 3600 + m * 60 + s


def rows(archive: ZipFile, name: str):
    """Itère sur un CSV GTFS en streaming ; mémoire proportionnelle à une ligne."""
    import io
    with archive.open(name) as source, io.TextIOWrapper(source, encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def service_active(day: date, calendar: dict, exceptions: dict) -> bool:
    """Exécute les règles calendar.txt et calendar_dates.txt (ajout/retrait)."""
    key = day.strftime("%Y%m%d")
    if key in exceptions:
        return exceptions[key] == 1
    if not calendar:
        return False
    if not calendar["start_date"] <= key <= calendar["end_date"]:
        return False
    return calendar[day.strftime("%A").lower()] == "1"


@dataclass(frozen=True)
class StopTime:
    trip_id: str
    stop_id: str
    sequence: int
    arrival: int
    departure: int


@dataclass(frozen=True)
class Connection:
    trip_id: str
    service_id: str
    route_id: str
    origin: str
    destination: str
    departure: int
    arrival: int

    @property
    def seconds(self) -> int:
        return self.arrival - self.departure


def connections_for_trip(stop_times: list[StopTime], *, trip_id: str, route_id: str, service_id: str):
    """Arcs temporels orientés entre arrêts consécutifs, sans écraser les branches."""
    ordered = sorted(stop_times, key=lambda stop: stop.sequence)
    for previous, following in zip(ordered, ordered[1:]):
        if following.arrival < previous.departure:
            raise ValueError(f"Horaires incohérents pour {trip_id}")
        yield Connection(
            trip_id=trip_id, service_id=service_id, route_id=route_id,
            origin=previous.stop_id, destination=following.stop_id,
            departure=previous.departure, arrival=following.arrival,
        )


def _date(value: str) -> date:
    return datetime.strptime(value, "%Y%m%d").date()


class GTFSArchive:
    """Index jour/service des GTFS officiels. Pas de téléchargement implicite."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _read_optional(self, zf: ZipFile, name: str):
        if name not in zf.namelist():
            return []
        return list(rows(zf, name))

    def connections_on(self, day: date) -> list[Connection]:
        """Retourne les départs dont le jour de service est day.

        Attention : certains départs >24h se produisent physiquement le lendemain.
        Pour une recherche exacte autour de minuit, indexer aussi le service J-1.
        """
        with ZipFile(self.path) as zf:
            calendars = {r["service_id"]: r for r in self._read_optional(zf, "calendar.txt")}
            overrides: dict[str, dict[str, int]] = {}
            for r in self._read_optional(zf, "calendar_dates.txt"):
                overrides.setdefault(r["service_id"], {})[r["date"]] = int(r["exception_type"])

            active_services = {
                service for service in calendars.keys() | overrides.keys()
                if service_active(day, calendars.get(service, {}), overrides.get(service, {}))
            }
            trips = {
                r["trip_id"]: (r["route_id"], r["service_id"])
                for r in rows(zf, "trips.txt")
                if r["service_id"] in active_services
            }
            times: dict[str, list[StopTime]] = {}
            for row in rows(zf, "stop_times.txt"):
                tid = row["trip_id"]
                if tid not in trips:
                    continue
                times.setdefault(tid, []).append(StopTime(
                    trip_id=tid, stop_id=row["stop_id"],
                    sequence=int(row["stop_sequence"]),
                    arrival=gtfs_seconds(row["arrival_time"]),
                    departure=gtfs_seconds(row["departure_time"]),
                ))
            output = []
            for tid, stops in times.items():
                route, service = trips[tid]
                output.extend(connections_for_trip(stops, trip_id=tid, route_id=route, service_id=service))
            return output


def download_gtfs(destination: str | Path, *, url: str, max_bytes: int = 150_000_000):
    """Télécharge une archive via TLS avec limite de taille et remplacement atomique."""
    import os
    import tempfile
    import urllib.request

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not url.startswith("https://"):
        raise ValueError("Une URL HTTPS est requise")
    fd, temporary = tempfile.mkstemp(prefix=".gtfs-", suffix=".zip", dir=destination.parent)
    try:
        with os.fdopen(fd, "wb") as output, urllib.request.urlopen(url, timeout=60) as response:
            total = 0
            while chunk := response.read(64 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("Archive GTFS trop volumineuse")
                output.write(chunk)
        with ZipFile(temporary) as archive:
            required = {"trips.txt", "stop_times.txt", "stops.txt"}
            if not required.issubset(archive.namelist()):
                raise ValueError("Archive GTFS incomplète")
            if not {"calendar.txt", "calendar_dates.txt"} & set(archive.namelist()):
                raise ValueError("Calendrier GTFS manquant")
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
