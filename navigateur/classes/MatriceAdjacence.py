class MatriceAdjacence:
    def __init__(self, dimension=0):
        self.dimension = dimension
        self.matrice = []

    def nouveau_graphe(self):
        """methode qui renvoie un graphe de n sommets sans aucun arc"""
        self.matrice = [
            [0 for j in range(self.dimension)] for i in range(self.dimension)
        ]

    def taille_graphe(self) -> int:
        """methode qui renvoie le nombre de sommets du graphe G"""
        return self.dimension

    def etendre(self):
        self.matrice.append([0 for i in range(self.dimension)])
        self.dimension += 1
        for i in range(self.dimension):
            self.matrice[i].append(0)

    def ajouter_arc(self, i: int, j: int, v: int):
        """methode qui ajoute un arc i → j au graphe G"""
        self.matrice[i][j] = v

    def avoir_arc(self, i: int, j: int):
        """methode qui ajoute un arc i → j au graphe G"""
        return self.matrice[i][j]

    def existe_arc(self, i: int, j: int) -> bool:
        """methode qui renvoie True s’il y a un arc i → j dans le graphe G"""
        return self.matrice[i][j] == 1

    def copy(self):
        """Return a new SquareMatrix containing the same values."""
        m = MatriceAdjacence()
        for i in range(self.dimension):
            m.extend()
        for i in range(self.dimension):
            for j in range(self.dimension):
                m.ajouter_arc(i, j, self.avoir_arc(i, j))
        return m

    def __str__(self):
        """methode qui affiche la matrice d’adjacence du graphe G sur l’écran"""
        line = "-" + "-" * (6 * self.dimension - 1) + "\n"
        s = line

        max_width = len(str(max(map(max, self.matrice))))

        for row in self.matrice:
            s += "| "
            for element in row:
                # Right-align each element within the cell
                s += str(element).rjust(max_width) + " | "
            s += "\n" + line

        return s
    

if __name__ == "__main__":
    pass
