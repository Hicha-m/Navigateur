# Stratégie de performance

## Etat
Le réseau TER contient environ 3 924 gares uniques. La matrice dense actuelle représente plus de 15 millions de cases et l'algorithme Floyd-Warshall fonctionne en O(V³).

## Changement incrémental
Les voisins sont désormais mis en cache dans `Graphe._voisins` pour éviter de parcourir une ligne complète de la matrice à chaque exploration Dijkstra. La matrice est maintenue pour conserver les usages existants (notamment Floyd-Warshall et Isomap).

## Étape suivante
Remplacer la matrice par une représentation sparse après avoir conçu des tests de compatibilité et des benchmarks sur le jeu TER. Ne pas appeler Floyd-Warshall sur le réseau TER complet avant optimisation. Mesurer temps et mémoire avant et après avec des conditions reproductibles.
