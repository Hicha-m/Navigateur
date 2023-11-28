import matplotlib.pyplot as plt
from sklearn.manifold import Isomap
from navigateur.fonctions.parcours import (
    parcours_Floyd_Warshall,
)


class Interface:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        plt.title("Carte")

    def plot_villes(self, villes):
        x = [ville.coordonnee[1] for ville in villes]
        y = [ville.coordonnee[0] for ville in villes]
        noms = [ville.nom for ville in villes]

        self.ax.scatter(x, y)
        for i, nom in enumerate(noms):
            self.ax.annotate(
                nom,
                (x[i], y[i]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

    def plot_connexions(self, connexions):
        for connexion in connexions:
            ville1, ville2 = connexion[0], connexion[1]
            coord1 = ville1.coordonnee
            coord2 = ville2.coordonnee
            self.ax.plot([coord1[1], coord2[1]], [coord1[0], coord2[0]], "k--")

    def afficher_plot(self):
        plt.show()


def afficher_carte(g, avoir_connexion=False):
    # afficher villes et connexion
    plotter = Interface()
    plotter.plot_villes(g.avoir_noeuds())
    if avoir_connexion:
        plotter.plot_connexions(g.avoir_arretes())


def isomap_graphe(g, voisins=True):
    if voisins:
        voisins = g.avoir_taille() - 1

    dist = parcours_Floyd_Warshall(g)[0]

    adjacency_matrix = dist.matrice

    isomap = Isomap(n_components=2, n_neighbors=voisins)

    embedding = isomap.fit_transform(adjacency_matrix)

    plt.figure()
    plt.title("Isomap")
    plt.scatter(embedding[:, 0], embedding[:, 1])
    for i, (x, y) in enumerate(embedding):
        plt.annotate(
            str(g.avoir_noeud_indice(i).nom),
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )


if __name__ == "__main__":
    pass
