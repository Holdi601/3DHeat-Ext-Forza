---
title: "Règles et licences"
nav_order: 12
lang: "fr"
source: terms.md
source_hash: "e6bd7ab93f27"
nav_exclude: true
search_exclude: true
---
# Règles et licences {#terms-and-licence}

## Le jeu appartient à Microsoft {#the-game-is-microsofts}

Forza Horizon et Forza Motorsport, leurs pistes, voitures et textures appartiennent à Microsoft
(Playground Games et Turn 10 Studios). 3DHeat Forza n'est ni affilié à Microsoft, Playground Games
ou Turn 10 Studios, ni soutenu par eux. Forza ainsi que les noms et marques associés appartiennent
à leurs propriétaires.

Ce dépôt ne contient **aucun fichier des jeux**, ni aucun parcours, aucune voiture ni aucune texture
qui en soit tirés - ni ressources du jeu, ni code du jeu, ni DLL -, et l'outil ne **télécharge
jamais de contenu de jeu** : il lit la copie **installée sur votre machine**.

## Pas de clés : aucune fournie, aucune récupérée {#no-keys-none-shipped-none-recovered}

Les archives `.minizip` de ForzaTech, et leurs modèles, textures et fichiers de placement, ne sont
pas chiffrés ; l'outil ne contient aucune clé, n'en récupère aucune, ne lit la mémoire d'aucun autre
processus et n'injecte rien dans le jeu. Les tours viennent de la télémétrie que le jeu publie
lui-même.

## La sortie n'est pas à redistribuer {#output-is-not-for-redistribution}

Ce qui sort est une géométrie pour le **contexte spatial** : le sol, la route et ce qui se trouve à
côté, simplifiés à un budget, pour pouvoir analyser les tours sur place. Elle reste sur votre machine.

- Gardez les parcours `.glb` exportés, le fichier de voitures (`.h3dcars`) et les textures qu'ils
  contiennent pour votre propre analyse, sur la machine où ils ont été faits.
- Ne publiez, ne partagez et ne vendez pas les parcours, voitures, modèles ou textures exportés.
- Le fichier `.gitignore` du dépôt tient les fichiers de jeu, les exports, les tours et les
  enregistrements hors du contrôle de version, par type de fichier (`*.glb`, `*.h3dcars`,
  `*.minizip`, `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` et d'autres).

## Les formats {#the-formats}

Les formats de ForzaTech ne sont pas documentés. Aucun des lecteurs ici n'est dérivé du code source d'un autre projet : chaque
décalage a été mesuré sur les fichiers, et la façon dont chacun a été établi est noté sur
[ForzaTech](reader-forzatech.md).

## Pourquoi c'est un outil à part {#why-this-is-a-separate-tool}

Chaque lecteur de jeu est un petit projet à part, avec son propre fichier de licence, ses propres versions et son propre suivi des tickets : il peut être installé, mis à jour, maintenu - ou retiré à la demande d'un ayant droit - seul, sans toucher au visualiseur ni aux autres outils.

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) garde les lecteurs génériques de
formats de moteur et la tuyauterie commune ; cet outil garde ceux de Forza.

Ayants droit : ouvrez un ticket sur [github.com/Holdi601/3DHeat-Ext-Forza/issues](https://github.com/Holdi601/3DHeat-Ext-Forza/issues) - nous répondons rapidement et retirons tout ce qui est demandé.

## La licence de cet outil {#this-tools-licence}

Tout ce qui est écrit pour ce dépôt est sous **licence MIT**
([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSE)) : vous pouvez
l'utiliser, le modifier, le diffuser, à des fins commerciales ou non.

Paquets tiers, tous permissifs
([`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSES.md)) :

| Paquet | Licence | Utilisé pour |
|---|---|---|
| 3DHeat GameFiles | MIT | l'écrivain glTF, les fichiers de tours, le couloir, les natures de sol, le budget de détail, les bibliothèques Steam |
| numpy | BSD-3-Clause | décodage des maillages |
| lz4 | BSD-3-Clause | les blocs LZ4 des archives `.minizip` |
| Pillow | MIT-CMU (HPND) | textures compressées par blocs, sortie JPEG |
| pytest | MIT | développement seulement |

Les licences ont été relevées dans les métadonnées des paquets en septembre 2026. Si les conditions
d'un composant ont changé depuis, c'est la source qui fait foi.
