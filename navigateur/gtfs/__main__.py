"""CLI de validation d'archive GTFS statique, indépendante de l'interface web."""
import argparse
import json
from collections import Counter
from datetime import date

from navigateur.gtfs.static import GTFSArchive, download_gtfs

SNCF_GTFS = "https://eu.ftp.opendatasoft.com/sncf/plandata/Export_OpenData_SNCF_GTFS_NewTripId.zip"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspection des horaires GTFS SNCF")
    parser.add_argument("--archive", default="data/raw/sncf.zip", help="Chemin ZIP local")
    parser.add_argument("--download", action="store_true", help="Télécharger l'archive GTFS officielle en HTTPS")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(), help="Jour de service YYYY-MM-DD")
    args = parser.parse_args(argv)

    if args.download:
        download_gtfs(args.archive, url=SNCF_GTFS)

    connections = GTFSArchive(args.archive).connections_on(args.date)
    summary = {
        "service_day": args.date.isoformat(),
        "connections": len(connections),
        "trips": len({edge.trip_id for edge in connections}),
        "stops": len({stop for edge in connections for stop in (edge.origin, edge.destination)}),
        "routes": dict(Counter(edge.route_id for edge in connections).most_common(10)),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    main()
