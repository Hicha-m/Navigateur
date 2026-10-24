from navigateur.classes.MatriceAdjacence import MatriceAdjacence
from navigateur.classes.File import File
from navigateur.classes.Graphe import Graphe, DEFAULT


def parcours_en_largeur(M, s):
    """Cette fonction renvoie un graphe H qui contient les sommets de G
    et seulement les arcs parcourus en explorant le graphe à partir du sommet s."""
    n = M.taille_graphe()
    couleur = [-1] * n
    for i in range(n):
        couleur[i] = "blanc"
    H = MatriceAdjacence(0, n)
    H.nouveau_graphe()
    F = File()
    couleur[s] = "rouge"
    F.enfiler(s)
    while not F.file_vide():
        i = F.defiler()
        for j in range(n ):
            if M.existe_arc(i, j) == True and couleur[j] == "blanc":
                couleur[j] = "rouge"
                H.ajouter_arc(i, j, M.avoir_arc(i, j))
                F.enfiler(j)
        couleur[i] = "vert"
    return H


def test_parcours_en_largeur():
    pass


def trouver_chemin(G, s, t):
    pass


def test_trouver_chemin():
    pass


def parcours_Floyd_Warshall(G: Graphe) -> (MatriceAdjacence, MatriceAdjacence):
    """
    Retourne la matrice d'adjacence du plus court chemin selon le poid de chaque connexion
    """

    dist_matrice = G.matrice.copy()
    predecesseur_matrice = (
        G.matrice.copy()
    )  # matrice predecesseur qui va permettre de retrouver le chemin avec les indices

    for i in range(dist_matrice.taille_graphe()):
        for j in range(dist_matrice.taille_graphe()):
            if dist_matrice.avoir_arc(i, j) != DEFAULT:
                predecesseur_matrice.ajouter_arc(i, j, i)

    for k in range(dist_matrice.taille_graphe()):
        # chaque pair de noeud i et j
        for i in range(dist_matrice.taille_graphe()):
            for j in range(dist_matrice.taille_graphe()):
                a = dist_matrice.avoir_arc(i, k)
                b = dist_matrice.avoir_arc(k, j)

                if a == DEFAULT or b == DEFAULT:
                    continue  # passe si k est inatteignable depuis i ou j

                chemin_intermediaire = a + b
                chemin_principale = dist_matrice.avoir_arc(i, j)
                if chemin_intermediaire < chemin_principale:
                    dist_matrice.ajouter_arc(i, j, chemin_intermediaire)
                    predecesseur_matrice.ajouter_arc(
                        i, j, predecesseur_matrice.avoir_arc(k, j)
                    )

    return (dist_matrice, predecesseur_matrice)


def avoir_chemin_Floyd_Warshall(
    G, nom1: str, nom2: str, predecesseur_matrice: MatriceAdjacence
) -> list:
    """
    Retourne une liste du chemin du noeud A à un noeud B
    """
    source = G.index_nom(nom1)
    destination = G.index_nom(nom2)
    if source is None or destination is None:
        raise ValueError("Sommet inconnu")
    chemin = [G.avoir_noeud_indice(destination)]
    courant = destination
    for _ in range(G.avoir_taille()):
        if courant == source:
            chemin.reverse()
            return chemin
        parent = predecesseur_matrice.avoir_arc(source, courant)
        if parent == DEFAULT or not isinstance(parent, int):
            return []
        courant = parent
        chemin.append(G.avoir_noeud_indice(courant))
    raise ValueError("Cycle détecté dans la matrice des prédécesseurs")


def Dijkstra(G, source):
    """Plus courts chemins depuis source pour des poids non négatifs."""
    import heapq

    if source not in G.noeudAindice:
        raise ValueError("Le sommet source est absent du graphe")

    dist = {node: float("inf") for node in G.avoir_noeuds()}
    previous = {source: source}
    dist[source] = 0
    queue = [(0, 0, source)]
    counter = 0

    while queue:
        cost, _, current = heapq.heappop(queue)
        if cost != dist[current]:
            continue
        for neighbor in G.avoir_adjacent(current):
            weight = G.avoir_poid(current, neighbor)
            if weight < 0:
                raise ValueError("Dijkstra exige des poids non négatifs")
            candidate = cost + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                previous[neighbor] = current
                counter += 1
                heapq.heappush(queue, (candidate, counter, neighbor))
    return dist, previous


def Itineraire(G, source, but):
    """Retourne (chemin, poids total), ou ([], inf) sans connexion."""
    if but not in G.noeudAindice:
        raise ValueError("Le sommet destination est absent du graphe")
    distances, previous = Dijkstra(G, source)
    if distances[but] == float("inf"):
        return [], float("inf")
    path = [but]
    while path[-1] != source:
        path.append(previous[path[-1]])
    path.reverse()
    return path, distances[but]


if __name__ == "__main__":
    pass
