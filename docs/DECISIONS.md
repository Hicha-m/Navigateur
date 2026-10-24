# Journal des décisions

## ADR-001 — Reprise incrémentale
**Date :** 2026-10-24
**Décision :** travailler sur `refactor/project-recovery` avec commits isolés. Ne pas modifier `main` directement.
**Motif :** préserver le projet scolaire historique et permettre une revue du code.
**Conséquence :** les adaptations du format des données seront explicitement documentées.

## ADR-002 — Commencer par les tests
**Date :** 2026-10-24
**Décision :** rétablir une suite de tests alignée sur l'API actuelle avant de corriger les algorithmes.
**Motif :** limiter les régressions au cours de la reprise.
