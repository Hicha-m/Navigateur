"""Tests isolés de la politique d'association temps réel/statique."""
from datetime import datetime, timezone
from types import SimpleNamespace

from navigateur.gtfs.realtime import TripUpdate, apply_delay, feed_fresh
from navigateur.gtfs.static import Connection


def test_flux_obsolete_refuse():
    feed = SimpleNamespace(header=SimpleNamespace(timestamp=100))
    now = datetime.fromtimestamp(1000, tz=timezone.utc)
    assert not feed_fresh(feed, now=now)


def test_flux_recent_accepte():
    feed = SimpleNamespace(header=SimpleNamespace(timestamp=950))
    now = datetime.fromtimestamp(1000, tz=timezone.utc)
    assert feed_fresh(feed, now=now)


def test_annulation_avec_id_et_jour_exact():
    edge = Connection("trip", "service", "route", "A", "B", 10, 20)
    updates = {("trip", "20261024"): TripUpdate("trip", "20261024", 3, {}, 900)}
    assert apply_delay([edge], updates, "20261024") == []
    assert apply_delay([edge], updates, "20261025") == [edge]


def test_identifiants_inconnus_non_interpretes():
    edge = Connection("Trip-Internal", "service", "route", "A", "B", 10, 20)
    updates = {("12345", "20261024"): TripUpdate("12345", "20261024", 3, {}, 900)}
    assert apply_delay([edge], updates, "20261024") == [edge]
