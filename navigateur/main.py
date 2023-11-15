"""Fichier qui exécute le projet"""

from navigateur.classes.Graphe import Graphe
from navigateur.classes.Ville import Ville


from navigateur.fonctions.get_csv import avoir_trajets, avoir_villes


villes = avoir_villes()  # toutes les villes de france
trajets = avoir_trajets()  # certaines villes de france

# print(villes)
# print(trajets)

villes_trajets = set()

for trajet in trajets:
    villes_trajets.add(trajet[0])
    villes_trajets.add(trajet[1])

# print(villes_trajets)

g = Graphe()

map_Villes = {}


for ville_trajet in villes_trajets:
    ville = villes[ville_trajet]
    v = Ville(ville_trajet, (ville[0], ville[1]))
    map_Villes[ville_trajet] = v
    g.ajouter_noeud(v)

for ville_debut, ville_fin, temps in trajets:
    g.ajouter_arrete(map_Villes[ville_debut], map_Villes[ville_fin], temps)

#print(g)
