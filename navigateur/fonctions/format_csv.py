import csv
from unidecode import unidecode
import re
import os

from navigateur.fonctions.get_csv import avoir_trajets, avoir_villes


def formatter_temps_trains():
    trajets = []

    with open(
        "data/meilleurs-temps-des-parcours-des-trains.csv",
        mode="r",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            if int(row["annee"]) < 2019 or row["temps_estime_en_minutes"] == "":
                continue

            villes = str(row["relations"]).split(" - ")
            ville_debut = normaliser_texte(villes[0])
            ville_fin = normaliser_texte(villes[1])
            temps = int(float(row["temps_estime_en_minutes"]))

            trajets.append([ville_debut, ville_fin, temps])

    save(trajets, "ville_debut;ville_fin;temps", "trajets.csv")


def formatter_villes_France():
    villes = []

    with open("data/fr.csv", mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            ville = normaliser_texte(row["city"])
            latitude = float(row["lat"])
            longitude = float(row["lng"])

            villes.append([ville, latitude, longitude])

    save(villes, "ville;latitude;longitude", "villes.csv")


def formatter_villes_inter_trajets():
    trajets = avoir_trajets()
    villes = avoir_villes()

    villes_trajets = set(ville for trajet in trajets for ville in trajet[:2])

    villes_inter_trajets = []

    for ville_trajet in villes_trajets:
        villes_inter_trajets.append([ville_trajet, *villes[ville_trajet]])

    save(villes_inter_trajets, "ville;latitude;longitude", "villes_inter_trajets.csv")


def formatter_gtfs_stop(dir, export):
    stops = []
    stops_temp = {}
    stops_sans_dup = []

    with open("data/" + export + "/" + dir, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            stop_id = str(row["stop_id"])
            nom = normaliser_texte(row["stop_name"])
            coordonnees = (float(row["stop_lat"]), float(row["stop_lon"]))

            stops.append([stop_id, nom, *coordonnees])
            stops_temp[nom] = coordonnees

        for nom, coordonnees in stops_temp.items():
            stops_sans_dup.append([nom, *coordonnees])

    save(stops, "stop_id;nom;latitude;longitude", "stops.csv", export)
    save(stops_sans_dup, "nom;latitude;longitude", "stops_sans_dup.csv", export)


def formatter_gtfs_stop_temps(dir, export):
    stop_temps_voyage_id = {}
    stop_temps_stop_id = {}

    with open("data/" + export + "/" + dir, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            voyage_id = str(row["trip_id"])
            depart_temps = str(row["departure_time"]).split(":")
            temps_min = int(
                int(depart_temps[0]) * 60
                + int(depart_temps[1])
                + int(depart_temps[0]) / 60
            )
            stop_id = str(row["stop_id"])
            index = str(row["stop_sequence"])

            stop_temps_voyage_id.setdefault(voyage_id, {}).update(
                {index: [temps_min, stop_id]}
            )

    for voyage_id, dic in stop_temps_voyage_id.items():
        stops = []
        temps = []
        for i in range(len(dic)):
            i = str(i)
            stops.append(dic[i][1])
            temps.append(dic[i][0] - dic["0"][0])
        stop_temps_stop_id.setdefault(tuple(stops), temps)

    connexions = {}
    for tuples, temps in stop_temps_stop_id.items():
        for i in range(len(tuples) - 1):
            connexions.setdefault(tuples[i], [tuples[i + 1], temps[i + 1]])

    connexions_liste = []

    for stop, stop_Et_temps in connexions.items():
        connexions_liste.append([stop, stop_Et_temps[0], stop_Et_temps[1]])

    save(connexions_liste, "stop1;stop2;temps", "stops_temps.csv", export)


def normaliser_texte(text):
    return re.sub(r"[^a-zA-Z0-9 ]", " ", unidecode(text.lower()))


def save(liste, csv, dir, export="", sep=";"):
    n = len(csv.split(sep))
    export = "data/export/" + export
    os.makedirs(export, exist_ok=True)

    with open(export + "/" + dir, "w", encoding="utf-8") as file:
        file.write(f"{csv}\n")
        for elm in liste:
            for sub in range(n - 1):
                file.write(f"{elm[sub]};")
            file.write(f"{elm[-1]}\n")


if __name__ == "__main__":
    """
    formatter_temps_trains()
    formatter_villes_France()
    formatter_gtfs_stop("stops.txt", "export_gtfs_voyages")
    formatter_gtfs_stop_temps("stop_times.txt", "export_gtfs_voyages")
    """
    # formatter_villes_inter_trajets()

    # formatter_gtfs_stop("stops.txt", "export-intercites-gtfs-last")
    # formatter_gtfs_stop_temps("stop_times.txt", "export-intercites-gtfs-last")
    formatter_gtfs_stop("stops.txt", "export-ter-gtfs-last")
    formatter_gtfs_stop_temps("stop_times.txt", "export-ter-gtfs-last")
