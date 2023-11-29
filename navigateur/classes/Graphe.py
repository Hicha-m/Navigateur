from navigateur.classes.MatriceAdjacence import MatriceAdjacence
from navigateur.fonctions.calcul_distance import marche_duree


DEFAULT = 99999


class Graphe:
    """
    Graphe des localisation de point géographique sur une carte
    Chaque points sont des noeuds d'attributs nom et coordonnees
    Ayant des connexions entre eux pondéré par un poid (= temps,distance,vitesse...)
    """

    def __init__(self, default=DEFAULT):
        self.noeuds = []
        self.arretes = []
        self.matrice = MatriceAdjacence(default)
        self.noeudAindice = {}  # Noeud : indice
        self.strAindice = {}  # str : indice

    def index_noeud(self, noeud) -> int:
        """
        Retourne l'index du noeud dans
        la numérotation utilisé pour la matrice d'adjacence
        """
        return self.noeudAindice.get(noeud)

    def index_nom(self, noeud) -> int:
        """
        Retourne l'index du nom du noeud dans
        la numérotation utilisé pour la matrice d'adjacence
        """
        return self.strAindice.get(noeud)

    def ajouter_noeud(self, noeud):
        """
        Ajoute le noeud dans la liste noeuds,
        l'associe à son indice (noeudAindice) et son nom (strAindice)
        """
        n = self.avoir_taille()
        self.noeuds.append(noeud)
        self.noeudAindice[noeud] = n
        self.strAindice[noeud.nom] = n
        self.matrice.etendre()
        self.ajouter_arrete(noeud, noeud, 0)  # par def de la position

    def ajouter_arrete(self, noeud1, noeud2, poid: int):
        """
        Ajoute une connexion entre deux noeuds et un poid (= temps,distance,vitesse...)
        """
        index_noeud1, index_noeud2 = self.index_noeud(noeud1), self.index_noeud(noeud2)
        if type(index_noeud1) is int and type(index_noeud2) is int:
            self.matrice.ajouter_arc(index_noeud1, index_noeud2, poid)
            self.arretes.append([noeud1, noeud2])

    def avoir_noeud_nom(self, nom: str):
        """
        Retourne un noeud selon son nom
        """
        i = self.strAindice.get(nom)
        if type(i) is int:
            return self.noeuds[i]
        return None

    def avoir_noeud_indice(self, i):
        """
        Retourne un noeud selon son indice
        """
        longueur = len(self.noeuds)
        if -longueur < i < longueur:
            return self.noeuds[i]
        return None

    def avoir_noeuds(self) -> list:
        """
        Retourne la liste de tous les noeuds
        """
        return self.noeuds

    def avoir_noeuds_nom(self) -> list:
        """
        Retourne la liste de tous les noeuds
        """
        return [noeud.nom for noeud in self.noeuds]

    def avoir_arrete(self, noeud1, noeud2) -> list:
        """
        Retourne la liste de toutes les connexions
        """
        return self.matrice.avoir_arc(self.index_noeud(noeud1),self.index_noeud(noeud2))

    def avoir_arretes(self) -> list:
        """
        Retourne la liste de toutes les connexions
        """
        return self.arretes

    def avoir_taille(self) -> int:
        """
        Retourne le nombre de noeud présent
        """
        return len(self.noeuds)

    def avoir_adjacent(self, noeud) -> list:
        """
        Retourne la liste des noeuds adjacents (voisins) au noeud
        """
        return [
            self.noeuds[i]
            for i in range(self.matrice.taille_graphe())
            if self.matrice.matrice[self.index_noeud(noeud)][i] != DEFAULT
        ]

    def avoir_poid(self, noeud1, noeud2) -> int:
        """
        Retourne le poid de deux noeuds
        """
        index_noeud1, index_noeud2 = self.index_noeud(noeud1), self.index_noeud(noeud2)
        if type(index_noeud1) is int and type(index_noeud2) is int:
            return self.matrice.avoir_arc(index_noeud1, index_noeud2)

    def marche_graphe(self):
        """
        Retourne un graphe de la durée de marche entre tous les noeuds
        """

        g = self.copie()

        for noeud1 in g.avoir_noeuds():
            for noeud2 in g.avoir_noeuds():
                p = marche_duree(
                    noeud1.coordonnee[0],
                    noeud2.coordonnee[0],
                    noeud2.coordonnee[1],
                    noeud1.coordonnee[1],
                )
                g.ajouter_arrete(noeud1, noeud2, p)
        return g

    def ajouter_arretes_manquante(self):
        """
        Ajoute pour chaque connexions manquantes une connexions de marche entre deux noeuds
        Permet d'avoir l'ordre de grandeur entre les noeuds pour l'Isomap
        """

        g = self.marche_graphe()

        for noeud1 in self.avoir_noeuds():
            for noeud2 in self.avoir_noeuds():
                p_w = g.avoir_poid(noeud1, noeud2)
                if p_w < self.avoir_poid(noeud1, noeud2):
                    self.ajouter_arrete(noeud1, noeud2, p_w)
                    self.ajouter_arrete(noeud2, noeud1, p_w)

    def copie(self):
        """
        Retourne une nouvelle MatriceAdjacence qui contient les mêmes valeurs
        """
        g = Graphe()
        for noeud in self.avoir_noeuds():
            g.ajouter_noeud(noeud)
        for noeud1 in self.avoir_noeuds():
            for noeud2 in self.avoir_noeuds():
                g.ajouter_arrete(noeud1, noeud2, self.avoir_poid(noeud1, noeud2))
        return g

    def __str__(self):
        """
        Affiche la matrice d'adjacence avec classe
        """
        if len(self.matrice.matrice) != 0:
            column_widths = [
                max(len(str(row[i])) for row in self.matrice.matrice)
                for i in range(len(self.matrice.matrice[0]))
            ]
            line = ""
            # Print the matrix with aligned columns
            for j, row in enumerate(self.matrice.matrice):
                nb = 0
                for i, value in enumerate(row):
                    nb += column_widths[i] + 1
                    line += "{:<{width}}".format(value, width=column_widths[i]) + "|"
                line += " " + self.noeuds[j].nom
                line += "\n"
                line += "-" * nb
                line += "\n"

            return line
        return ""


if __name__ == "__main__":
    pass
