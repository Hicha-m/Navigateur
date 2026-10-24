"""La CLI utilise le parser statique et ne dépend pas de Flask."""
from datetime import date
from zipfile import ZipFile

from navigateur.gtfs.__main__ import main


def test_cli_fixture(tmp_path, capsys):
    archive = tmp_path / "sncf.zip"
    with ZipFile(archive, "w") as zf:
        zf.writestr("calendar_dates.txt", "service_id,date,exception_type\nS,20261024,1\n")
        zf.writestr("trips.txt", "route_id,service_id,trip_id\nR,S,T\n")
        zf.writestr("stop_times.txt", "trip_id,arrival_time,departure_time,stop_id,stop_sequence\nT,10:00:00,10:00:00,A,1\nT,11:00:00,11:00:00,B,2\n")
        zf.writestr("stops.txt", "stop_id,stop_name,stop_lat,stop_lon\nA,A,43,5\nB,B,44,6\n")
    result = main(["--archive", str(archive), "--date", "2026-10-24"])
    assert result["connections"] == 1
    assert result["trips"] == 1
    assert result["stops"] == 2
    assert "2026-10-24" in capsys.readouterr().out
