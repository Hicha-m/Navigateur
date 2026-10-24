# Journal des décisions (ADR)

## ADR-001 — Branche dédiée
Date : 2026-10-24. Travail sur `refactor/project-recovery` plutôt que directement sur `main`. Préserver l'historique et permettre une revue.

## ADR-002 — Tests avant migration
Date : 2026-10-24. Restaurer les tests existants et ajouter des régressions sur les parcours. Les tests constituent le contrat minimal pendant la reprise.

## ADR-003 — Préserver la compatibilité de Graphe
Date : 2026-10-24. Ajouter un cache de voisins sans supprimer encore la matrice. Une réécriture sparse nécessite des mesures, une migration des usages de Floyd-Warshall et une vérification de l'interface.

## ADR-004 — Données historiques non fiables
Date : 2026-10-24. Corriger la logique du générateur GTFS mais **ne pas** modifier arbitrairement les CSV historiques. Sans les archives source complètes, la correction exacte des durées et itinéraires antérieurs est impossible.

## ADR-005 — Itinéraire impossible
Date : 2026-10-24. Un itinéraire vers un nœud existant mais inatteignable renvoie `([], float("inf"))`. Les identifiants de nœuds absents produisent `ValueError`.

## ADR-006 — Licence du code de groupe
Date : 2026-10-24. Ne pas ajouter de licence sans accord des contributeurs. Le dépôt public n'implique pas automatiquement un droit de réutilisation libre.
