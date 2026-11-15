---
title: Terms and licence
nav_order: 12
---

# Terms and licence

This page is a record of what the licences say, not legal advice.

## The game is Microsoft's

Forza Horizon and Forza Motorsport, their tracks, cars and textures belong to
Microsoft (Playground Games and Turn 10 Studios), who do not endorse this
project. This repository holds **no file of the games** and no course, car or
texture made from one, and the tool **never downloads game content**: it reads
the copy **installed on your machine**.

What you point it at stays your responsibility. Games carry their own licence
terms, and EULAs commonly prohibit reverse engineering. Those are enforceable
contracts, and the obligation sits with whoever runs the tool. No design choice
here discharges it.

## No keys: none shipped, none recovered

**It reads containers.** Parsing an archive format is ordinary file handling.
ForzaTech's `.minizip` archives and their models, textures and placement files
are not encrypted, and the tool contains no key, recovers no key, reads no
other process's memory and injects nothing into the game. Laps come from the
telemetry the game publishes itself.

## Output is not for redistribution

What comes out is geometry for **spatial context**: the ground, the road and
what stands beside it, decimated to a budget, so laps can be analysed in place.
It is the least of what the archives hold, and it is still the publisher's
content.

- Keep exported `.glb` courses, the car file (`.h3dcars`) and the textures
  inside them for your own analysis, on the machine they were made on.
- Do not publish, share or sell exported courses, cars, models or textures.
- The repository's `.gitignore` keeps game files, exports, laps and recordings
  out of version control by file type (`*.glb`, `*.h3dcars`, `*.minizip`,
  `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` and more).

## The formats

ForzaTech's formats are undocumented. Reading them is reverse engineering of a
container. None of the readers here is derived from another project's source:
every offset was measured on the files, and how each was decided is written down
on [ForzaTech](reader-forzatech.md).

## Why this is a separate tool

The readers of each company's games live in their own repository, so a licensing
question or a takedown request about one game reaches only that game's tool.
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) keeps the
generic engine-format readers and the shared plumbing; this tool keeps Forza's.
If this repository has to go, nothing else goes with it.

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
