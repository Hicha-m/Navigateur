import sqlite3


def fetch_data_from_database():
    conn = sqlite3.connect("base_de_donnee.db")
    cursor = conn.cursor()

    # Sélectionnez les données nécessaires pour mettre à jour la carte
    cursor.execute(
        """
        SELECT cities.id, cities.name, cities.latitude, cities.longitude
        FROM cities
    """
    )
    cities = cursor.fetchall()

    cursor.execute(
        """
        SELECT connections.city1_id, connections.city2_id, connections.travel_time
        FROM connections
    """
    )
    connections = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    # Retournez les données pour la mise à jour de la carte
    return {"cities": cities, "connections": connections}
