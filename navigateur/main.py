"""Fichier qui exécute le projet"""

from navigateur.fonctions.setup_graphe import (
    setup_g_villes,
    setup_g_gares,
    afficher_donnee_brut,
    afficher_donnee_brut,
    afficher_donnee_marche,
    afficher_donnee_ajout_marche,
)
from matplotlib.pyplot import show


g_villes = setup_g_villes()
g_gares = setup_g_gares()

stop = True
while stop:
    entre = input(
        "Veuiller choisir vos graphes soit ville(1) ou soit gare(2) ou les deux(0) : "
    )
    if entre == "0":
        entre = input(
            "Veuiller choisir votre type d'affichage soit brut(1) ou soit marche(2) ou soit ajout_marche(3) : "
        )
        if entre == "1":
            afficher_donnee_brut(g_villes)
            afficher_donnee_brut(g_gares)
            show()
        elif entre == "2":
            afficher_donnee_marche(g_villes)
            afficher_donnee_marche(g_gares)
            show()
        elif entre == "3":
            afficher_donnee_ajout_marche(g_villes)
            afficher_donnee_ajout_marche(g_gares)
            show()
    elif entre == "1":
        entre = input(
            "Veuiller choisir votre type d'affichage soit brut(1) ou soit marche(2) ou soit ajout_marche(3) : "
        )
        if entre == "1":
            afficher_donnee_brut(g_villes)
            show()
        elif entre == "2":
            afficher_donnee_marche(g_villes)
            show()
        elif entre == "3":
            afficher_donnee_ajout_marche(g_villes)
            show()
    elif entre == "2":
        entre = input(
            "Veuiller choisir votre type d'affichage soit brut(1) ou soit marche(2) ou soit ajout_marche(3) : "
        )
        if entre == "1":
            afficher_donnee_brut(g_gares)
            show()
        elif entre == "2":
            afficher_donnee_marche(g_gares)
            show()
        elif entre == "3":
            afficher_donnee_ajout_marche(g_gares)
            show()

    stop = True
