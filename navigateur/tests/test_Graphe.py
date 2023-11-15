""""ce programme contient les tests des méthodes contenus dans le fichier "Graphe.py""" ""

from navigateur.classes.Graphe import Graphe


def test_instance():
    taille = 3
    g = Graphe(taille)

    assert isinstance(g, Graphe) == True


def test_nouveau_graphe():
    taille = 3
    g = Graphe(taille)
    g.nouveau_graphe()
    assert g.tableaux == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def test_taille_graphe():
    taille = 3
    g = Graphe(taille)
    g.nouveau_graphe()
    assert g.taille_graphe() == taille
    assert g.n == taille


def test_ajouter_arc():
    taille = 3
    g = Graphe(taille)
    g.nouveau_graphe()
    g.ajouter_arc(0, 0)
    assert g.tableaux == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    g.ajouter_arc(1, 1)
    assert g.tableaux == [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    g.ajouter_arc(2, 2)
    assert g.tableaux == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def test_existe_arc():
    taille = 3
    g = Graphe(taille)
    g.nouveau_graphe()
    assert g.existe_arc(2, 2) == False
    g.ajouter_arc(0, 0)
    assert g.existe_arc(0, 0) == True
