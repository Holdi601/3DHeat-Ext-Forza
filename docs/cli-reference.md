---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each command step by step.

## `heat3d-forza-maps`

```text
usage: heat3d-forza-maps [-h] [--version]
                         {identify,list,extract,course,courses,races,cars,terrain} ...

Courses, races and cars out of an installed Forza (Horizon or Motorsport, the
ForzaTech engine) for the 3DHeat viewer.

positional arguments:
  {identify,list,extract,course,courses,races,cars,terrain}
    identify            say what a Forza file is (a .minizip archive or a ForzaTech
                        model)
    list                list what is inside a .minizip archive
    extract             write one entry of a .minizip archive to disk
    course              export the ground around a lap, working out the rest
    courses             export every course in a recorded lap library, one file each
    races               every race an installed Forza defines: its own assets, venues,
                        and the exports of it
    cars                every car of an installed Forza at low detail, in one file for
                        the viewer
    terrain             cut a piece of Forza terrain out, by world coordinates

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

What you point it at is subject to the game's own licence; what it writes stays on
your machine.
```

## `course`

```text
usage: heat3d-forza-maps course [-h] [--texture-size {2048,1024,512}] [--no-textures]
                                [--season {summer,autumn,winter,spring}] [--no-placed]
                                [--trees] [--detail-budget DETAIL_BUDGET] [-o OUT]
                                [--track TRACK] [--margin MARGIN]
                                [--game {forza,beamng,acrally}] [--level LEVEL]
                                [--install INSTALL]
                                lap

positional arguments:
  lap                   a lap or course: a file written by heat3d_capture, a lap or
                        course folder from a recorded library, or just a course's name

options:
  -h, --help            show this help message and exit
  --texture-size {2048,1024,512}
                        ground texture per 512 m tile, in pixels (2048 = 25 cm a
                        pixel)
  --no-textures         flat colours only: a far smaller file, and no ground detail
  --season {summer,autumn,winter,spring}
                        which season's ground maps and model textures to use
  --no-placed           terrain only: leave out kerbs, barriers, tyre walls, signs and
                        buildings
  --trees               also place trees and bushes (many triangles, and they hide the
                        road)
  --detail-budget DETAIL_BUDGET
                        a ceiling on triangles for everything placed; the costliest
                        models drop to coarser levels of detail until it fits, and
                        past that the furthest copies are left out (default: enough to
                        keep every copy, and at least 1,500,000; kerbs always stay at
                        full detail)
  -o, --out OUT         where to write the .glb (default: the course's name, in
                        $HEAT3D_LEVELS/forza/courses when that is set, else here)
  --track TRACK         the track folder, if the installed game should not be searched
                        for
  --margin MARGIN       metres of ground to keep either side of the driving (default
                        80)
  --game {forza,beamng,acrally}
                        which game the lap is from (default: what the lap file says,
                        else Forza); a BeamNG.drive or AC Rally lap is refused with
                        the tool that exports it
  --level LEVEL         accepted for heat3d-gamefiles' command line; not used for
                        Forza
  --install INSTALL     accepted for heat3d-gamefiles' command line; not used for
                        Forza
```

## `courses`

```text
usage: heat3d-forza-maps courses [-h] [--texture-size {2048,1024,512}] [--no-textures]
                                 [--season {summer,autumn,winter,spring}]
                                 [--no-placed] [--trees]
                                 [--detail-budget DETAIL_BUDGET] [-o OUT]
                                 [--library LIBRARY] [--only ONLY [ONLY ...]]
                                 [--force] [--track TRACK] [--margin MARGIN]

options:
  -h, --help            show this help message and exit
  --texture-size {2048,1024,512}
                        ground texture per 512 m tile, in pixels (2048 = 25 cm a
                        pixel)
  --no-textures         flat colours only: a far smaller file, and no ground detail
  --season {summer,autumn,winter,spring}
                        which season's ground maps and model textures to use
  --no-placed           terrain only: leave out kerbs, barriers, tyre walls, signs and
                        buildings
  --trees               also place trees and bushes (many triangles, and they hide the
                        road)
  --detail-budget DETAIL_BUDGET
                        a ceiling on triangles for everything placed; the costliest
                        models drop to coarser levels of detail until it fits, and
                        past that the furthest copies are left out (default: enough to
                        keep every copy, and at least 1,500,000; kerbs always stay at
                        full detail)
  -o, --out OUT         folder to write into (default $HEAT3D_LEVELS/forza/courses,
                        else ./courses)
  --library LIBRARY     the lap library (default: FH Companion's, under
                        %LOCALAPPDATA%)
  --only ONLY [ONLY ...]
                        just the courses whose names contain these
  --force               export again what is already there
  --track TRACK         the track folder, if not the installed game's
  --margin MARGIN       metres either side of the driving (default 80)
```

