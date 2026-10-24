# Routage horaire SNCF — état et contrat

## Décision d'architecture (ADR-010)

Le réseau horaire est traité comme un ensemble de connexions **datées**. Chaque arc GTFS conserve le jour de service, la course, le stop_id d'origine/destination et les instants de départ et d'arrivée. L'algorithme cherche l'arrivée la plus tôt après une heure demandée : il compare des instants et ajoute les durées d'attente, au lieu de sommer des poids statiques.

La solution initiale est un balayage de connexions chronologiques (inspiré de CSA), avec état de course pour distinguer une continuation à bord de la correspondance à un autre train. Il s'agit d'une version pédagogique, non encore optimisée pour toutes les courses nationales.

## Usage

Télécharger une archive théorique avec :
```sh
python -m navigateur.gtfs --download --date 2026-10-24
```

Consulter ensuite une recherche théorique utilisant les **stop_id** présents dans `stops.txt` :
```sh
python -m navigateur.gtfs.route_cli \
  --archive data/raw/sncf.zip \
  --from-stop "STOP_ID_ORIGINE" \
  --to-stop "STOP_ID_DESTINATION" \
  --departure 2026-10-24T09:30 \
  --transfer-minutes 5
```

Ces commandes sont indépendantes du serveur Flask. La sortie est JSON : `found`, horaires d'arrivée et de départ, durée totale, legs et identifiants de course. L'absence de trajet retourne `found: false`.

## Hypothèses

- Les horaires sont théoriques et les connexions sont orientées.
- Le départ demandé est en heure locale Europe/Paris si aucune zone n'est précisée.
- Une correspondance entre deux trains exige un délai minimal fixe de cinq minutes par défaut. Ce n'est pas une garantie de faisabilité en gare.
- La continuation dans un même `trip_id` et même jour de service n'exige pas de correspondance.
- Le routage examine le jour de service de la veille, du jour et du lendemain pour gérer les trains à horaires GTFS supérieurs à 24 heures.
- Le routage ne propose ni correspondances à pied, ni dates après l'horizon du GTFS, ni optimisation multi-critères.
- Le code ne traite pas encore rigoureusement toutes les ambiguïtés du changement d'heure hiver/été ; l'usage en production à ces dates exige une politique DST et des tests complémentaires.
- L'algorithme garde potentiellement de nombreux états par gare et par train : prévoir indexation et benchmarks avant un usage national massif.
- Les annulations/retards GTFS-RT ne sont pas appliqués au résultat théorique.
- Le calcul d'heure d'arrivée suppose que les horaires GTFS progressent, et rejette une connexion dont l'arrivée serait antérieure au départ.

## Tests attendus

- Attente avant départ, train plus tardif arrivant plus tôt.
- Correspondance insuffisante rejetée ; continuation à bord acceptée.
- Aucun trajet, même gare, heure sans fuseau.
- Course identifiée par (jour de service, trip_id).
- Correspondance avec un départ >24h et service de la veille.
- CLI sur fixture ZIP construite dans le test.

## Étape suivante

Construire un index local des courses, séparer heure de départ / heure d'arrivée par quai, gérer les règles `transfers.txt` et `pathways.txt`, associer les flux GTFS-RT de manière sûre et exposer une API paginée. Mesurer temps/mémoire sur l'archive officielle avant toute mise en production.
