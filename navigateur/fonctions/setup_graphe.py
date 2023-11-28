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
    dicteNoeud = {}
    mapNoeudStr = {}
    for nom, coor in localisation.items():
        noeud = classe(nom, coor)
        dicteNoeud[nom] = [*coor]
        g.ajouter_noeud(noeud)
        mapNoeudStr[nom] = noeud
    return dicteNoeud, mapNoeudStr


def avoir_mapGareId(stops: dict[str, tuple]):
    # stops
    map_gare_id = {}
    for id, nomETcoor in stops.items():
        nom = nomETcoor[0]
        map_gare_id[id] = nom
    return map_gare_id


def id(id):
    return id


def idENStr(id, map_id):
    return map_id[id]


def idENGare(id, map_id, map_str):
    return map_str[map_id[id]]


def idENVille(id, map_str):
    return map_str[id]


def avoir_connexions(
    trajets, g, convert_class, args_convert_class, convert_str, args_convert_str
):
    connexions = []

    for noeud1_str, noeud2_str, temps in trajets:
        connexions.append(
            [
                convert_str(noeud1_str, *args_convert_str),
                convert_str(noeud2_str, *args_convert_str),
                temps,
            ]
        )
        connexions.append(
            [
                convert_str(noeud2_str, *args_convert_str),
                convert_str(noeud1_str, *args_convert_str),
                temps,
            ]
        )

        g.ajouter_arrete(
            convert_class(noeud1_str, *args_convert_class),
            convert_class(noeud2_str, *args_convert_class),
            temps,
        )
        g.ajouter_arrete(
            convert_class(noeud1_str, *args_convert_class),
            convert_class(noeud2_str, *args_convert_class),
            temps,
        )

    return connexions


def setup_g_villes():
    g_villes = Graphe()
    ##donnée
    villes_inter_trajets = avoir_villes_inter_trajets()
    trajets = avoir_trajets()
    ##
    dicte_villes, map_villes_str = avoir_listeNoeud_mapNoeudStr(
        villes_inter_trajets, g_villes, Ville
    )
    connexions_villes = avoir_connexions(
        trajets, g_villes, idENVille, (map_villes_str,), id, ()
    )
    return g_villes, dicte_villes, connexions_villes


def setup_g_gares(export):
    g_gares = Graphe()
    ## donnée
    stops = avoir_gtfs_stop(export)
    stops_sans_dup = avoir_gtfs_stop_sans_dup(export)
    stops_temps = avoir_gtfs_stop_temps(export)
    ##
    dicte_Gares, map_gare_str = avoir_listeNoeud_mapNoeudStr(
        stops_sans_dup, g_gares, Gare
    )
    map_gare_id = avoir_mapGareId(stops)
    connexions_gares = avoir_connexions(
        stops_temps,
        g_gares,
        idENGare,
        (map_gare_id, map_gare_str),
        idENStr,
        (map_gare_id,),
    )
    return g_gares, dicte_Gares, connexions_gares


def afficher_donnee_brut(g, avoir_connexion):
    afficher_carte(g, avoir_connexion)
    isomap_graphe(g)


def afficher_donnee_marche(g, avoir_connexion):
    g_marche = g.marche_graphe()
    afficher_carte(g, avoir_connexion)
    isomap_graphe(g_marche)


def afficher_donnee_ajout_marche(g, avoir_connexion):
    afficher_carte(g, avoir_connexion)
    g.ajouter_arretes_manquante()
    isomap_graphe(g)


if __name__ == "__main__":
    pass
