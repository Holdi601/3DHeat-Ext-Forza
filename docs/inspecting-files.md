---
title: Inspecting Forza files
nav_order: 7
---

# Inspecting Forza files: `identify`, `list`, `extract`

**In plain words:** a Forza track is stored in a few very large archive files.
These three commands say what a file is, show what an archive holds, and copy
one thing out of it. You do not need them to export a course; they are for
looking inside.

## identify

```
heat3d-forza-maps identify <file>
```

1. **Find a file.** A track's archives are in
   `<game folder>\media\Tracks\<map>\`: `GeoChunk0.minizip` to `GeoChunk3.minizip`,
   each with a `ChunkContentsMiniZip<n>.txt` beside it.
2. **Run it.** Example (synthetic numbers):

   ```
   > heat3d-forza-maps identify GeoChunk0.minizip
   GeoChunk0.minizip  (12,345,678,901 bytes)
     ForzaTech .minizip archive, version 101
       entries    98,304 in 192 segments
       names      ChunkContentsMiniZip0.txt
   ```

   The archive itself stores no names (see [ForzaTech](reader-forzatech.md)).
   `names` says which list names them; with none beside it, entries go by
   number (`#0`, `#1`, ...), and a list whose line count differs from the
   entries is reported as not belonging together.
3. **A model** extracted from an archive (`.modelbin`) is named too: its
   version, how many chunks it has, and the most common chunk tags. Chunk
   contents are not decoded here.

Anything that is neither says `<file>: not a Forza file` on standard error and
exits with code 2. The format is decided by the bytes, never by the extension.

## list

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

Each line is the unpacked size, the compression (`lz4`, `deflate` or
`stored`), and the path as the name list spells it, with the build machine's
prefix removed and the game's backslashes kept. `--filter` matches any part of
the path, ignoring case; `--limit` (default 50) caps the lines, not the count.

## extract

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

```
> heat3d-forza-maps extract GeoChunk0.minizip "scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin"
65,536 bytes -> autoterrain_x0_z0_cluster000.i.modelbin
```

The entry is the path exactly as `list` prints it, or `#<number>`. Without
`--out` it is written to the current folder under its own file name. An entry
that is not in the archive exits with code 1 (`not in the archive: ...`).

What you take out of the game's archives is the game's content: for your own
look inside, not for passing around ([Terms](terms.md)).
