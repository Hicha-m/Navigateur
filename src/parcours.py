from Graphe import Graphe
from File import File

def parcours_en_largeur(G, s):
    """Cette fonction renvoie un graphe H qui contient les sommets de G 
    et seulement les arcs parcourus en explorant le graphe à partir du sommet s."""
    n = len(G)
    couleur = [-1]*n
    for i in range(n-1):
        couleur[i] = "blanc"
    H = Graphe(n)
    F = File()
    couleur[s] = "rouge"
    F.enfiler(s)
    while len(F) != 0:
        i = F.defiler()
        for j in range(n-1):
            if G.existe_arc(i,j) == True and couleur[j] == "blanc":
                couleur[j] = "rouge"
                H.ajouter_arc(i,j)
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
    pass
