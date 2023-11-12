import csv


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
            ville_debut = villes[0]
            ville_fin = villes[1]
            temps = int(float(row["temps_estime_en_minutes"]))

            trajets.append([ville_debut, ville_fin, temps])

    save(trajets, "data/trajets.csv", "ville_debut;ville_fin;temps")


def formatter_villes_France():
    villes = []

    with open("data/fr.csv", mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            ville = str(row["city"])
            latitude = float(row["lat"])
            longitude = float(row["lng"])

            villes.append([ville, latitude, longitude])

    save(villes, "data/villes.csv", "ville;latitude;longitude")


def save(liste, dir, csv, sep=";"):
    n = len(csv.split(sep))

    with open(dir, "w") as file:
        file.write(f"{csv}\n")
        for elm in liste:
            for sub in range(n - 1):
                file.write(f"{elm[sub]};")
            file.write(f"{elm[-1]}\n")


formatter_temps_trains()
formatter_villes_France()
