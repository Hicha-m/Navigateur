# Feuille de route et critères de validation

## Phase 1 — Stabilisation
- [x] Corriger le packaging auto-référent.
- [x] Restaurer les tests des objets graphes et des parcours.
- [x] Ajouter GitHub Actions.
- [ ] Valider la CI après toutes les modifications.

## Phase 2 — Corrections fonctionnelles
- [x] Corriger la création des arcs dans le sens retour pour le modèle existant.
- [x] Corriger le parcours en largeur et Dijkstra.
- [x] Éviter la reconstruction infinie des chemins inaccessibles.
- [x] Corriger le code d'export GTFS : séquences d'arrêts, secondes, poids des arcs, embranchements.
- [ ] Régénérer et vérifier les CSV historiques depuis des sources GTFS complètes.
- [ ] Distinguer les services réellement directionnels des liaisons supposées bidirectionnelles.

## Phase 3 — Modernisation
- [x] Ajouter un cache des voisins pour réduire les balayages de la matrice durant Dijkstra.
- [x] Valider les coordonnées de l'API de marqueur et supprimer le décalage artificiel.
- [x] Éviter l'empilement des couches de données lors du rechargement des cartes.
- [ ] Remplacer la matrice dense après benchmarks et tests de migration.
- [ ] Refaire la gestion des clics et cercles dans Leaflet avec des groupes de couches séparés.
- [ ] Mettre à jour et auditer les versions des dépendances.

## Phase 4 — Documentation
- [x] Refaire le README et documenter les limitations.
- [x] Documenter le plan de reprise et les décisions.
- [x] Consigner la stratégie de performances.
- [ ] Ajouter des benchmarks quantifiés et des captures actualisées.
- [ ] Examiner la licence avec les autres contributeurs du projet.

## Règles de contribution
Toute modification doit rester isolée dans un commit descriptif, passer les tests unitaires et justifier les changements de contrat dans un test de non-régression. Ne pas fusionner une CI rouge. Ne pas publier des résultats de trajets réels à partir des CSV historiques non vérifiés.
