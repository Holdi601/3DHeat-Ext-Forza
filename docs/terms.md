---
title: Terms and licence
nav_order: 12
---

# Terms and licence

## The game is Microsoft's

Forza Horizon and Forza Motorsport, their tracks, cars and textures belong to
Microsoft (Playground Games and Turn 10 Studios). 3DHeat Forza is not
affiliated with or endorsed by Microsoft, Playground Games or Turn 10 Studios.
Forza and related names and trademarks belong to their owners.

This repository holds **no file of the games** and no course, car or texture
made from one - no game assets, no game code, no DLLs - and the tool **never
downloads game content**: it reads the copy **installed on your machine**.

## No keys: none shipped, none recovered

ForzaTech's `.minizip` archives and their models, textures and placement files
are not encrypted, and the tool contains no key, recovers no key, reads no
other process's memory and injects nothing into the game. Laps come from the
telemetry the game publishes itself.

## Output is not for redistribution

What comes out is geometry for **spatial context**: the ground, the road and
what stands beside it, decimated to a budget, so laps can be analysed in place.
It stays on your machine.

- Keep exported `.glb` courses, the car file (`.h3dcars`) and the textures
  inside them for your own analysis, on the machine they were made on.
- Do not publish, share or sell exported courses, cars, models or textures.
- The repository's `.gitignore` keeps game files, exports, laps and recordings
  out of version control by file type (`*.glb`, `*.h3dcars`, `*.minizip`,
  `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` and more).

## The formats

ForzaTech's formats are undocumented. None of the readers here is derived from another project's source:
every offset was measured on the files, and how each was decided is written down
on [ForzaTech](reader-forzatech.md).

## Why this is a separate tool

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn
on a rights holder's request - on its own, without affecting the viewer or the
other tools.

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) keeps the generic engine-format readers and the shared
plumbing; this tool keeps Forza's.

Rights holders: open an issue at
[github.com/Holdi601/3DHeat-Ext-Forza/issues](https://github.com/Holdi601/3DHeat-Ext-Forza/issues)
- we respond quickly and remove anything on request.

## This tool's licence

Everything written for this repository is under the **MIT licence**
([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSE)):
use it, change it, ship it, commercially or not.

Third-party packages, all permissive
([`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSES.md)):

| Package | Licence | Used for |
|---|---|---|
| 3DHeat GameFiles | MIT | the glTF writer, lap files, the corridor, ground kinds, the detail budget, Steam libraries |
| numpy | BSD-3-Clause | mesh decoding |
| lz4 | BSD-3-Clause | the `.minizip` archives' LZ4 blocks |
| Pillow | MIT-CMU (HPND) | block-compressed textures, JPEG output |
| pytest | MIT | development only |

The licences were read off the package metadata in September 2026. Where a
component's terms changed after that, the source is what counts.
