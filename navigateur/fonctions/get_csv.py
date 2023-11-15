import csv


def avoir_trajets():
    trajets = []

    with open(
        "data/trajets.csv",
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

    with open("data/villes.csv", mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")

        for row in reader:
            ville = str(row["ville"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            villes[ville] = [latitude, longitude]

    return villes
