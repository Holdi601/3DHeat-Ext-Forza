# 3DHeat Forza: Forza courses, races and cars as 3D files

**What is it?** This tool builds a 3D model of a Forza race track from your own
Forza install (Forza Horizon or Forza Motorsport, the ForzaTech engine): give it
a lap you drove, and it writes the road, the verge and grass, the kerbs,
barriers, tyre walls, signs and buildings around it, plus what the game puts out
for that race alone, as one `.glb`. It also writes every car at low detail into
one file.

**Why would I use it?** To see your laps in the
[3DHeat](https://github.com/Holdi601/3DHeat) viewer on the real track: speed,
braking and lines painted on the road, laps compared corner by corner in the
Race analysis tab, each car drawn in its own shape.

**Example:** `heat3d-forza-maps course "Example Circuit"` -> `example_circuit.glb`,
in the game's own coordinates, so a recorded lap lies on it with no placing.

**Documentation:** [holdi601.github.io/3DHeat-Ext-Forza](https://holdi601.github.io/3DHeat-Ext-Forza/), a page per
command with step-by-step use and example output, in the 3DHeat viewer's
languages. Part of [3DHeat](https://github.com/Holdi601/3DHeat)
([documentation](https://holdi601.github.io/3DHeat/)).

This tool is kept outside the other 3DHeat tools on purpose: it reads
Microsoft's game files. If it ever has to go, nothing else goes with it. What it
writes stays on your machine.

## Install

New to the command line? Read [Before you start](https://holdi601.github.io/3DHeat-Ext-Forza/before-you-start.html) first.

1. Install Python 3.10 or later, and a Forza through Steam or the Microsoft Store.
2. `git clone https://github.com/Holdi601/3DHeat-Ext-Forza` (or download the
   ZIP) and open a terminal in that folder.
3. Install the command; this also installs
   [3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles), the library
   the readers build on, and numpy, lz4 and Pillow:

```bash
python -m pip install -e .        # installs the heat3d-forza-maps command
heat3d-forza-maps --help          # the commands
```

Running from a plain checkout without installing (`python -m heat3d_ext_forza`)
works too: GameFiles is then found through `HEAT3D_GAMEFILES`, the `gamefiles`
folder of a 3DHeat checkout, or a `3DHeat-GameFiles` folder beside this one.

## Commands

| Command | Does | Page |
|---|---|---|
| `course <lap> [-o file.glb]` | the track around a lap, working out the game, track, race and cut by itself | [Course export](https://holdi601.github.io/3DHeat-Ext-Forza/course-export.html) |
| `courses [-o folder]` | `course` for every course in a recorded lap library | [Commands](https://holdi601.github.io/3DHeat-Ext-Forza/commands.html#courses) |
| `races [--markdown file]` | every race the game defines, and whether your exports of it are current | [Commands](https://holdi601.github.io/3DHeat-Ext-Forza/commands.html#races) |
| `terrain <track folder> -o file.glb (--box ... \| --route ...)` | a piece of track by world coordinates | [Commands](https://holdi601.github.io/3DHeat-Ext-Forza/commands.html#terrain) |
| `cars [-o forza.h3dcars]` | every car at low detail, for the viewer's Race analysis tab | [Forza cars](https://holdi601.github.io/3DHeat-Ext-Forza/forza-cars.html) |
| `identify <file>` | what a Forza file is (a `.minizip` archive or a ForzaTech model) | [Inspecting Forza files](https://holdi601.github.io/3DHeat-Ext-Forza/inspecting-files.html) |
| `list <.minizip>`, `extract <.minizip> <entry>` | what an archive holds, one entry out | [Inspecting Forza files](https://holdi601.github.io/3DHeat-Ext-Forza/inspecting-files.html) |

```bash
heat3d-forza-maps course "Example Circuit"                  # a course from the FH Companion library, by name
heat3d-forza-maps course lap.json -o example.glb --margin 40
heat3d-forza-maps courses -o courses                        # the whole library, one file per course
heat3d-forza-maps cars                                      # forza.h3dcars
```

Exit status: 0 done; 1 the work failed (an unreadable lap, no terrain under it,
an unreadable archive); 2 nothing to read (no Forza installed, no lap library,
not a Forza file or lap, a missing dependency), with a line saying what to do.
Every option, as the program prints it:
[Command reference](https://holdi601.github.io/3DHeat-Ext-Forza/cli-reference.html).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) runs this
tool for its own `course`, `courses`, `races`, `cars` and `terrain` on a Forza
lap or track, with the same options.

## What comes out, and loading it

A course is one glTF binary: a node per part, named `ground:road x<X> z<Z>`,
`ground:verge ...`, `ground:terrain ...` (per 512 m terrain tile, each with its
baked ground texture), `ground:kerbs`, `ground:markings`, `water:water`,
`structure:<category>` for what stands on the ground, and
`structure:event_<category>` for the race's own layer. Load it in the viewer's
**Background / level** panel with **3D model…**. The car file loads with
**Load car file...** in the race tab's view settings.
[Course export](https://holdi601.github.io/3DHeat-Ext-Forza/course-export.html),
[Forza cars](https://holdi601.github.io/3DHeat-Ext-Forza/forza-cars.html).

## Terms

Forza Horizon and Forza Motorsport belong to Microsoft, who do not endorse this
project. Nothing of the games is in this repository or downloaded by it; the
courses and cars come out of your own install, and what the tool writes is
yours to view, not to share
([Terms and licence](https://holdi601.github.io/3DHeat-Ext-Forza/terms.html)).

## Tests

```bash
python -m pip install -e .[test]
python -m pytest
```

On made-up data: archives, models, textures and whole track folders are written
by the tests. A few also read an installed Forza when there is one, and skip
when there is not.

## Licence

MIT ([`LICENSE`](LICENSE)). Third-party software it uses: [`LICENSES.md`](LICENSES.md).
