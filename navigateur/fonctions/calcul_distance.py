import numpy as np

TERRE_RAYON_METRES = 6_371_000
MARCHE_VITESSE_M_S = 1.1
MARCHE_VITESSE_M_MIN = MARCHE_VITESSE_M_S * 60


def calcul_distance_metres(lat1, lat2, lon1, lon2):
    """coords en degrees"""
    lat1, lat2, lon1, lon2 = [np.radians(col) for col in [lat1, lat2, lon1, lon2]]

    # https://en.wikipedia.org/wiki/Haversine_formula
    distance_metres = (
        2
        * TERRE_RAYON_METRES
        * np.arcsin(
            np.sqrt(
                np.sin((lat1 - lat2) / 2) ** 2
                + np.cos(lat1) * np.cos(lat2) * (np.sin((lon1 - lon2) / 2) ** 2)
            )
        )
    )
    return distance_metres


def marche_duree(lat1, lat2, lon1, lon2):
    distance_metres = calcul_distance_metres(lat1, lat2, lon1, lon2)
    marche_duree_minutes = int(distance_metres / MARCHE_VITESSE_M_MIN)
    return marche_duree_minutes


def marche_distance(duree):
    return duree * MARCHE_VITESSE_M_MIN
