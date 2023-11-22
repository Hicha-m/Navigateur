"""Fichier qui exécute le projet"""

from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville
from navigateur.classes.Interface import Interface

from navigateur.fonctions.get_csv import avoir_trajets, avoir_villes
from navigateur.fonctions.format_csv import (
    formatter_temps_trains,
    formatter_villes_France,
)
from os.path import exists

if exists("../data/fr.csv"):
    formatter_temps_trains()
if exists("../data/meilleurs-temps-des-parcours-des-trains.csv"):
    formatter_villes_France()


villes = (
    avoir_villes()
)  # toutes les villes de france dictionnaire{ ville:str : coord:(lat,lon)}
trajets = (
    avoir_trajets()
)  # certaines villes de france liste de liste [ville1,ville2,temps]

# print(villes)
# print(trajets)

villes_trajets = set()  # villes des trajets

for trajet in trajets:
    villes_trajets.add(trajet[0])
    villes_trajets.add(trajet[1])

# print(villes_trajets)

g = Graphe()

map_Villes = {}  # dictionnaire{ ville:str : ville:Ville}
villes_class = []  # liste des villes de type Ville

for ville_trajet in villes_trajets:
    ville = villes[ville_trajet]
    v = Ville(ville_trajet, (ville[0], ville[1]))
    map_Villes[ville_trajet] = v
    villes_class.append(v)
    g.ajouter_noeud(v)


connexions = []  # liste de tuple (ville1:Ville, ville2:Ville)

for ville_debut, ville_fin, temps in trajets:
    connexions.append((map_Villes[ville_debut], map_Villes[ville_fin]))
    connexions.append((map_Villes[ville_fin], map_Villes[ville_debut]))
    g.ajouter_arrete(map_Villes[ville_debut], map_Villes[ville_fin], temps)
    g.ajouter_arrete(map_Villes[ville_fin], map_Villes[ville_debut], temps)

# print(g) # matrice adjacence de g

dist = g.shortestpath()
# print(dist) # matrcide adjacence des plus courts chemins

villesDict = {ville.nom: g.index(ville) for ville in g.avoir_noeuds()}

# print(villesDict) # dictionnaire{ ville:str : index:int}


"""
# afficher villes et connexion
plotter = Interface()
plotter.plot_villes(villes_class)
plotter.plot_connexions(connexions)
plotter.afficher_plot()

"""

"""
# isomap 2d
adjacency_matrix = dist.matrice

# g.matrice.matrice
import matplotlib.pyplot as plt
from sklearn.manifold import Isomap


# Compute the Isomap embedding with 2 neighbors
isomap = Isomap(n_components=2)
embedding = isomap.fit_transform(adjacency_matrix)

# Plot the Isomap embedding
plt.scatter(embedding[:, 0], embedding[:, 1])
for i, (x, y) in enumerate(embedding):
    plt.annotate(
        str(g.avoir_noeud(i).nom),
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
    )
plt.show()
"""

"""
# isomap 3d
# Plot the adjacency matrix in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(embedding[:, 0], embedding[:, 1], embedding[:, 2])

# Add labels to the points
for i, (x, y, z) in enumerate(embedding):
    ax.text(
        x,
        y,
        z,
        str(g.avoir_noeud(i).nom),
    )

plt.show()
"""
