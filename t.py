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
import numpy as np

D= villesDict
#Dictionnaire Métro dans Paris
M= g.matrice.matrice
print(D)
#Matrice des distances entre deux stations de métro voisines


def ListeVoisins(D,M,sommet):
    """Renvoie la liste des voisins de sommet dans le graphe"""
    return [voisin for voisin in D if M[D[sommet]][D[voisin]]>0]

def Min(Dis,T):
    """Renvoie un sommet non traité (qui n’est pas dans T) dont la valeur
    dans Dis est minimale"""
    m=np.inf
    for sommet in Dis:
        if sommet not in T and Dis[sommet]<=m:
            m=Dis[sommet]
            smin=sommet
    return smin

       
def Dijkstra(D,M,source):
    """Algorithme de Dijkstra: trouve le plus court chemin de source à 
    n’importe quel sommet"""
    T={}#dictionnaire dont les clés sont les sommets traités
    Dis={sommet:np.inf for sommet in D}
    Dis[source]=0
    P={source:source}
    for i in range(len(D)):
        smin=Min(Dis,T)
        T[smin]=smin
        for voisin in ListeVoisins(D,M,smin):
            d=Dis[smin]+M[D[smin]][D[voisin]]#distance entre source et voisin 
            #si on passe smin
            if Dis[voisin]>d:
                Dis[voisin]=d
                P[voisin]=smin
    return Dis,P   

def Itineraire(D,M,source,but):
    """Renvoie l'itinéraire dans le graphe du plus court chemin entre source
    et but"""
    Dis,P=Dijkstra(D,M,source)#On prend la version la plus rapide
    buti=but
    Chemin=[but]#Liste des sommets à parcourir
    while but!=source:
        but=P[but]
        Chemin.append(but)
    Chemin.reverse()#On obtient la liste à l’envers donc on la renverse
    return Chemin,Dis[buti]#On renvoie le chemin et le temps de parcours


print(Itineraire(D,M,"paris",'grenoble'))