## `races`

```text
usage: heat3d-forza-maps races [-h] [-o OUT] [--library LIBRARY] [--track TRACK]
                               [--markdown MARKDOWN]

options:
  -h, --help           show this help message and exit
  -o, --out OUT        the folder `courses` writes to (default as for `courses`)
  --library LIBRARY    the lap library (default: FH Companion's)
  --track TRACK        the track folder, if not the installed game's
  --markdown MARKDOWN  also write the table here
```

## `cars`

```text
usage: heat3d-forza-maps cars [-h] [-o OUT] [--game GAME]

options:
  -h, --help     show this help message and exit
  -o, --out OUT  the file to write (default $HEAT3D_LEVELS/forza/forza.h3dcars, else
                 ./forza.h3dcars)
  --game GAME    the game's folder, if not the installed one found
```

## `terrain`

```text
usage: heat3d-forza-maps terrain [-h] [--texture-size {2048,1024,512}] [--no-textures]
                                 [--season {summer,autumn,winter,spring}]
                                 [--no-placed] [--trees]
                                 [--detail-budget DETAIL_BUDGET] -o OUT
                                 [--box X0 Z0 X1 Z1] [--route ROUTE] [--margin MARGIN]
                                 path

positional arguments:
  path                  a track folder under media/Tracks

options:
  -h, --help            show this help message and exit
  --texture-size {2048,1024,512}
                        ground texture per 512 m tile, in pixels (2048 = 25 cm a
                        pixel)
  --no-textures         flat colours only: a far smaller file, and no ground detail
  --season {summer,autumn,winter,spring}
                        which season's ground maps and model textures to use
  --no-placed           terrain only: leave out kerbs, barriers, tyre walls, signs and
                        buildings
  --trees               also place trees and bushes (many triangles, and they hide the
                        road)
  --detail-budget DETAIL_BUDGET
                        a ceiling on triangles for everything placed; the costliest
                        models drop to coarser levels of detail until it fits, and
                        past that the furthest copies are left out (default: enough to
                        keep every copy, and at least 1,500,000; kerbs always stay at
                        full detail)
  -o, --out OUT
  --box X0 Z0 X1 Z1     the region to cut, in the game's metres
  --route ROUTE         a route JSON with "bounds" {"min": [x, y, z], "max": [x, y,
                        z]}, as heat3d_capture route and laps write it; its x and z
                        extent is the region, and its positions, if it has at least
                        10, narrow it to a corridor
  --margin MARGIN       metres to add around a route, so the verge comes with the road
```

## `identify`

```text
usage: heat3d-forza-maps identify [-h] path

positional arguments:
  path

options:
  -h, --help  show this help message and exit
```

## `list`

```text
usage: heat3d-forza-maps list [-h] [--filter FILTER] [--limit LIMIT] [--key KEY] path

positional arguments:
  path             a ForzaTech .minizip (its ChunkContentsMiniZip<n>.txt beside it
                   names the entries)

options:
  -h, --help       show this help message and exit
  --filter FILTER  only paths containing this text
  --limit LIMIT
  --key KEY        accepted for the same command line as heat3d-gamefiles; a .minizip
                   needs no key
```

## `extract`

```text
usage: heat3d-forza-maps extract [-h] [--out OUT] [--key KEY] path entry

positional arguments:
  path        a ForzaTech .minizip (its ChunkContentsMiniZip<n>.txt beside it names
              the entries)
  entry       the path as list prints it (a .minizip without its manifest: #number)

options:
  -h, --help  show this help message and exit
  --out OUT
  --key KEY   accepted for the same command line as heat3d-gamefiles; a .minizip needs
              no key
```

## Output

### `.glb` parts

Ground, per 512 m terrain tile (its grid name): `ground:terrain x<X> z<Z>`, `ground:verge x<X> z<Z>`, `ground:road x<X> z<Z>`; then `water:water`, `ground:tyre marks`, `ground:markings`.

Placed and world-space models: `ground:kerbs`, `ground:venue`, `ground:plinths`, `structure:barriers`, `structure:props`, `structure:signs`, `structure:buildings`, `structure:infrastructure`, `structure:bridges`, `structure:rocks`, `structure:smashables`, `structure:trees`; a part with its own texture adds the texture's name after a space.

A race's own layer: `structure:event_<category>` (extras `{"layer": "event", "route": <id>}`); another switched-on layer: `structure:layer_<category>` (extras `{"layer": "layer"}`); a venue's own ground: `ground:venue` (extras `{"layer": "venue"}`).

### `asset.extras`

`course_format` (2), `route`, and unless `--no-placed`: `event_copies`, `event_kinds`, `hidden`, `venue`, `layers`.
