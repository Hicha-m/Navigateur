"""Fichier qui exécute le projet"""

from navigateur.fonctions.setup_graphe import (
    setup_g_villes,
    setup_g_gares,
    afficher_donnee_brut,
    afficher_donnee_brut,
    afficher_donnee_marche,
    afficher_donnee_ajout_marche,
)
from navigateur.fonctions.parcours import Itineraire, parcours_en_largeur
from matplotlib.pyplot import show

g_villes, dicte_villes, connexions_villes = setup_g_villes()
g_gares_tgv, dicte_Gares_tgv, connexions_gares_tgv = setup_g_gares(
    "export_gtfs_voyages"
)
g_gares_intercites, dicte_Gares_intercites, connexions_gares_intercites = setup_g_gares(
    "export-intercites-gtfs-last"
)
g_gares_ter, dicte_Gares_ter, connexions_gares_ter = setup_g_gares(
    "export-ter-gtfs-last"
)


"""
print(g_villes.avoir_noeuds_nom())
chemin, temps = Itineraire(
    g_villes, g_villes.avoir_noeud_nom("paris"), g_villes.avoir_noeud_nom("grenoble")
)
print([c.nom for c in chemin], temps)
"""
# print(parcours_en_largeur(g_villes.matrice, g_villes.index_nom("paris")))


map_graphe = {
    "0": (g_villes, g_gares_tgv),
    "1": (g_villes,),
    "2": (g_gares_tgv,),
    "3": (g_gares_intercites,),
    "4": (g_gares_ter,),
}
map_affichage = {
    "1": afficher_donnee_brut,
    "2": afficher_donnee_marche,
    "3": afficher_donnee_ajout_marche,
}

stop = True
while stop:
    entree_graphe = input(
        "Veuiller choisir vos graphes soit villes(1),soit gares_tgv(2),soit gares_intercites(3),soit gares_ter(4) ou villes,gares_tgv(0) : "
    )
    graphes = map_graphe.get(entree_graphe, False)

    if not graphes:
        continue

    entree_affichage = input(
        "Veuiller choisir votre type d'affichage soit brut(1) ou soit marche(2) ou soit ajout_marche(3) : "
    )

    affichage = map_affichage.get(entree_affichage, False)

    if not affichage:
        continue

    connexion = True

    for g in graphes:
        affichage(g, connexion)

    show()
