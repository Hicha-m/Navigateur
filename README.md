# Navigateur — exploration de trajets ferroviaires

Projet pédagogique Python de graphes géographiques, avec représentation de réseaux de villes et de gares, recherche d'itinéraires et visualisation cartographique.

> **État du projet : reprise technique en cours.** Les données fournies sont historiques : elles ne représentent pas une offre de transport ni des horaires en temps réel. La recherche utilise des poids fixes, sans calcul de correspondances par horaire.

## Installation

Prérequis : Python 3.11 conseillé.

```bash
git clone https://github.com/Hicha-m/Navigateur.git
cd Navigateur
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell : .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

Lancer l'application depuis la racine du dépôt :

```bash
python -m app.app
```

Ouvrir http://127.0.0.1:5000

La démonstration des graphes en ligne de commande :

```bash
python -m navigateur.main
```

## Tests

```bash
python -m pytest -q
```

GitHub Actions effectue les tests à chaque commit de la branche de reprise et à chaque demande de fusion vers `main`.

## Architecture

- `navigateur/classes/` : structures de données et affichage Python/Matplotlib
- `navigateur/fonctions/` : création des graphes, lecture des CSV, algorithmes, calculs de distance
- `navigateur/tests/` : tests Python
- `app/` : serveur Flask et interface Leaflet
- `data/export/` : données CSV historiques fournies avec le projet
- `docs/` : décisions techniques, plan de reprise et performances

Les PDF `Sujet.pdf` et `Projet-navigateur.pdf` sont les documents historiques du projet.

## Limites connues

- La matrice d'adjacence reste dense et coûteuse pour le réseau TER.
- Les CSV GTFS historiques peuvent contenir des durées cumulées et une perte de branches due à l'ancien export ; ils doivent être régénérés depuis les jeux GTFS source avant d'être considérés comme fiables.
- Les données source utilisées par `format_csv.py` ne sont pas toutes présentes dans le dépôt.
- L'interface web est une démonstration, sans requête de recherche d'itinéraire complète.
- Le calcul des temps de marche repose sur la distance à vol d'oiseau, non sur le réseau piétonnier.

## Suivi de reprise

Lire [ROADMAP](docs/ROADMAP.md), [DECISIONS](docs/DECISIONS.md) et [PERFORMANCE](docs/PERFORMANCE.md). Les changements sont réalisés sur une branche dédiée avant revue.

## Historique

Projet réalisé en groupe dans le cadre du portail René Descartes (2023). Voir l'historique Git pour les contributions individuelles.

## Données SNCF actuelles : import séparé

Le nouvel importeur est indépendant de l'ancien graphe de démonstration. Les anciennes données ne sont pas remplacées automatiquement.

Télécharger explicitement le dernier GTFS SNCF et inspecter les services pour un jour donné :

```bash
python -m navigateur.gtfs --download --date 2026-10-24
```

Réutiliser ensuite la copie locale (sans télécharger à nouveau) :

```bash
python -m navigateur.gtfs --archive data/raw/sncf.zip --date 2026-10-25
```

Le téléchargement n'est pas déclenché au lancement du serveur. Les archives sont ignorées par Git. Le jour doit être compris dans la période réellement couverte par l'archive téléchargée.

Le temps réel GTFS-RT est un composant expérimental isolé. Pour décoder son flux :

```bash
python -m pip install -r requirements-realtime.txt
```

**Important :** les mises à jour temps réel ne sont pas encore affichées sur la carte et les retards ne sont pas encore utilisés pour calculer des itinéraires. Voir [DATA_SOURCES](docs/DATA_SOURCES.md) et [ROADMAP](docs/ROADMAP.md).
