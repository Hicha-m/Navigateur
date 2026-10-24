# Plan de reprise du projet

La branche `refactor/project-recovery` isole les travaux de la branche principale.

## Phase 1 — Stabilisation
- [x] Corriger la dépendance circulaire du packaging.
- [x] Adapter les anciens tests à l'API actuelle.
- [x] Déclarer les tests GitHub Actions.
- [ ] Constater une exécution CI réussie.

## Phase 2 — Correction fonctionnelle
- [ ] Corriger la construction des arcs et les algorithmes de parcours.
- [ ] Corriger l'extraction GTFS et contrôler les CSV historiques.
- [ ] Ajouter les tests de non-régression.

## Phase 3 — Modernisation
- [ ] Mesurer mémoire et temps sur les graphes TER.
- [ ] Envisager une liste d'adjacence, après conservation de la compatibilité.
- [ ] Revoir l'API Flask et l'interface Leaflet.

## Phase 4 — Documentation
- [ ] Documenter le périmètre et les limitations.
- [ ] Fournir un guide reproductible pour le lancement et les tests.
- [ ] Préparer une revue avant intégration dans main.

Les données CSV actuelles sont historiques et ne doivent pas être présentées comme des horaires SNCF actuels.
