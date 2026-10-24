# Changelog

## 2026-10-24 — Import de données SNCF
- **feat(gtfs)** : parseur statique sensible au calendrier, aux exceptions et aux horaires >24h.
- **test(gtfs)** : fixtures ZIP de services et de départs orientés ; test de la CLI.
- **feat(gtfs-rt)** : décodeur optionnel GTFS-RT, validation de fraîcheur, filtration stricte des annulations.
- **docs(data)** : registre des sources et règles d'identification.
- **cli** : inspection d'archives locales et téléchargement explicite.

## 2026-10-24 — Reprise technique du projet historique
- **test** : tests historiques remis à niveau et GitHub Actions.
- **build** : correction du packaging.
- **fix** : graphes, parcours, générateur GTFS historique, endpoints et carte.
- **refactor** : cache des voisins.
- **docs** : README et décisions de reprise.

Ne pas présenter ce changelog comme une validation d'itinéraires réels : le calcul temporel et l'intégration des retards ne sont pas encore disponibles.
