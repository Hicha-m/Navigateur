# Sources SNCF et contrat de données

Document établi le 24 octobre 2026. Source officielle :
https://transport.data.gouv.fr/datasets/horaires-sncf

## Fichiers retenus

| Couche | Standard | Usage |
| --- | --- | --- |
| Théorique | GTFS ZIP | `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, calendriers |
| Réel | GTFS-RT Trip Updates | Retards, changements d'horaires et annulations |
| Alertes | GTFS-RT Service Alerts | Perturbations et communications voyageurs, à intégrer ultérieurement |
| Alternatifs | NeTEx / SIRI Lite | Non intégrés dans le MVP (éviter les doublons et identifiants incohérents) |

- GTFS officiel : https://eu.ftp.opendatasoft.com/sncf/plandata/Export_OpenData_SNCF_GTFS_NewTripId.zip
- Trip Updates : https://proxy.transport.data.gouv.fr/resource/sncf-gtfs-rt-trip-updates
- Service Alerts : https://proxy.transport.data.gouv.fr/resource/sncf-gtfs-rt-service-alerts

La fiche du jeu de données annonce environ 151 jours d'horizon théorique et une actualisation toutes les deux minutes des Trip Updates pour les circulations des 60 prochaines minutes. Ces chiffres sont les caractéristiques annoncées du fournisseur, **pas** une garantie d'exactitude du moteur.

## Règles d'intégration

1. Les IDs `stop_id` désignent les arrêts ; les noms des gares ne servent pas de clé unique.
2. Les horaires GTFS dépassant 24:00:00 sont rapportés au jour de service du train.
3. `service_id` se calcule avec `calendar.txt` ET `calendar_dates.txt`.
4. Les arcs restent dirigés, ordonnés par `stop_sequence`, et stockent départ et arrivée, pas seulement un poids fixe.
5. Un flux temps réel doit être frais ; sa fraîcheur se déduit de l'horodatage `FeedHeader.timestamp`.
6. Pas de rapprochement automatique entre numéro commercial et `trip_id` sans table documentée. Le périmètre GTFS-RT de la SNCF n'est pas garanti pour tous les TER et services régionaux.
7. Les données historiques sous `data/export/` ne sont pas écrasées par l'importeur.
8. Les archives sources téléchargées sont locales et ignorées par Git. Valider leurs sources, la taille, le schéma et les droits de redistribution avant publication.
9. Un trajet à date/heure exige des contraintes temporelles : montée/descente, attentes, changements de jour et correspondances. Le simple Dijkstra pondéré en durée ne suffit pas pour obtenir un itinéraire horaire exact.

## Limites du code actuel

- `GTFSArchive.connections_on` lit une archive locale pour un jour de service donné mais ne possède pas encore de stockage persistant ni d'index pour des requêtes massives.
- Le parseur RT est disponible mais non connecté à un service périodique. L'adaptateur ne transpose pas encore les retards par arrêt : il filtre seulement les annulations correspondant à un identifiant exact et à un jour exact.
- Aucune promesse de temps réel ne doit être affichée dans l'interface avant mise en place de la gestion de cache, de l'expiration et de la correspondance des IDs.
- Le moteur de routage horaire, les transferts entre quais/gares et le choix de date/heure sont à réaliser dans une phase suivante.

## Validation

Exécuter `python -m pytest -q`. Pour une validation réelle avec la ressource du jour, télécharger manuellement l'archive du fournisseur et appeler `GTFSArchive(path).connections_on(date)` depuis un script Python, puis inspecter les services retenus. Ne pas committer les archives.
