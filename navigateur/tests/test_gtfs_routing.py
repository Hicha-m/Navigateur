"""Non-régressions sur horaires, changement de train et minuit."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from navigateur.gtfs.routing import Leg, earliest_arrival, search_archive

TZ = ZoneInfo("Europe/Paris")
DAY = date(2026, 10, 23)


def dt(hour, minute=0, *, day=DAY):
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=TZ)


def leg(train, start, end, departure, arrival, *, service_day=DAY):
    return Leg(train, service_day, start, end, departure, arrival)


def test_wait_for_departure_and_take_earliest_arrival():
    edges = [
        leg("slow", "A", "B", dt(10), dt(12)),
        leg("fast", "A", "B", dt(11), dt(11, 30)),
    ]
    got = earliest_arrival(edges, "A", "B", dt(9))
    assert got.arrival == dt(11, 30)
    assert got.legs[0].trip_id == "fast"


def test_transfer_must_meet_minimum_time():
    edges = [
        leg("T1", "A", "B", dt(10), dt(10, 30)),
        leg("T2", "B", "C", dt(10, 33), dt(11)),
        leg("T3", "B", "C", dt(10, 40), dt(11, 20)),
    ]
    got = earliest_arrival(edges, "A", "C", dt(9), minimum_transfer_seconds=300)
    assert got is not None
    assert [step.trip_id for step in got.legs] == ["T1", "T3"]


def test_stay_on_same_trip_without_transfer_penalty():
    edges = [
        leg("T", "A", "B", dt(10), dt(10, 30)),
        leg("T", "B", "C", dt(10, 30), dt(11)),
    ]
    got = earliest_arrival(edges, "A", "C", dt(9))
    assert got is not None
    assert got.arrival == dt(11)


def test_no_departure_no_journey():
    assert earliest_arrival([], "A", "B", dt(9)) is None
    assert earliest_arrival([], "A", "A", dt(9)).duration_seconds == 0


def test_reject_naive_date():
    with pytest.raises(ValueError):
        earliest_arrival([], "A", "B", datetime(2026, 10, 23, 9))


def test_trip_identity_includes_service_day():
    a = leg("123", "A", "B", dt(10), dt(10, 30))
    b = leg("123", "B", "C", dt(10, 30), dt(11), service_day=DAY + timedelta(days=1))
    assert earliest_arrival([a, b], "A", "C", dt(9)) is None


def test_over_midnight_from_previous_service_day():
    class FakeArchive:
        def connections_on(self, day):
            from navigateur.gtfs.static import Connection
            if day == DAY:
                return [Connection("night", "svc", "R", "A", "B", 24*3600+10*60, 24*3600+35*60)]
            return []
    query = dt(0, 5, day=DAY + timedelta(days=1))
    got = search_archive(FakeArchive(), "A", "B", query)
    assert got is not None
    assert got.departure.hour == 0 and got.departure.minute == 10
    assert got.arrival.minute == 35
