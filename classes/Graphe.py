from random import randint

class Graphe:
    def __init__(self, n):
        self.n = n
        self.tableaux = []

    def nouveau_graphe(self):
        """methode qui renvoie un graphe de n sommets sans aucun arc"""
        t = []
        for i in range(self.n):
            l = []
            for j in range(self.n):
                l.append(0)
            t.append(l)
        self.tableaux = t

    def taille_graphe(self) -> int:
        """methode qui renvoie le nombre de sommets du graphe G"""
        return len(self.tableaux)

    def ajouter_arc(self, x: int, y: int):
        """methode qui ajoute un arc i → j au graphe G"""
        for i in range(len(self.tableaux)):
            if i == x:
                for j in range(len(self.tableaux[i])):
                    if j == y:
                        self.tableaux[i][j] = 1

    def existe_arc(self, x: int, y: int) -> bool:
        """methode qui renvoie True s’il y a un arc i → j dans le graphe G"""
        return self.tableaux[x][y] == 1

    def __str__(self):
        """methode qui affiche la matrice d’adjacence du graphe G sur l’écran"""
        line = "-" + "-" * 4 * self.n + "\n"
        s = line

        for l in self.tableaux:
            s += "| "
            for x in l:
                s += str(x) + " | "
            s += "\n" + line
        return s

    def lire_graphe(self, nom_fichier):
        """méthode qui renvoie un graphe construit à partir de la matrice d’adjacence"""
        pass


def test_graphe():
    """methode de test qui crée un graphe aléatoire et l’affiche sur l’écran"""
    n = randint(1, 10)
    g = Graphe(n)
    g.nouveau_graphe()

    nombre_arc = randint(0, n * n)
    for i in range(nombre_arc):
        x = randint(0, n)
        y = randint(0, n)
        g.ajouter_arc(x, y)
    print(g)


if __name__ == "__main__":
    """
    g = Graphe(5)
    g.nouveau_graphe()
    g.ajouter_arc(3,1)

    print(g.afficher_graphe())
    """
    test_graphe()
