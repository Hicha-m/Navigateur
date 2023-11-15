from random import randint

from navigateur.classes.MatriceAdjacence import MatriceAdjacence


class Graphe:
    def __init__(self):
        self.noeud = []
        self.matrice = MatriceAdjacence()
        self.map = {}

    def indexe(self, n):
        """Retourne l'indexe du noeu dans
        la numérotation utilisé pour la matrice d'adjacence"""
        return self.map.get(n)

    def ajouter_noeud(self, valeur):
        self.noeud.append(valeur)
        self.map[valeur] = self.matrice.taille_graphe()
        self.matrice.etendre()

    def ajouter_arrete(self, s, t, poid):
        indexe_s, indexe_t = self.indexe(s), self.indexe(t)
        if indexe_s and indexe_t:
            self.matrice.ajouter_arc(indexe_s, indexe_t, poid)

    def avoir_noeud(self):
        return self.nodes

    def adjacent(self, s):
        return [
            self.noeud[i]
            for i in range(self.matrice.taille_graphe())
            if self.matrice.matrice[self.indexe(s)][i] != 0
        ]

    def poid(self, s, t):
        indexe_s, indexe_t = self.indexe(s), self.indexe(t)
        if indexe_s and indexe_t:
            return self.matrice.avoir_arc(indexe_s, indexe_t)

    def shortestpath(self):
        dist_matrice = self.matrice.copy()
        for k in range(self.matrice.taille_graphe()):
            for i in range(self.matrice.taille_graphe()):
                for j in range(self.matrice.taille_graphe()):
                    dist_matrice.set(
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
