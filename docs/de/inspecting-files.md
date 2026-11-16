---
title: Forza-Dateien untersuchen
nav_order: 7
lang: "de"
source: inspecting-files.md
source_hash: "e6cee3695640"
nav_exclude: true
search_exclude: true
---
# Forza-Dateien untersuchen: `identify`, `list`, `extract` {#inspecting-forza-files-identify-list-extract}

**Einfach gesagt:** Eine Forza-Strecke liegt in ein paar sehr großen Archivdateien. Diese drei Befehle sagen, was eine Datei ist, zeigen, was ein Archiv enthält, und holen eine Sache daraus. Du brauchst sie nicht, um eine Strecke zu exportieren. Sie sind zum Hineinschauen da.

## identify {#identify}

```
heat3d-forza-maps identify <file>
```

1. **Finde eine Datei.** Die Archive einer Strecke liegen in `<game folder>\media\Tracks\<map>\`: `GeoChunk0.minizip` bis `GeoChunk3.minizip`, jeweils mit einer `ChunkContentsMiniZip<n>.txt` daneben.
2. **Starte es.** Beispiel (erfundene Zahlen):

   ```
   > heat3d-forza-maps identify GeoChunk0.minizip
   GeoChunk0.minizip  (12,345,678,901 bytes)
     ForzaTech .minizip archive, version 101
       entries    98,304 in 192 segments
       names      ChunkContentsMiniZip0.txt
   ```

   Das Archiv selbst speichert keine Namen (siehe [ForzaTech](reader-forzatech.md)).
   `names` sagt, welche Liste sie nennt. Liegt keine daneben, werden die Einträge über ihre Nummer angesprochen (`#0`, `#1`, ...). Eine Liste, deren Zeilenzahl nicht zu den Einträgen passt, wird als nicht zusammengehörig gemeldet.
3. **Ein Modell**, das aus einem Archiv geholt wurde (`.modelbin`), wird ebenfalls benannt: seine Version, wie viele Chunks es hat, und die häufigsten Chunk-Tags. Der Inhalt der Chunks wird hier nicht dekodiert.

Alles, was keins von beidem ist, meldet `<file>: not a Forza file` auf der Standardfehlerausgabe und endet mit Exit-Code 2. Das Format entscheiden die Bytes, nie die Endung.

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

Jede Zeile zeigt die entpackte Größe, die Komprimierung (`lz4`, `deflate` oder `stored`) und den Pfad, so wie die Namensliste ihn schreibt. Dabei ist das Präfix des Build-Rechners entfernt, und die Backslashes des Spiels bleiben erhalten. `--filter` trifft jeden Teil des Pfads, ohne Groß- und Kleinschreibung zu beachten. `--limit` (Standard 50) begrenzt die Zeilen, nicht die Anzahl.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

```
> heat3d-forza-maps extract GeoChunk0.minizip "scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin"
65,536 bytes -> autoterrain_x0_z0_cluster000.i.modelbin
```

Der Eintrag ist der Pfad genau so, wie `list` ihn ausgibt, oder `#<number>`. Ohne `--out` wird er im aktuellen Ordner unter seinem eigenen Dateinamen geschrieben. Ein Eintrag, der nicht im Archiv steht, endet mit Exit-Code 1 (`not in the archive: ...`).

Was du aus den Archiven des Spiels herausholst, ist Inhalt des Spiels: für deinen eigenen Blick hinein, nicht zum Weitergeben ([Regeln und Lizenzen](terms.md)).
