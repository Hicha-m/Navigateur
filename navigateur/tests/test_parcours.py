""""ce programme contient les tests des fonctions contenus dans le fichier "parcours.py""" ""

from navigateur.classes.Graphe import Graphe


from navigateur.fonctions.parcours import parcours_en_largeur, trouver_chemin


def test_parcours_en_largeur():
    g = Graphe(5)
    g.nouveau_graphe()
    g.ajouter_arc(0, 1)
    g.ajouter_arc(0, 2)
    g.ajouter_arc(2, 3)
    g.ajouter_arc(2, 4)
    g.ajouter_arc(3, 4)
    print(g)
    h = parcours_en_largeur(g, 0)
    print(h)

    assert h.tableaux == [
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    g.nouveau_graphe()
    g.ajouter_arc(0, 1)
    g.ajouter_arc(0, 2)
    g.ajouter_arc(0, 3)
    g.ajouter_arc(1, 3)
    g.ajouter_arc(2, 1)
    g.ajouter_arc(2, 3)
    g.ajouter_arc(2, 4)
    g.ajouter_arc(3, 4)
    g.ajouter_arc(4, 0)
    print(g)
    h = parcours_en_largeur(g, 0)
    print(h)

    assert h.tableaux == [
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
    ]


def test_trouver_chemin():
    pass
