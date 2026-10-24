# Changelog de la reprise

## 2026-10-24 — Branche refactor/project-recovery

- **test** : réalignement des tests historiques avec les interfaces actuelles et ajout de GitHub Actions.
- **build** : retrait de la dépendance du projet à lui-même dans `setup.py`.
- **fix** : correction des parcours de graphes et des chemins inaccessibles.
- **fix** : correction du générateur des connexions GTFS (durées par portion et conservation des destinations).
- **refactor** : cache des voisins en complément de la matrice dense.
- **fix** : validation des coordonnées web et réduction de la duplication des couches de carte.
- **docs** : documentation des limites, décisions et tâches restantes.

Note : ce changelog décrit le travail engagé sur la branche. Les états des tests et l'intégration à `main` doivent être vérifiés sur GitHub avant fusion.
