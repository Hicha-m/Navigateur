from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville
from navigateur.classes.Gare import Gare
from navigateur.classes.Interface import afficher_carte, isomap_graphe
from matplotlib.pyplot import show

from navigateur.fonctions.get_csv import (
    avoir_trajets,
    avoir_villes_inter_trajets,
    avoir_gtfs_stop,
    avoir_gtfs_stop_sans_dup,
    avoir_gtfs_stop_temps,
)


def avoir_listeNoeud_mapNoeudStr(localisation: dict[str, tuple], g, classe):
    listeNoeud = []
    mapNoeudStr = {}
    for nom, coor in localisation.items():
        noeud = classe(nom, coor)
        listeNoeud.append(noeud)
        g.ajouter_noeud(noeud)
        mapNoeudStr[nom] = noeud
    return listeNoeud, mapNoeudStr


def avoir_mapGareId(stops: dict[str, tuple]):
    # stops
    map_gare_id = {}
    for id, nomETcoor in stops.items():
        nom = nomETcoor[0]
        map_gare_id[id] = nom
    return map_gare_id


def idENGare(id, map_id, map_str):
    return map_str[map_id[id]]


def idENVille(id, map_str):
    return map_str[id]


def avoir_connexions(trajets, g, convert, args_convert):
    # convert idENGare
    connexions = []

    for noeud1, noeud2, temps in trajets:
        connexions.append(
            [convert(noeud1, *args_convert), convert(noeud2, *args_convert)]
        )
        connexions.append(
            [convert(noeud1, *args_convert), convert(noeud2, *args_convert)]
        )

        g.ajouter_arrete(
            convert(noeud1, *args_convert), convert(noeud2, *args_convert), temps
        )
        g.ajouter_arrete(
            convert(noeud1, *args_convert), convert(noeud2, *args_convert), temps
        )

    return connexions


def setup_g_villes():
    g_villes = Graphe()
    ##donnée
    villes_inter_trajets = avoir_villes_inter_trajets()
    trajets = avoir_trajets()
    ##
    liste_villes, map_villes_str = avoir_listeNoeud_mapNoeudStr(
        villes_inter_trajets, g_villes, Ville
    )
    connexions_villes = avoir_connexions(
        trajets, g_villes, idENVille, (map_villes_str,)
    )
    return g_villes


def setup_g_gares():
    g_gares = Graphe()
    ## donnée
    stops = avoir_gtfs_stop("export_gtfs_voyages")
    stops_sans_dup = avoir_gtfs_stop_sans_dup("export_gtfs_voyages")
    stops_temps = avoir_gtfs_stop_temps("export_gtfs_voyages")
    ##
    liste_Gares, map_gare_str = avoir_listeNoeud_mapNoeudStr(
        stops_sans_dup, g_gares, Gare
    )
    map_gare_id = avoir_mapGareId(stops)
    connexions_gares = avoir_connexions(
        stops_temps, g_gares, idENGare, (map_gare_id, map_gare_str)
    )
    return g_gares


def afficher_donnee_brut(g):
    afficher_carte(g)
    isomap_graphe(g)


def afficher_donnee_marche(g):
    g_marche = g.marche_graphe()
    afficher_carte(g)
    isomap_graphe(g_marche)


def afficher_donnee_ajout_marche(g):
    afficher_carte(g)
    g.ajouter_arretes_manquante()
    isomap_graphe(g)


if __name__ == "__main__":
    pass
