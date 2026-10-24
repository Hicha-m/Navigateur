"""Cas de référence GTFS : calendrier, direction, branches, lendemain."""
from datetime import date
from zipfile import ZipFile

import pytest

from navigateur.gtfs.static import GTFSArchive, StopTime, connections_for_trip, gtfs_seconds, service_active


def test_gtfs_time_beyond_midnight():
    assert gtfs_seconds("25:05:03") == 90303
    with pytest.raises(ValueError):
        gtfs_seconds("10:99:00")


def test_calendar_exception_prioritaire():
    cal = dict(start_date="20261001", end_date="20261031", saturday="1")
    assert service_active(date(2026, 10, 24), cal, {}) is True
    assert service_active(date(2026, 10, 24), cal, {"20261024": 2}) is False
    assert service_active(date(2026, 10, 25), cal, {"20261025": 1}) is True


def test_arcs_temporels_orientes_et_durees():
    stops = [
        StopTime("T1", "C", 3, 3900, 3930),
        StopTime("T1", "A", 1, 0, 60),
        StopTime("T1", "B", 2, 1800, 1830),
    ]
    result = list(connections_for_trip(stops, trip_id="T1", route_id="R1", service_id="S1"))
    assert [(c.origin, c.destination, c.seconds) for c in result] == [
        ("A", "B", 1740), ("B", "C", 2070)
    ]


def test_archive_service_et_branches(tmp_path):
    path = tmp_path / "fixture.zip"
    contents = {
        "calendar_dates.txt": "service_id,date,exception_type\nS,20261024,1\n",
        "trips.txt": "route_id,service_id,trip_id\nR,S,T1\nR,S,T2\n",
        "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\nA,A,43,5\nB,B,44,6\nC,C,45,7\n",
        "stop_times.txt": (
            "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n"
            "T1,23:50:00,23:50:00,A,1\nT1,24:10:00,24:10:00,B,2\n"
            "T2,10:00:00,10:00:00,A,1\nT2,11:00:00,11:00:00,C,2\n"
        ),
    }
    with ZipFile(path, "w") as zf:
        for name, content in contents.items():
            zf.writestr(name, content)
    connections = GTFSArchive(path).connections_on(date(2026, 10, 24))
    assert {(c.origin, c.destination, c.seconds) for c in connections} == {
        ("A", "B", 1200), ("A", "C", 3600)
    }
    assert GTFSArchive(path).connections_on(date(2026, 10, 25)) == []
