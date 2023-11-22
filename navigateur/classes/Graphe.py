from random import randint

from navigateur.classes.MatriceAdjacence import MatriceAdjacence


class Graphe:
    def __init__(self, default=9999):
        self.noeuds = []
        self.matrice = MatriceAdjacence(default)
        self.map = {}

    def index(self, n):
        """Retourne l'index du noeu dans
        la numérotation utilisé pour la matrice d'adjacence"""
        return self.map.get(n)

    def ajouter_noeud(self, valeur):
        self.noeuds.append(valeur)
        self.map[valeur] = self.matrice.taille_graphe()
        self.matrice.etendre()

    def ajouter_arrete(self, s, t, poid):
        index_s, index_t = self.index(s), self.index(t)
        if type(index_s) is int and type(index_t) is int:
            self.matrice.ajouter_arc(index_s, index_t, poid)

    def avoir_noeud(self, i):
        longueur = len(self.noeuds)
        if -longueur < i < longueur:
            return self.noeuds[i]
        return None

    def avoir_noeuds(self):
        return self.noeuds

    def adjacent(self, s):
        return [
            self.noeuds[i]
            for i in range(self.matrice.taille_graphe())
            if self.matrice.matrice[self.index(s)][i] != 0
        ]

    def poid(self, s, t):
        index_s, index_t = self.index(s), self.index(t)
        if index_s and index_t:
            return self.matrice.avoir_arc(index_s, index_t)

    def shortestpath(self):
        dist_matrice = self.matrice.copy()

        for k in range(dist_matrice.taille_graphe()):
            for i in range(dist_matrice.taille_graphe()):
                for j in range(dist_matrice.taille_graphe()):
                    dist_matrice.ajouter_arc(
                        i,
                        j,
                        min(
                            dist_matrice.avoir_arc(i, j),
                            dist_matrice.avoir_arc(i, k) + dist_matrice.avoir_arc(k, j),
                        ),
                    )
        return dist_matrice

    def __str__(self):
        return str(self.matrice)


if __name__ == "__main__":
    pass
