class MatriceAdjacence:
    def __init__(self, valeur, dimension=0):
        self.dimension = dimension
        self.matrice = []
        self.default = valeur

    def nouveau_graphe(self):
        """methode qui renvoie un graphe de n sommets sans aucun arc"""
        self.matrice = [
            [self.default for j in range(self.dimension)] for i in range(self.dimension)
        ]

    def taille_graphe(self) -> int:
        """methode qui renvoie le nombre de sommets du graphe G"""
        return self.dimension

    def etendre(self):
        self.matrice.append([self.default for i in range(self.dimension)])
        self.dimension += 1
        for i in range(self.dimension):
            self.matrice[i].append(self.default)

    def ajouter_arc(self, i: int, j: int, v: int):
        """methode qui ajoute un arc i → j au graphe G"""
        self.matrice[i][j] = v

    def avoir_arc(self, i: int, j: int):
        """methode qui ajoute un arc i → j au graphe G"""
        return self.matrice[i][j]

    def existe_arc(self, i: int, j: int) -> bool:
        """methode qui renvoie True s’il y a un arc i → j dans le graphe G"""
        return self.matrice[i][j] != self.default

    def copy(self):
        """Return a new SquareMatrix containing the same values."""
        m = MatriceAdjacence(self.default)
        for i in range(self.dimension):
            m.etendre()
        for i in range(self.dimension):
            for j in range(self.dimension):
                m.ajouter_arc(i, j, self.avoir_arc(i, j))
        return m

    def __str__(self):
        # Find the maximum length of each column
        if len(self.matrice) != 0:
            column_widths = [
                max(len(str(row[i])) for row in self.matrice)
                for i in range(len(self.matrice[0]))
            ]
            line = ""
            # Print the matrix with aligned columns
            for row in self.matrice:
                nb = 0
                for i, value in enumerate(row):
                    nb += column_widths[i] + 1
                    line += "{:<{width}}".format(value, width=column_widths[i]) + "|"
                line += "\n"
                line += "-" * nb
                line += "\n"

            return line
        return ""


if __name__ == "__main__":
    pass
