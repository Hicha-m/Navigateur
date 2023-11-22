import matplotlib.pyplot as plt


class Interface:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

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


if __name__ == "__main__":
    pass
