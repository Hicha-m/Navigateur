"""Cherche un itinéraire horaire entre deux stop_id GTFS officiels."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from navigateur.gtfs.routing import search_archive
from navigateur.gtfs.static import GTFSArchive

PARIS = ZoneInfo("Europe/Paris")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Itinéraire théorique SNCF par identifiants GTFS")
    parser.add_argument("--archive", default="data/raw/sncf.zip", type=Path)
    parser.add_argument("--from-stop", required=True, dest="origin")
    parser.add_argument("--to-stop", required=True, dest="destination")
    parser.add_argument("--departure", required=True, help="Date et heure locale YYYY-MM-DDTHH:MM")
    parser.add_argument("--transfer-minutes", type=int, default=5)
    args = parser.parse_args(argv)
    value = datetime.fromisoformat(args.departure)
    if value.tzinfo is None:
        value = value.replace(tzinfo=PARIS)
    elif value.utcoffset() is None:
        parser.error("Fuseau horaire invalide")
    if args.transfer_minutes < 0:
        parser.error("Le temps de correspondance doit être positif ou nul")
    journey = search_archive(
        GTFSArchive(args.archive), args.origin, args.destination, value,
        minimum_transfer_seconds=args.transfer_minutes * 60,
    )
    if journey is None:
        result = {"found": False, "from": args.origin, "to": args.destination}
    else:
        result = {
            "found": True,
            "from": args.origin, "to": args.destination,
            "departure": journey.departure.isoformat(),
            "arrival": journey.arrival.isoformat(),
            "duration_seconds": journey.duration_seconds,
            "legs": [
                {
                    "trip_id": leg.trip_id,
                    "service_day": leg.service_day.isoformat(),
                    "from": leg.origin,
                    "to": leg.destination,
                    "departure": leg.departure.isoformat(),
                    "arrival": leg.arrival.isoformat(),
                }
                for leg in journey.legs
            ],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
