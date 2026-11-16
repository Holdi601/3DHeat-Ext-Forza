---
title: "Commandes"
nav_order: 3
lang: "fr"
source: commands.md
source_hash: "32f5e35285be"
nav_exclude: true
search_exclude: true
---
# Commandes {#commands}

Chaque commande s'écrit `heat3d-forza-maps <commande> ...` (ou, depuis le dossier de l'outil
sans l'installer, `python -m heat3d_ext_forza <commande> ...`).

| Commande | Prend | Fait |
|---|---|---|
| [`course`](#course) | un tour | exporte le parcours autour de lui |
| [`courses`](#courses) | une bibliothèque de tours enregistrés | lance `course` sur chaque parcours de la bibliothèque |
| [`races`](#races) | un Forza installé | liste chaque course que le jeu définit : ce qu'elle ajoute, ce qu'elle cache, les lieux, l'état de son export |
| [`terrain`](#terrain) | un dossier de piste Forza | découpe une zone à partir de coordonnées du monde |
| [`cars`](#cars) | un Forza installé | chaque voiture à faible détail, dans un seul fichier pour l'onglet Analyse de course du visualiseur |
| [`identify`](#identify) | un fichier | dit si c'est une archive Forza `.minizip` ou un modèle ForzaTech, et ce qu'elle contient |
| [`list`](#list) | un `.minizip` | liste ses entrées |
| [`extract`](#extract) | un `.minizip` | écrit une entrée sur le disque |

**Lire les exemples :** `<x>` signifie « remplacez-le par votre propre valeur, sans les
chevrons » ; `[...]` est facultatif ; un chemin contenant des espaces se met entre
« guillemets doubles », par exemple `"C:\Games\My Game"`. Vous débutez ? Voir
[Avant de commencer](before-you-start.md). La liste complète de `--help` de chaque commande
se trouve sur la [Référence des commandes](../cli-reference.md).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) lance cet outil avec vos
arguments inchangés pour ses propres commandes `course`, `courses`, `races`, `cars` et
`terrain` sur un tour ou une piste Forza, et demande à ses `identify`, `list` et `extract`
les fichiers Forza que ses propres lecteurs ne connaissent pas. C'est pourquoi `course`
accepte aussi `--level` et `--install` de GameFiles, et que `list` et `extract` acceptent
`--key` : ces options sont acceptées et ne servent à rien.

Chaque fois que le programme démarre, il peut d'abord vérifier s'il existe une version plus
récente. `HEAT3D_NO_UPDATE=1` désactive cette vérification.

Source : [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py).

## Codes de sortie {#exit-codes}

| Code | Signification |
|---|---|
| 0 | terminé |
| 1 | le travail a échoué : un tour illisible, un tour sans conduite, aucun terrain sous la conduite, un parcours de `courses` qui a échoué, un `.minizip` qui ne peut pas être lu ou dont la liste de noms ne lui appartient pas, une entrée absente de l'archive |
| 2 | rien à lire, ou mauvais arguments : aucun Forza installé, aucune piste sous la conduite, aucune bibliothèque de tours, un tour d'un autre jeu, un fichier qui n'est pas un fichier Forza, un chemin qui n'existe pas, une dépendance manquante (GameFiles, numpy, lz4, Pillow), `terrain` reçu avec ni `--box` ni `--route`, ou avec les deux, un argument que argparse refuse |

Chaque échec tient en une ou deux lignes sur la sortie d'erreur, qui dit quoi faire, et non
une trace Python.

---

## course {#course}

```
heat3d-forza-maps course <lap> [-o FILE] [options]
```

Cela exporte le parcours autour d'un tour : le sol dans une bande de chaque côté de la
conduite, et ce qui s'y dresse, dans un seul `.glb`. Le reste, la commande le trouve
elle-même : où le jeu est installé, sur laquelle de ses pistes le tour a été fait, et laquelle
des courses du jeu il suit. Voir [Export de parcours](course-export.md).

`<lap>` peut être l'une des formes suivantes (détails dans
[Entrées de tour](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)) :

- un fichier de tour : JSON de route, JSON de tour FH Companion, JSON `heat3d-lap`, `.npz`,
  ou `.csv` avec les colonnes x, y, z
- un dossier de fichiers de tour, fouillé récursivement (un parcours enregistré complet)
- un **nom** de parcours, cherché dans la bibliothèque FH Companion, à
  `%LOCALAPPDATA%\FHCompanion\laps`

### Options {#options}

| Option | Par défaut | Signification |
|---|---|---|
| `-o`, `--out FILE` | `<nom du parcours>.glb` dans le dossier courant, ou dans `$HEAT3D_LEVELS/forza/courses/` si cette variable est réglée | où écrire ; le nom est mis en minuscules, et chaque suite d'autres caractères devient `_` |
| `--margin M` | 80 | mètres de sol gardés de chaque côté de la conduite |
| `--texture-size {2048,1024,512}` | 2048 | pixels de texture de sol par carré de terrain de 512 m (2048 = 25 cm par pixel) |
| `--no-textures` | désactivé | couleurs unies seulement : un fichier bien plus petit. Cela supprime aussi la séparation route / bord |
| `--season {summer,autumn,winter,spring}` | summer | la saison dont on prend les cartes de sol et les textures des modèles |
| `--no-placed` | désactivé | le terrain seulement : ni bordures, ni barrières, ni panneaux, ni bâtiments |
| `--trees` | désactivé | place aussi les arbres, les buissons et les objets destructibles |
| `--detail-budget N` | automatique | un plafond de triangles pour tout ce qui est placé ; voir [Niveaux de détail et budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html) |
| `--track DIR` | cherchée | le dossier de piste (sous `media\Tracks`, contenant `GeoChunk0.minizip`) si le jeu installé ne doit pas être cherché |
| `--game {forza,beamng,acrally}` | ce que dit le fichier de tour, sinon `forza` | le jeu dont vient le tour (voir plus bas) |
| `--level`, `--install` | | acceptés pour la ligne de commande de GameFiles, non utilisés |

### Quel jeu {#which-game}

Le jeu est pris dans `--game`, puis dans le champ `game` d'un fichier `heat3d-lap` (ou dans la
ligne de description `# {...}` d'un CSV), et vaut par défaut Forza. Un dossier prend le jeu
que nomment ses fichiers, lorsqu'ils n'en nomment qu'un seul ; un fichier qui n'en nomme
aucun (un tour FH Companion, `course.json`, un CSV sans ligne de description) ne compte pas.

| Valeur | Ce qui se passe |
|---|---|
| commence par `forza` | l'export Forza |
| `beamng` | refusé, code de sortie 2 : `export it with heat3d-beamng-maps course` |
| `assetto-corsa-rally` ou `acrally` | refusé, code de sortie 2 : `export it with heat3d-acrally-maps course` |
| `assetto-corsa-evo` | refusé : « keeps all its content in one package obfuscated with a key, and this tool recovers none » |
| `iracing` | refusé : « tracks ship in a protected format that is not a file-extraction target » |
| autre valeur | refusé : « there is no course reader for <game> yet » |

Les trois derniers cas proposent aussi des solutions de rechange : reconstruire le parcours à
partir de la partie (3DHeat GameCapture), ou analyser les tours sans parcours, car l'onglet
Analyse de course du visualiseur trace une route à partir d'eux.

### Exemples {#examples}

```
# Un parcours de la bibliothèque FH Companion, par son nom
heat3d-forza-maps course "Example Circuit"

# Un fichier de tour, une bande plus étroite, un fichier plus petit
heat3d-forza-maps course lap.json -o example.glb --margin 40 --texture-size 1024

# Textures d'hiver, arbres compris
heat3d-forza-maps course "Example Circuit" --season winter --trees

# Un plafond strict de 500 000 triangles placés
heat3d-forza-maps course lap.json --detail-budget 500000

# Un dossier de piste donné directement (jeu installé dans un endroit où il n'est pas cherché)
heat3d-forza-maps course lap.json --track "D:\Games\<Forza>\media\Tracks\<map>"
```

Ce qu'affiche une exécution, sur une piste fictive que les tests construisent (sur une vraie
piste, les nombres se comptent en centaines de milliers de triangles, et la commande indique
la piste et la course qu'elle a trouvées) :

![course run on a made-up track](../assets/img/course-run.svg)

## courses {#courses}

```
heat3d-forza-maps courses [-o FOLDER] [options]
```

Cela lance `course` sur chaque dossier de parcours d'une bibliothèque de tours enregistrés, et
écrit un `<name>.glb` par parcours.

| Option | Par défaut | Signification |
|---|---|---|
| `-o`, `--out FOLDER` | `courses`, ou `$HEAT3D_LEVELS/forza/courses` si cette variable est réglée | le dossier où écrire (créé s'il manque) |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la bibliothèque de tours |
| `--only TEXT [TEXT ...]` | tous | seulement les parcours dont le nom de dossier contient l'un de ces textes (sans tenir compte des majuscules) |
| `--force` | désactivé | exporte de nouveau ce qui a déjà un `.glb` |
| `--track DIR` | cherchée | comme pour `course` |
| `--margin M` | 80 | comme pour `course` |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | comme pour `course` |

Ce qui compte comme dossier de parcours : un sous-dossier direct de la bibliothèque dont le nom
contient ` (course_`, la façon dont FH Companion les nomme, par exemple
`Example Circuit (course_1200_3400_to_1175_3400)`. La partie à partir de ` (course_` est retirée
du nom.

Comportement d'une exécution :

- Un parcours dont le `.glb` existe déjà est sauté (`kept`), sauf si `--force` est donné. Une
  exécution interrompue reprend donc là où elle s'est arrêtée.
- Un `.glb` écrit par une version plus ancienne, sans la couche propre à la course ni ses lieux
  (son `asset.extras.course_format` manque ou est inférieur au format actuel), est exporté de
  nouveau, comme si `--force` avait été donné pour lui seul.
- Deux dossiers de parcours qui ont le même nom avant ` (course_` (un enregistreur qui a donné à
  un nouveau parcours le nom d'un ancien) ne s'écrasent pas : le dossier créé en premier garde
  `<name>.glb`, l'autre est écrit sous `<name>_<start>.glb`, `<start>` étant l'endroit où il
  commence, les signes moins devenant `m` (par exemple `example_circuit_m120_m340.glb`).
- Un parcours qui échoue (tours illisibles, mémoire insuffisante, aucun terrain...) est signalé
  `FAILED`, et l'exécution continue.
- À la fin, elle affiche un tableau : l'état, la taille en Mo, les secondes écoulées et le nom,
  puis `<n> of <total> courses in <folder>`.
- Le code de sortie est 1 si un parcours a échoué, et 2 s'il n'y a pas de bibliothèque de tours.

```
heat3d-forza-maps courses -o courses --only circuit sprint --texture-size 1024
```

## races {#races}

```
heat3d-forza-maps races [-o FOLDER] [--markdown FILE] [options]
```

Liste chaque course qu'un Forza installé définit, d'après ses définitions de routes (voir
[Comment un parcours Forza est fait](course-forza-horizon.md#which-race)), et vérifie les exports
d'un dossier `courses` par rapport à elles. La commande lit le jeu et la bibliothèque de tours ;
elle n'écrit rien d'autre que le tableau optionnel.

| Option | Par défaut | Signification |
|---|---|---|
| `-o`, `--out FOLDER` | comme pour `courses` | le dossier où `courses` écrit, et dont les fichiers sont vérifiés |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la bibliothèque de tours |
| `--track DIR` | cherchée | le dossier de piste, s'il ne s'agit pas de celui du jeu installé |
| `--markdown FILE` | aucun | écrit aussi le tableau, en Markdown |

Une ligne par course, et une par parcours enregistré roulé sur elle :

| Colonne | Signification |
|---|---|
| route | l'identifiant de la route |
| course | le parcours enregistré qui lui correspond, s'il y en a un |
| own assets | les copies que la course ajoute au monde en roue libre |
| drawn | parmi celles-ci, les copies dont le modèle est livré par la piste |
| kinds | les copies ajoutées, par type (barrières, accessoires, décalcomanies, infrastructure, ...) |
| not geometry | marqueurs de spectateurs et splines de collision, comptés |
| hidden | objets de roue libre que la course retire |
| venue | les modèles de sol de lieu que la ligne IA de la course traverse à moins de 10 m |
| export | `current`, `older format` (exporté de nouveau par `courses`), `not exported`, ou vide pour une course sans parcours enregistré |

La commande se termine par un décompte : `<n> races: <a> with assets of their own, <v> through a
venue, <d> driven in the lap library, <s> recorded courses to export again`.

```
heat3d-forza-maps races -o courses --markdown races.md
```

## terrain {#terrain}

```
heat3d-forza-maps terrain <track folder> -o FILE (--box X0 Z0 X1 Z1 | --route FILE) [options]
```

C'est la découpe faite à la main : vous donnez le dossier de piste et une zone, et non un tour.
Elle sert quand la zone voulue est une boîte plutôt qu'un trajet.

| Option | Par défaut | Signification |
|---|---|---|
| `<path>` | obligatoire | un dossier de piste Forza sous `media\Tracks` (contenant `GeoChunk*.minizip`) |
| `-o`, `--out FILE` | obligatoire | le `.glb` à écrire |
| `--box X0 Z0 X1 Z1` | | la zone, en mètres du jeu (x et z, tels que la télémétrie les donne) ; les coins dans n'importe quel ordre |
| `--route FILE` | | un JSON de route avec `"bounds": {"min": [x, y, z], "max": [x, y, z]}`, tel qu'écrit par `heat3d_capture route` et `heat3d_capture laps` ; lu en UTF-8, avec ou sans marque d'ordre des octets |
| `--margin M` | **100** | mètres ajoutés autour des limites d'une route, et largeur du couloir quand la route a une ligne |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | comme pour `course` |

Donnez exactement un seul de `--box` et `--route`, sinon le code de sortie est 2. Avec
`--route`, la découpe suit les `bounds` (`min` / `max`, en x et z) de la route, élargis de la
marge. Si le fichier contient aussi au moins 10 positions, la découpe se resserre en un couloir
de `--margin` mètres autour d'elles, et les modèles placés reçoivent leur détail selon leur
distance à cette ligne. Avec `--box`, toute la boîte est gardée, et le détail va à ce qui se
trouve le plus près du milieu de la boîte.

L'altitude n'entre jamais dans la découpe. Une boîte hors de la carte, ou en mer, donne
« no terrain there » (code de sortie 1), et non une erreur sur les coordonnées.

```
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --box 0 0 512 512 -o piece.glb
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --route route.json -o map.glb
```

## cars {#cars}

```
heat3d-forza-maps cars [-o FILE] [--game FOLDER]
```

Chaque voiture d'un Forza installé, au niveau de détail bas du jeu, dans un seul fichier pour
l'onglet Analyse de course du visualiseur. Cela prend quelques secondes et écrit environ 5 Mo. Voir
[Voitures Forza](forza-cars.md).

## identify {#identify}

```
heat3d-forza-maps identify <path>
```

Lit le fichier et dit ce qu'il est, d'après ses octets et non son extension : une archive
ForzaTech `.minizip` (la signature `PGZP` : version, nombres d'entrées et de segments, et si la
liste `ChunkContentsMiniZip<n>.txt` qui nomme ses entrées se trouve à côté) ou un modèle
ForzaTech, `.modelbin` (version, nombre de morceaux, les étiquettes de morceaux les plus
fréquentes). Tout autre fichier sort avec le code 2 et `<file>: not a Forza file` sur la sortie
d'erreur. Voir [Inspecter les fichiers Forza](inspecting-files.md).

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

| Option | Par défaut | Signification |
|---|---|---|
| `<.minizip>` | obligatoire | un `.minizip` ForzaTech, comme le `GeoChunk0.minizip` d'une piste |
| `--filter TEXT` | aucun | seulement les chemins contenant TEXT, sans tenir compte des majuscules |
| `--limit N` | 50 | affiche au plus N entrées (le nombre total est toujours affiché) |
| `--key HEX` | aucun | accepté, non utilisé : un `.minizip` n'est pas chiffré |

Chaque ligne indique la taille décompressée, la compression (`lz4`, `deflate` ou `stored`) et le
chemin, tel que le fichier de noms placé à côté de l'archive le donne.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

| Option | Par défaut | Signification |
|---|---|---|
| `<entry>` | obligatoire | le chemin exactement tel que `list` l'affiche, ou `#<number>` |
| `--out FILE` | le nom de fichier de l'entrée (après le dernier `/` ou `\`), dans le dossier courant | où écrire ; les dossiers parents sont créés |
| `--key HEX` | aucun | accepté, non utilisé |

## Variables d'environnement {#environment-variables}

| Variable | Effet |
|---|---|
| `HEAT3D_LEVELS` | un dossier pour chaque export fait sans `-o` : les parcours dans `<HEAT3D_LEVELS>/forza/courses/`, le pack de voitures dans `<HEAT3D_LEVELS>/forza/`. Si elle n'est pas réglée, ils vont dans le dossier courant |
| `HEAT3D_GAMEFILES` | un dossier 3DHeat GameFiles, quand GameFiles n'est pas installé avec pip |
| `HEAT3D_NO_UPDATE` | toute valeur autre que vide, `0`, `false` ou `no` désactive la vérification de mise à jour |
| `LOCALAPPDATA` | l'endroit où sont cherchées la bibliothèque FH Companion et le cache des mises à jour |
| `HEAT3D_COURSE` | tests seulement : le parcours qu'utilise le test des bordures sur le jeu installé ; voir [Maintenance](maintaining.md#tests) |
