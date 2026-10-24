"""Non-régressions pour les erreurs découvertes lors de l'audit."""
from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville
from navigateur.fonctions.parcours import Dijkstra, Itineraire, avoir_chemin_Floyd_Warshall, parcours_Floyd_Warshall
from navigateur.fonctions.setup_graphe import avoir_connexions, id, idENVille


def graphe_test():
    graph = Graphe()
    points = {name: Ville(name, (float(i), 0.0)) for i, name in enumerate(("a", "b", "c", "d"))}
    for point in points.values():
        graph.ajouter_noeud(point)
    return graph, points


def test_connexions_bidirectionnelles():
    graph, points = graphe_test()
    avoir_connexions([["a", "b", 7]], graph, idENVille, (points,), id, ())
    assert graph.avoir_poid(points["a"], points["b"]) == 7
    assert graph.avoir_poid(points["b"], points["a"]) == 7


def test_dijkstra_et_itineraire():
    graph, points = graphe_test()
    graph.ajouter_arrete(points["a"], points["b"], 2)
    graph.ajouter_arrete(points["b"], points["c"], 3)
    path, duration = Itineraire(graph, points["a"], points["c"])
    assert [node.nom for node in path] == ["a", "b", "c"]
    assert duration == 5
    assert Dijkstra(graph, points["a"])[0][points["c"]] == 5


def test_destination_inaccessible():
    graph, points = graphe_test()
    assert Itineraire(graph, points["a"], points["d"]) == ([], float("inf"))


def test_reconstruction_floyd():
    graph, points = graphe_test()
    graph.ajouter_arrete(points["a"], points["b"], 2)
    graph.ajouter_arrete(points["b"], points["c"], 3)
    _, pred = parcours_Floyd_Warshall(graph)
    assert [n.nom for n in avoir_chemin_Floyd_Warshall(graph, "a", "c", pred)] == ["a", "b", "c"]
    assert avoir_chemin_Floyd_Warshall(graph, "a", "d", pred) == []
