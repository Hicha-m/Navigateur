"""Tests des opérations élémentaires de graphes géographiques."""
from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville


def test_ajouter_noeud_et_arrete():
    g = Graphe()
    a = Ville("a", (43.0, 5.0))
    b = Ville("b", (44.0, 6.0))
    g.ajouter_noeud(a)
    g.ajouter_noeud(b)
    g.ajouter_arrete(a, b, 12)

    assert g.avoir_taille() == 2
    assert g.avoir_noeud_nom("a") is a
    assert g.avoir_poid(a, b) == 12
    assert g.avoir_poid(b, a) == 99999


def test_copie_est_independante():
    g = Graphe()
    a = Ville("a", (43.0, 5.0))
    b = Ville("b", (44.0, 6.0))
    g.ajouter_noeud(a)
    g.ajouter_noeud(b)
    copie = g.copie()
    copie.ajouter_arrete(a, b, 10)
    assert g.avoir_poid(a, b) == 99999
