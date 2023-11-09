class Graphe:
    def __init__(self, n):
        self.n = n
        self.tableaux = []

    def nouveau_graphe(self, n: int) -> list[list[int]]:
        """methode qui renvoie un graphe de n sommets sans aucun arc"""
        for i in n:
            l = []
            for j in n:
                l.append(0)
            self.tableaux.append(l)
        return self.tableaux

    def taille_graphe(self) -> int:
        """methode qui renvoie le nombre de sommets du graphe G"""
        return len(self.tableaux)

    def ajouter_arc(self, i: int, j: int):
        """methode qui ajoute un arc i → j au graphe G"""
        for i in self.tableaux:
            for j in range(i):
                pass

    def existe_arc(self, i: int, j: int) -> bool:
        """methode qui renvoie True s’il y a un arc i → j dans le graphe G"""
        pass

    def afficher_graphe(self):
        """methode qui affiche la matrice d’adjacence du graphe G sur l’écran"""
        line = "-" + "-" * 4 * self.longueur + "\n"
        s = line
        for l in self.tableau:
            s += "| "
            for x in l:
                s += str(x) + " | "
            s += "\n" + line
        return s

    def test_graphe(self):
        """methode de test qui crée un graphe aléatoire et l’affiche sur l’écran"""
        pass

    def lire_graphe(self, nom_fichier):
        """méthode qui renvoie un graphe construit à partir de la matrice d’adjacence"""
        pass


if __name__ == "__main__":
    pass
