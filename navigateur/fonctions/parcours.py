from navigateur.classes.MatriceAdjacence import MatriceAdjacence
from navigateur.classes.File import File


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


if __name__ == "__main__":
    g = MatriceAdjacence(2)
    g.nouveau_graphe()
    print(g)