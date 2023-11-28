from navigateur.classes.MatriceAdjacence import MatriceAdjacence
from navigateur.classes.File import File
from navigateur.classes.Graphe import Graphe, DEFAULT


def parcours_en_largeur(G, s):
    """Cette fonction renvoie un graphe H qui contient les sommets de G
    et seulement les arcs parcourus en explorant le graphe à partir du sommet s."""
    n = G.taille_graphe()  # voir le cas pour G si Graphe ou MAtriceADjacent
    couleur = [-1] * n
    for i in range(n - 1):
        couleur[i] = "blanc"
    H = MatriceAdjacence(n)
    H.nouveau_graphe()
    F = File()
    couleur[s] = "rouge"
    F.enfiler(s)
    while not F.file_vide():
        i = F.defiler()
        for j in range(n - 1):
            if G.existe_arc(i, j) == True and couleur[j] == "blanc":
                couleur[j] = "rouge"
                H.ajouter_arc(i, j)
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
    predecesseur_matrice = G.matrice.copy() # matrice predecesseur qui va permettre de retrouver le chemin avec les indices

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
                    predecesseur_matrice.ajouter_arc(i, j, predecesseur_matrice.avoir_arc(k, j))

    return (dist_matrice, predecesseur_matrice)


def avoir_chemin_Floyd_Warshall(
    G, nom1: str, nom2: str, predecesseur_matrice: MatriceAdjacence
) -> list:
    """
    Retourne une liste du chemin du noeud A à un noeud B
    """
    chemin = [nom2]
    noeud = nom2
    while noeud != nom1:
        noeud_index = G.index_nom(noeud)
        noeud = list(G.noeuds)[
            predecesseur_matrice.avoir_arc(G.index_nom(nom1), noeud_index)
        ]
        chemin.append(noeud)
    chemin.reverse()
    print(chemin)
    return chemin


''' a mettre en place
def ListeVoisins(D, M, sommet):
    """Renvoie la liste des voisins de sommet dans le graphe"""
    return [voisin for voisin in D if M[D[sommet]][D[voisin]] > 0]


def Min(Dis, T):
    """Renvoie un sommet non traité (qui n’est pas dans T) dont la valeur
    dans Dis est minimale"""
    m = np.inf
    for sommet in Dis:
        if sommet not in T and Dis[sommet] <= m:
            m = Dis[sommet]
            smin = sommet
    return smin


def Dijkstra(D, M, source):
    """Algorithme de Dijkstra: trouve le plus court chemin de source à
    n’importe quel sommet"""
    T = {}  # dictionnaire dont les clés sont les sommets traités
    Dis = {sommet: np.inf for sommet in D}
    Dis[source] = 0
    P = {source: source}
    for i in range(len(D)):
        smin = Min(Dis, T)
        T[smin] = smin
        for voisin in ListeVoisins(D, M, smin):
            d = Dis[smin] + M[D[smin]][D[voisin]]  # distance entre source et voisin
            # si on passe smin
            if Dis[voisin] > d:
                Dis[voisin] = d
                P[voisin] = smin
    return Dis, P


def Itineraire(D, M, source, but):
    """Renvoie l'itinéraire dans le graphe du plus court chemin entre source
    et but"""
    Dis, P = Dijkstra(D, M, source)  # On prend la version la plus rapide
    buti = but
    Chemin = [but]  # Liste des sommets à parcourir
    while but != source:
        but = P[but]
        Chemin.append(but)
    Chemin.reverse()  # On obtient la liste à l’envers donc on la renverse
    return Chemin, Dis[buti]  # On renvoie le chemin et le temps de parcours


print(Itineraire(D, M, "paris", "grenoble"))
'''

if __name__ == "__main__":
    g = MatriceAdjacence(2)
    g.nouveau_graphe()
    print(g)
