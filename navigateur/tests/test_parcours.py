"""Tests du calcul des plus courts chemins."""
from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville
from navigateur.fonctions.parcours import parcours_Floyd_Warshall


def test_floyd_warshall_avec_etape():
    g = Graphe()
    a, b, c = [Ville(nom, (0, i)) for i, nom in enumerate(("a", "b", "c"))]
    for n in (a, b, c):
        g.ajouter_noeud(n)
    g.ajouter_arrete(a, b, 3)
    g.ajouter_arrete(b, c, 4)
    g.ajouter_arrete(a, c, 12)
    distances, _ = parcours_Floyd_Warshall(g)
    assert distances.avoir_arc(g.index_noeud(a), g.index_noeud(c)) == 7
