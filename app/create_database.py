import sqlite3
from navigateur.fonctions.get_csv import avoir_trajets, avoir_villes

# DELETE FROM cities; DELETE FROM connections;

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect("base_de_donnee.db")

# Création d'une table pour les villes
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    )
"""
)

# Création d'une table pour les connexions
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        city1_id INTEGER NOT NULL,
        city2_id INTEGER NOT NULL,
        travel_time INTEGER NOT NULL,
        FOREIGN KEY (city1_id) REFERENCES cities (id),
        FOREIGN KEY (city2_id) REFERENCES cities (id)
    )
"""
)

# Fermer la connexion
conn.close()


villes = avoir_villes()
trajets = avoir_trajets()

villes_trajets = set()  # villes des trajets

for trajet in trajets:
    villes_trajets.add(trajet[0])
    villes_trajets.add(trajet[1])


conn = sqlite3.connect("base_de_donnee.db")
cursor = conn.cursor()

id_villes = {}

for index, ville_trajet in enumerate(villes_trajets):
    ville = villes[ville_trajet]
    lat, long = ville
    querry = f"INSERT INTO cities (name, latitude, longitude) VALUES ('{ville_trajet}', {lat}, {long})"
    print(querry)
    cursor.execute(querry)
    id_villes[ville_trajet] = index + 1


for ville_debut, ville_fin, temps in trajets:
    querry = f"INSERT INTO connections (city1_id, city2_id, travel_time) VALUES ({id_villes[ville_debut]}, {id_villes[ville_fin]}, {temps})"
    cursor.execute(querry)


conn.commit()
conn.close()
