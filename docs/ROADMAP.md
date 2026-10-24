# Feuille de route et critères de validation

## Phase 1 — Stabilisation du projet historique
- [x] Corriger le packaging.
- [x] Restaurer les tests et mettre en place la CI.

## Phase 2 — Correction des algorithmes historiques
- [x] Corriger les arcs du modèle historique et la reconstruction des chemins.
- [x] Corriger le code de génération des poids des anciens CSV.
- [ ] Vérifier/régénérer les anciens exports si des sources historiques sont disponibles.

## Phase 3 — Import moderne de données SNCF (GTFS)
- [x] Ajouter un parseur GTFS statique indépendant des anciennes classes.
- [x] Respecter calendrier, exceptions, stop_sequence, arcs orientés, horaires après minuit.
- [x] Ajouter tests sur archive ZIP miniature entièrement reproductible.
- [x] Ajouter une CLI de téléchargement explicite et inspection.
- [ ] Tester avec une archive SNCF officielle réelle et documenter son schéma effectif.
- [ ] Créer un index persistant / cache construit en dehors de la requête HTTP.
- [x] Ajouter un premier moteur d'arrivée au plus tôt sur arcs GTFS datés, avec attentes et temps minimal de correspondance.\n- [x] Fournir une CLI JSON de recherche d'itinéraires par stop_id.\n- [ ] Faire évoluer le moteur pour les règles de transfert GTFS, les périodes de changement d'heure et de très grands volumes.

## Phase 4 — Temps réel SNCF
- [x] Ajouter le décodeur GTFS-RT optionnel et validation de fraîcheur.
- [x] Garantir que les identifiants non appariés n'altèrent pas les horaires théoriques.
- [x] Filtrer les annulations identifiées exactement.
- [ ] Ajouter le mapping vérifiable entre les identifiants GTFS / GTFS-RT, ainsi que les règles d'annulation et de changement d'arrêt.
- [ ] Propager les retards par arrêt et gérer l'information incomplète.
- [ ] Intégrer les alertes de service.
- [ ] Tester en direct les données et la couverture régionale.

## Phase 5 — Application et qualité
- [ ] Remplacer les opérations O(V²) et O(V³) de la matrice dense pour les grands graphes.
- [ ] Connecter le moteur horaire à une API et à une interface.
- [ ] Benchmarks, couverture d'intégration et tests de navigateur.
- [ ] Dépendances, licence et documentation finale.

Tout ajout doit être accompagné de tests et d'une décision documentée. Ne pas fusionner les changements sans validation de la CI.
