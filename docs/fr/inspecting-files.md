---
title: "Inspecter les fichiers Forza"
nav_order: 7
lang: "fr"
source: inspecting-files.md
source_hash: "e6cee3695640"
nav_exclude: true
search_exclude: true
---
# Inspecter les fichiers Forza : `identify`, `list`, `extract` {#inspecting-forza-files-identify-list-extract}

**En clair :** une piste Forza est stockée dans quelques très gros fichiers d'archive. Ces trois
commandes disent ce qu'est un fichier, montrent ce que contient une archive, et en copient une
chose. Vous n'en avez pas besoin pour exporter un parcours ; elles servent à regarder à l'intérieur.

## identify {#identify}

```
heat3d-forza-maps identify <file>
```

1. **Trouver un fichier.** Les archives d'une piste se trouvent dans
   `<dossier du jeu>\media\Tracks\<map>\` : `GeoChunk0.minizip` à `GeoChunk3.minizip`, chacune
   avec un `ChunkContentsMiniZip<n>.txt` à côté.
2. **Lancer la commande.** Exemple (chiffres inventés) :

   ```
   > heat3d-forza-maps identify GeoChunk0.minizip
   GeoChunk0.minizip  (12,345,678,901 bytes)
     ForzaTech .minizip archive, version 101
       entries    98,304 in 192 segments
       names      ChunkContentsMiniZip0.txt
   ```

   L'archive elle-même ne stocke aucun nom (voir [ForzaTech](reader-forzatech.md)). `names`
   indique quelle liste les nomme ; sans liste à côté, les entrées sont désignées par leur numéro
   (`#0`, `#1`, ...), et une liste dont le nombre de lignes ne correspond pas aux entrées est
   signalée comme n'allant pas avec l'archive.
3. **Un modèle** extrait d'une archive (`.modelbin`) est aussi nommé : sa version, son nombre de
   morceaux, et les étiquettes de morceaux les plus fréquentes. Le contenu des morceaux n'est pas
   décodé ici.

Tout fichier qui n'est ni l'un ni l'autre affiche `<file>: not a Forza file` sur la sortie d'erreur
et sort avec le code 2. Le format est déterminé par les octets, jamais par l'extension.

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

```
> heat3d-forza-maps list GeoChunk0.minizip --filter autoterrain --limit 3
1,024 entries matching 'autoterrain'
        65,536  lz4    scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin
        61,440  lz4    scene\tbheightfield\autoterrain_x0_z0_cluster001.i.modelbin
        70,112  lz4    scene\tbheightfield\autoterrain_x0_z1023_cluster000.i.modelbin
  ... 1,021 more
```

Chaque ligne donne la taille décompressée, la compression (`lz4`, `deflate` ou `stored`) et le
chemin tel que le fichier de noms l'écrit, sans le préfixe de la machine de fabrication, et avec
les barres obliques inversées du jeu. `--filter` retient tout chemin qui contient le texte, sans
tenir compte des majuscules ; `--limit` (par défaut 50) limite le nombre de lignes, et non le
décompte.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

```
> heat3d-forza-maps extract GeoChunk0.minizip "scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin"
65,536 bytes -> autoterrain_x0_z0_cluster000.i.modelbin
```

L'entrée est le chemin exactement tel que `list` l'affiche, ou `#<number>`. Sans `--out`, elle est
écrite dans le dossier courant sous son propre nom de fichier. Une entrée absente de l'archive sort
avec le code 1 (`not in the archive: ...`).

Ce que vous extrayez des archives du jeu est le contenu du jeu : c'est pour votre propre examen,
non pour le faire circuler ([Conditions](terms.md)).
