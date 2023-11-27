import csv


def avoir_trajets():
    trajets = []

    with open(
        "data/export/trajets.csv",
        mode="r",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            ville_debut = str(row["ville_debut"])
            ville_fin = str(row["ville_fin"])
            temps = int(row["temps"])

            trajets.append([ville_debut, ville_fin, temps])

    return trajets


def avoir_villes():
    villes = {}

    with open("data/export/villes.csv", mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            ville = str(row["ville"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            villes[ville] = [latitude, longitude]

    return villes


def avoir_villes_inter_trajets():
    villes_inter_trajets = {}
    with open(
        "data/export/villes_inter_trajets.csv", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            ville = str(row["ville"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            villes_inter_trajets[ville] = [latitude, longitude]

    return villes_inter_trajets


def avoir_gtfs_stop(export):
    stops = {}
    export = "export/" + export
    with open("data/" + export + "/stops.csv", mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            stop_id = str(row["stop_id"])
            name = str(row["nom"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            stops[stop_id] = [name, (latitude, longitude)]

    return stops


def avoir_gtfs_stop_sans_dup(export):
    stops_sans_dup = {}
    export = "export/" + export
    with open(
        "data/" + export + "/stops_sans_dup.csv", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            name = str(row["nom"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            stops_sans_dup[name] = (latitude, longitude)

    return stops_sans_dup


def avoir_gtfs_stop_temps(export):
    stops_temps = []
    export = "export/" + export
    with open(
        "data/" + export + "/stops_temps.csv", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            stop1 = str(row["stop1"])
            stop2 = str(row["stop2"])
            temps = int(row["temps"])

            stops_temps.append([stop1, stop2, temps])

    return stops_temps


"""
def avoir_gtfs_calendar_dates():
    calendar_dates = {}

    with open(
        "data/export_gtfs_voyages/calendar_dates.txt", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            service_id = str(row["service_id"])
            date = str(row["date"])

            calendar_dates[service_id] = date

    return calendar_dates


def avoir_gtfs_routes():
    routes = {}

    with open(
        "data/export_gtfs_voyages/routes.txt", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            route_id = str(row["route_id"])
            name = str(row["route_long_name"])

            routes[route_id] = name

    return routes


def avoir_gtfs_trips():
    trips = {}

    with open(
        "data/export_gtfs_voyages/trips.txt", mode="r", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            route_id = str(row["route_id"])
            service_id = str(row["service_id"])
            trip_id = str(row["trip_id"])

            trips[trip_id] = [route_id, service_id]

    return trips
"""

"""
calendar_dates_service_id : date
routes_route_id : name
stop_times_trip_id, stop_times_stop_id : departure_time
stop_stop_id : name,coordonne
trips_route_id, trips_service_id, trips_trip_id

"""
