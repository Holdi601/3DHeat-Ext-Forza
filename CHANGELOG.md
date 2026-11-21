# Changelog

## 1.1.0

- A standalone program for Windows and Linux (no Python needed), built by CI with a `SHA256SUMS` file. Without
  arguments it opens a window: what is found and what is missing (install, recorded laps, disk space), the levels
  folder, the recorded courses as new / with new laps or a game update / exported by an older version / up to
  date, export of the picked ones one at a time (`forza/courses/<course>.glb`, each from its laps alone), a single
  lap's export, the cars, the catalogue, and updates.
- Each exported course is recorded in `<levels>/forza/.heat3d-extract.json` (extractor version, game build, size
  and SHA-256 of its laps and of the tracks' entry lists), so new courses, new laps and game updates are found
  and only those exported: `status --json`, `extract --new` / `--changed` / `--outdated` / `<course>...`,
  `--progress-json`.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).
- The install is also found in Steam libraries on Linux (native, flatpak, Steam Deck).
- `catalog`: the car catalogue for the viewer (`catalog.json`, format
  `3dheat-catalog`): every car archive's number, make, model and year, joined
  with FH Companion's car list (name, stock class and index, type, country) and
  the lap headers (drivetrain, cylinders, power and class as driven).

## 1.0.0

- First version of its own, moved out of 3DHeat GameFiles with its history
  (GameFiles' `course`, `courses`, `races`, `cars` and `terrain` now run this
  tool for a Forza lap or track): the ForzaTech readers (`.minizip`,
  `.modelbin`, swatches, placement files, materials, routes, cars), the course
  export and the Forza commands, with the same options and output files as in
  GameFiles. The glTF writer, lap readers, corridor, ground kinds and detail
  budget come from GameFiles as a library.
- `course` refuses a BeamNG.drive or Assetto Corsa Rally lap with the tool that
  exports it (exit code 2), and takes GameFiles' `--level` and `--install`
  without using them.
- `identify` exits 2 with `not a Forza file` for anything that is neither a
  `.minizip` nor a ForzaTech model; `list` and `extract` take a `.minizip` (and
  accept GameFiles' `--key`).
- No installed Forza, no lap library, a missing dependency: exit code 2 and one
  line saying what to do.
- A Microsoft Store install is named by its game folder, not `Content`.
- Installs with one pip line from the release zip, no Git needed (GameFiles comes from its own release zip); a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Forza](https://holdi601.github.io/3DHeat-Ext-Forza/)):

| Feature | Page |
|---|---|
| Installing, GameFiles, a first course | [Before you start](docs/before-you-start.md) |
| Every command, its options and exit codes; `courses`, `races`, `terrain` | [Commands](docs/commands.md) |
| `course` step by step: the corridor, the ground, what stands on it | [Course export](docs/course-export.md) |
| Finding the game, the track and the race; terrain, ground texture, placed models, the race's own layer, venues | [How a Forza course is made](docs/course-forza-horizon.md) |
| `cars` and the car file's layout | [Forza cars](docs/forza-cars.md) |
| `identify`, `list`, `extract` | [Inspecting Forza files](docs/inspecting-files.md) |
| The file formats | [ForzaTech](docs/reader-forzatech.md) |
| Microsoft's games, what the output may be used for | [Terms and licence](docs/terms.md) |
| Every option and part name, generated | [Command reference](docs/cli-reference.md) |
| Tests and the release checklist | [Maintaining these docs](docs/maintaining.md) |
