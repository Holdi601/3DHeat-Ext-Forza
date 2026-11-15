---
title: Commands
nav_order: 3
---

# Commands

Every command runs as `heat3d-forza-maps <command> ...` (or, from the tool's
folder without installing it, `python -m heat3d_ext_forza <command> ...`).

| Command | Takes | Does |
|---|---|---|
| [`course`](#course) | a lap | exports the course around it |
| [`courses`](#courses) | a recorded lap library | runs `course` on every course in it |
| [`races`](#races) | an installed Forza | lists every race the game defines: what it adds, what it hides, venues, the state of its export |
| [`terrain`](#terrain) | a Forza track folder | cuts a region by world coordinates |
| [`cars`](#cars) | an installed Forza | every car at low detail, in one file for the viewer's Race analysis tab |
| [`identify`](#identify) | a file | says whether it is a Forza `.minizip` or ForzaTech model, and what is in it |
| [`list`](#list) | a `.minizip` | lists its entries |
| [`extract`](#extract) | a `.minizip` | writes one entry to disk |

**Reading the examples:** `<x>` means replace it with your own value, without the
angle brackets; `[...]` is optional; wrap a path with spaces in "double quotes",
for example `"C:\Games\My Game"`. New to this? See [Before you start](before-you-start.md).
The full `--help` of every command is on the [Command reference](cli-reference.md).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) runs this tool
with your arguments unchanged for its own `course`, `courses`, `races`, `cars`
and `terrain` on a Forza lap or track, and asks its `identify`, `list` and
`extract` for the Forza files its own readers do not know. That is why `course`
also takes GameFiles' `--level` and `--install`, and `list` and `extract` take
`--key`: they are accepted and not used.

Each time the program starts, it may check for a newer release first.
`HEAT3D_NO_UPDATE=1` turns that check off.

Source: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | done |
| 1 | the work failed: an unreadable lap, a lap with no driving, no terrain under the driving, a course in `courses` that failed, a `.minizip` that cannot be read or whose name list does not belong to it, an entry not in the archive |
| 2 | nothing to read, or bad arguments: no Forza installed, no track under the driving, no lap library, a lap from another game, not a Forza file, a path that does not exist, a missing dependency (GameFiles, numpy, lz4, Pillow), `terrain` given both or neither of `--box` and `--route`, an argument argparse refuses |

Every failure is one line (or two) on standard error, saying what to do, not a
Python traceback.

---

## course

```
heat3d-forza-maps course <lap> [-o FILE] [options]
```

This exports the course around a lap: the ground in a band either side of the
driving, and what stands on it, as one `.glb`. It works out the rest itself:
where the game is installed, which of its tracks the lap was driven on, and
which of the game's races. See [Course export](course-export.md).

`<lap>` can be any of the following (details in
[Lap inputs](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

- a lap file: route JSON, FH Companion lap JSON, `heat3d-lap` JSON, `.npz`, or `.csv` with x, y, z columns
- a folder of lap files, searched recursively (a whole recorded course)
- a course **name**, looked up in the FH Companion library at `%LOCALAPPDATA%\FHCompanion\laps`

### Options

| Option | Default | Meaning |
|---|---|---|
| `-o`, `--out FILE` | `<course name>.glb` in the current folder, or in `$HEAT3D_LEVELS/forza/courses/` when that is set | where to write; the name is lower-cased, with runs of other characters turned into `_` |
| `--margin M` | 80 | metres of ground kept either side of the driving |
| `--texture-size {2048,1024,512}` | 2048 | ground texture pixels per 512 m tile (2048 = 25 cm a pixel) |
| `--no-textures` | off | flat colours only: a far smaller file. This also skips the road/verge split |
| `--season {summer,autumn,winter,spring}` | summer | which season's ground maps and model textures |
| `--no-placed` | off | terrain only: no kerbs, barriers, signs, buildings |
| `--trees` | off | also place trees, bushes and smashables |
| `--detail-budget N` | automatic | a ceiling on triangles for everything placed; see [Levels of detail and the budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html) |
| `--track DIR` | searched | the track folder (under `media\Tracks`, holding `GeoChunk0.minizip`) if the installed game should not be searched |
| `--game {forza,beamng,acrally}` | what the lap file says, else `forza` | which game the lap is from (see below) |
| `--level`, `--install` | | accepted for GameFiles' command line, not used |

### Which game

The game is taken from `--game`, then from the `game` field of a `heat3d-lap`
file (or of a CSV's `# {...}` description line), then defaults to Forza. A
folder gets the game its files name, when they name only one; a file that names
none (an FH Companion lap, `course.json`, a CSV without a description line)
does not count.

| Value | What happens |
|---|---|
| starts with `forza` | the Forza export |
| `beamng` | refused, exit code 2: `export it with heat3d-beamng-maps course` |
| `assetto-corsa-rally` or `acrally` | refused, exit code 2: `export it with heat3d-acrally-maps course` |
| `assetto-corsa-evo` | refused: "keeps all its content in one package obfuscated with a key, and this tool recovers none" |
| `iracing` | refused: "tracks ship in a protected format that is not a file-extraction target" |
| anything else | refused: "there is no course reader for <game> yet" |

The last three also suggest the alternatives: reconstruct the course from
gameplay (3DHeat GameCapture), or analyse the laps without a course, because the
viewer's Race analysis tab draws a road from them.

### Examples

```
# A course from the FH Companion library, by name
heat3d-forza-maps course "Example Circuit"

# One lap file, a narrower band, a smaller file
heat3d-forza-maps course lap.json -o example.glb --margin 40 --texture-size 1024

# Winter textures, trees included
heat3d-forza-maps course "Example Circuit" --season winter --trees

# A hard ceiling of 500,000 placed triangles
heat3d-forza-maps course lap.json --detail-budget 500000

# A track folder given directly (game installed somewhere it is not searched)
heat3d-forza-maps course lap.json --track "D:\Games\<Forza>\media\Tracks\<map>"
```

What a run prints, on a made-up track the tests build (on a real track the
numbers run to hundreds of thousands of triangles, and it says which track and
race it found):

![course run on a made-up track](assets/img/course-run.svg)

## courses

```
heat3d-forza-maps courses [-o FOLDER] [options]
```

This runs `course` on every course folder in a recorded lap library, writing one
`<name>.glb` each.

| Option | Default | Meaning |
|---|---|---|
| `-o`, `--out FOLDER` | `courses`, or `$HEAT3D_LEVELS/forza/courses` when that is set | the folder to write into (created if missing) |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | the lap library |
| `--only TEXT [TEXT ...]` | all | only the courses whose folder names contain one of these (case-insensitive) |
| `--force` | off | export again what already has a `.glb` |
| `--track DIR` | searched | as for `course` |
| `--margin M` | 80 | as for `course` |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | as for `course` |

What counts as a course folder: a direct sub-folder of the library whose name
contains ` (course_`, which is how FH Companion names them, for example
`Example Circuit (course_1200_3400_to_1175_3400)`. The part from ` (course_` on is
dropped from the name.

How a run behaves:

- A course whose `.glb` already exists is skipped (`kept`) unless `--force` is given, so an interrupted run carries on where it stopped.
- A `.glb` written by an older version, without the race's own layer and venues (its `asset.extras.course_format` is missing or lower than the current one), is exported again, as if `--force` were given for it alone.
- Two course folders with the same name before ` (course_` (a recorder that named a new course after an old one) do not overwrite each other: the folder created first keeps `<name>.glb`, the other is written as `<name>_<start>.glb`, `<start>` being where it starts, minus signs as `m` (for example `example_circuit_m120_m340.glb`).
- A course that fails (unreadable laps, out of memory, no terrain...) is reported as `FAILED`, and the run continues.
- At the end it prints a table of status, size in MB, seconds taken and name, then `<n> of <total> courses in <folder>`.
- The exit code is 1 if any course failed, 2 if there is no lap library.

```
heat3d-forza-maps courses -o courses --only circuit sprint --texture-size 1024
```

## races

```
heat3d-forza-maps races [-o FOLDER] [--markdown FILE] [options]
```

Lists every race an installed Forza defines, from its route definitions (see
[How a Forza course is made](course-forza-horizon.md#which-race)), and checks
the exports in a `courses` folder against them. It reads the game and the lap
library; it writes nothing but the optional table.

| Option | Default | Meaning |
|---|---|---|
| `-o`, `--out FOLDER` | as for `courses` | the folder `courses` writes to, whose files are checked |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | the lap library |
| `--track DIR` | searched | the track folder, if not the installed game's |
| `--markdown FILE` | none | also write the table there, as Markdown |

One row per race, and one per recorded course driven on it:

| Column | Meaning |
|---|---|
| route | the route id |
| course | the recorded course matched to it, if any |
| own assets | copies the race adds to the free-roam world |
| drawn | of those, copies whose model the track ships |
| kinds | the added copies by kind (barriers, props, decals, infrastructure, ...) |
| not geometry | spectator markers and collision splines, counted |
| hidden | free-roam objects the race removes |
| venue | the venue ground models the race's AI line passes within 10 m of |
| export | `current`, `older format` (exported again by `courses`), `not exported`, or empty for a race with no recorded course |

It ends with a count: `<n> races: <a> with assets of their own, <v> through a
venue, <d> driven in the lap library, <s> recorded courses to export again`.

```
heat3d-forza-maps races -o courses --markdown races.md
```

## terrain

```
heat3d-forza-maps terrain <track folder> -o FILE (--box X0 Z0 X1 Z1 | --route FILE) [options]
```

This is the cut with everything spelled out by hand: you give the track folder
and a region, not a lap. It is useful when the area you want is a box rather
than a drive.

| Option | Default | Meaning |
|---|---|---|
| `<path>` | required | a Forza track folder under `media\Tracks` (holding `GeoChunk*.minizip`) |
| `-o`, `--out FILE` | required | the `.glb` to write |
| `--box X0 Z0 X1 Z1` | | the region, in the game's metres (x and z, as the telemetry reports them); corners in any order |
| `--route FILE` | | a route JSON with `"bounds": {"min": [x, y, z], "max": [x, y, z]}`, as `heat3d_capture route` and `heat3d_capture laps` write it; read as UTF-8, with or without a byte-order mark |
| `--margin M` | **100** | metres added around a route's bounds, and the corridor width when the route has a line |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | as for `course` |

Give exactly one of `--box` and `--route`, otherwise the exit code is 2. With
`--route`, the cut is the route's `bounds` (`min`/`max`, x and z) widened by the
margin. If the file also holds at least 10 positions, the cut narrows to a
corridor of `--margin` metres around them, and placed models get their detail by
distance to that line. With `--box`, the whole box is kept, and detail goes to
what stands nearest the middle of the box.

Height is never part of the cut. A box outside the map, or in the sea, gives
"no terrain there" (exit code 1), not an error about coordinates.

```
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --box 0 0 512 512 -o piece.glb
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --route route.json -o map.glb
```

## cars

```
heat3d-forza-maps cars [-o FILE] [--game FOLDER]
```

Every car of an installed Forza at the game's own low detail, in one file for
the viewer's race tab. Takes seconds and writes about 5 MB. See
[Forza cars](forza-cars.md).

## identify

```
heat3d-forza-maps identify <path>
```

Reads the file and says what it is, by its bytes, not its extension: a
ForzaTech `.minizip` archive (the `PGZP` magic: version, entry and segment
counts, and whether the `ChunkContentsMiniZip<n>.txt` naming its entries is
beside it) or a ForzaTech model, `.modelbin` (version, chunk count, the most
common chunk tags). Anything else exits with code 2 and
`<file>: not a Forza file` on standard error. See
[Inspecting Forza files](inspecting-files.md).

## list

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

| Option | Default | Meaning |
|---|---|---|
| `<.minizip>` | required | a ForzaTech `.minizip`, such as a track's `GeoChunk0.minizip` |
| `--filter TEXT` | none | only paths containing TEXT, case-insensitive |
| `--limit N` | 50 | print at most N entries (the total count is always printed) |
| `--key HEX` | none | accepted, not used: a `.minizip` is not encrypted |

Each line shows the uncompressed size, the compression (`lz4`, `deflate` or
`stored`) and the path, as the name list beside the archive spells it.

## extract

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

| Option | Default | Meaning |
|---|---|---|
| `<entry>` | required | the path exactly as `list` prints it, or `#<number>` |
| `--out FILE` | the entry's file name (after the last `/` or `\`), in the current folder | where to write; parent folders are created |
| `--key HEX` | none | accepted, not used |

## Environment variables

| Variable | Effect |
|---|---|
| `HEAT3D_LEVELS` | one folder for every export made without `-o`: courses in `<HEAT3D_LEVELS>/forza/courses/`, the car pack in `<HEAT3D_LEVELS>/forza/`. Unset, they go in the current folder |
| `HEAT3D_GAMEFILES` | a 3DHeat GameFiles folder, when GameFiles is not installed with pip |
| `HEAT3D_NO_UPDATE` | any value other than empty, `0`, `false`, `no` turns the update check off |
| `LOCALAPPDATA` | where the FH Companion library and the update cache are looked for |
| `HEAT3D_COURSE` | tests only: the course the installed-game kerb test uses; see [Maintaining](maintaining.md#tests) |
