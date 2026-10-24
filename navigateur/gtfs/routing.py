"""Recherche d'arrivée au plus tôt sur connexions GTFS datées.

Hypothèses explicites : une correspondance entre deux trip_id requiert
minimum_transfer_seconds ; continuer à bord du même train ne le requiert pas.
Les courses sont identifiées par (jour de service, trip_id).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from navigateur.gtfs.static import Connection, GTFSArchive

PARIS = ZoneInfo("Europe/Paris")


@dataclass(frozen=True)
class Leg:
    trip_id: str
    service_day: date
    origin: str
    destination: str
    departure: datetime
    arrival: datetime


@dataclass(frozen=True)
class Journey:
    legs: tuple[Leg, ...]
    departure: datetime
    arrival: datetime

    @property
    def duration_seconds(self) -> int:
        return int((self.arrival - self.departure).total_seconds())


def _absolute(service_day: date, seconds: int) -> datetime:
    """Convertit un temps GTFS en instant daté, y compris 24:xx / 25:xx."""
    wall = datetime.combine(service_day, time.min) + timedelta(seconds=seconds)
    return wall.replace(tzinfo=PARIS)


def dated_connections(archive: GTFSArchive, days: list[date]) -> list[Leg]:
    output = []
    for day in days:
        for edge in archive.connections_on(day):
            departure = _absolute(day, edge.departure)
            arrival = _absolute(day, edge.arrival)
            if arrival < departure:
                raise ValueError("Arrivée avant départ dans GTFS")
            output.append(Leg(edge.trip_id, day, edge.origin, edge.destination, departure, arrival))
    return sorted(output, key=lambda leg: leg.departure)


def earliest_arrival(
    legs: list[Leg], origin: str, destination: str, not_before: datetime,
    *, minimum_transfer_seconds: int = 300,
) -> Journey | None:
    """Balayage temporel de connexions (CSA), avec état par dernière course.

    Les états restent séparés par (stop_id, course) pour ne pas confondre
    changement de train et continuation à bord ; la sélection finale minimise
    l'heure d'arrivée. Cette implémentation ne traite pas les trajets à pied.
    """
    if not_before.tzinfo is None:
        raise ValueError("not_before doit être timezone-aware")
    if minimum_transfer_seconds < 0:
        raise ValueError("Le temps de correspondance ne peut pas être négatif")
    if origin == destination:
        return Journey((), not_before, not_before)

    # (stop, course) -> (instant d'arrivée, chemin). Course None au départ.
    states: dict[tuple[str, tuple[date, str] | None], tuple[datetime, tuple[Leg, ...]]] = {
        (origin, None): (not_before, ())
    }
    target: tuple[datetime, tuple[Leg, ...]] | None = None
    for leg in sorted(legs, key=lambda item: item.departure):
        if leg.departure < not_before:
            continue
        course = (leg.service_day, leg.trip_id)
        candidate: tuple[datetime, tuple[Leg, ...]] | None = None
        for (stop, previous_course), (available, path) in tuple(states.items()):
            if stop != leg.origin:
                continue
            required = 0 if previous_course is None or previous_course == course else minimum_transfer_seconds
            if available + timedelta(seconds=required) > leg.departure:
                continue
            if candidate is None or available < candidate[0]:
                candidate = (available, path)
        if candidate is None:
            continue
        next_path = candidate[1] + (leg,)
        key = (leg.destination, course)
        previous = states.get(key)
        if previous is None or leg.arrival < previous[0]:
            states[key] = (leg.arrival, next_path)
        if leg.destination == destination and (target is None or leg.arrival < target[0]):
            target = (leg.arrival, next_path)
    if target is None:
        return None
    path = target[1]
    return Journey(path, path[0].departure, target[0])


def search_archive(
    archive: GTFSArchive, origin: str, destination: str, depart_after: datetime,
    *, minimum_transfer_seconds: int = 300,
) -> Journey | None:
    """Inclut J-1 pour les services après 24h et J/J+1 pour passages de nuit."""
    if depart_after.tzinfo is None:
        raise ValueError("Date de départ timezone-aware obligatoire")
    day = depart_after.astimezone(PARIS).date()
    days = [day - timedelta(days=1), day, day + timedelta(days=1)]
    return earliest_arrival(
        dated_connections(archive, days), origin, destination, depart_after,
        minimum_transfer_seconds=minimum_transfer_seconds,
    )
