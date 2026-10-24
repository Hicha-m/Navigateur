"""Adaptateur GTFS-RT SNCF : retards/annulations, sans modification des horaires source.

Dépendance optionnelle : pip install gtfs-realtime-bindings.
Ne jamais rapprocher un numéro commercial et un trip_id sans mapping vérifié.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TripUpdate:
    trip_id: str
    start_date: str | None
    schedule_relationship: int | None
    delays: dict[int, int]
    timestamp: int | None


def parse_trip_updates(feed: Any) -> dict[tuple[str, str | None], TripUpdate]:
    """Parse un FeedMessage protobuf ou une structure compatible.

    Les retards proviennent de StopTimeUpdate.arrival/delay ou departure/delay.
    L'index reste (trip_id, start_date) ; pas de rapprochement commercial implicite.
    """
    updates = {}
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue
        item = entity.trip_update
        trip = item.trip
        tid = trip.trip_id
        if not tid:
            continue
        start_date = trip.start_date or None
        delays = {}
        for st in item.stop_time_update:
            delay = None
            if st.HasField("arrival") and st.arrival.HasField("delay"):
                delay = st.arrival.delay
            elif st.HasField("departure") and st.departure.HasField("delay"):
                delay = st.departure.delay
            if delay is not None and st.stop_sequence:
                delays[st.stop_sequence] = int(delay)
        update = TripUpdate(
            trip_id=tid,
            start_date=start_date,
            schedule_relationship=int(trip.schedule_relationship)
            if trip.HasField("schedule_relationship") else None,
            delays=delays,
            timestamp=int(item.timestamp) if item.timestamp else None,
        )
        updates[(tid, start_date)] = update
    return updates


def fetch_trip_updates(url: str, *, timeout: int = 15, max_bytes: int = 15_000_000):
    """Lit un flux GTFS-RT protobuf ; limite les données et le temps réseau."""
    import urllib.request

    if not url.startswith("https://"):
        raise ValueError("L'URL doit être HTTPS")
    try:
        from google.transit import gtfs_realtime_pb2
    except ImportError as exc:
        raise RuntimeError("Installer l'option gtfs-realtime-bindings") from exc
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = response.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise ValueError("Flux GTFS-RT trop volumineux")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(payload)
    return feed


def feed_fresh(feed: Any, *, now: datetime | None = None, max_age_seconds: int = 300) -> bool:
    """Évite d'appliquer silencieusement un flux obsolète ou horodaté dans le futur."""
    now = now or datetime.now(timezone.utc)
    timestamp = int(feed.header.timestamp) if feed.header.timestamp else 0
    age = int(now.timestamp()) - timestamp
    return timestamp > 0 and -60 <= age <= max_age_seconds


def apply_delay(connections: list, updates: dict, service_day: str, *, require_exact_trip_id: bool = True):
    """Projection simple des retards d'une course sur les arcs du jour de service.

    À ce stade, si les identifiants ne correspondent pas exactement, l'arc
    théorique reste inchangé. Les annulations ne sont pas extrapolées.
    """
    from dataclasses import replace

    result = []
    for edge in connections:
        update = updates.get((edge.trip_id, service_day))
        if update is None and not require_exact_trip_id:
            update = updates.get((edge.trip_id, None))
        if update is None:
            result.append(edge)
            continue
        # GTFS-RT : CANCELED=3 dans les TripDescriptor connus par le standard.
        if update.schedule_relationship == 3:
            continue
        # Une correspondance précise stop_sequence <-> connection est
        # nécessaire pour appliquer les retards par arrêt sans ambiguïté.
        # Ne jamais appliquer indistinctement le retard d'une gare à tout un trajet.
        result.append(edge)
    return result
