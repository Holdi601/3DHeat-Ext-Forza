---
title: Before you start
nav_order: 2
---

# Before you start

New to the command line? This page gets you from nothing to a working tool in
about ten minutes. You type commands into a window called a **terminal**, and
the tool answers with text.

## 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   **Python 3.10 or later**.
2. Run the installer. On its first screen, tick **"Add python.exe to PATH"**,
   then click **Install Now**.

You also need a Forza installed, through Steam or the Microsoft Store (Xbox
app). The tool finds it by itself.

## 2. Get the tool

- **With git:** `git clone https://github.com/Holdi601/3DHeat-Ext-Forza.git`
- **Without git:** on the [GitHub page](https://github.com/Holdi601/3DHeat-Ext-Forza),
  click the green **Code** button, then **Download ZIP**, and unpack it.

## 3. Open a terminal in the tool's folder

- In File Explorer, open the folder that holds `README.md`. Click the address
  bar, type `cmd` and press Enter. A black window opens, already in that folder.
- Or open **Windows Terminal** and go there with `cd`:

  ```
  cd "C:\Users\you\Downloads\3DHeat-Ext-Forza"
  ```

## 4. Install the tool

```
python -m pip install -e .
```

This installs the `heat3d-forza-maps` command and what it needs:
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) (the library
the readers build on), numpy, lz4 and Pillow. You should see lines ending in
`Successfully installed ...`.

Already have a GameFiles checkout and would rather not install it again? Set
`HEAT3D_GAMEFILES` to its folder; a GameFiles folder named `3DHeat-GameFiles`
beside this one is found by itself too.

## 5. Check that it works

```
heat3d-forza-maps --help
```

You should see `usage: heat3d-forza-maps [-h]` and a list of commands
(`identify`, `list`, `extract`, `course`, ...). That is success: the tool is
ready.

## 6. A first course

If you record laps with FH Companion, give `course` a course's name as the
library shows it:

```
heat3d-forza-maps course "Example Circuit"
```

Or give it a lap file (any of the shapes on
[Lap inputs](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

```
heat3d-forza-maps course lap.json -o example.glb
```

It says which track and which race it found, what the ground is made of, what
it placed on it, and ends with `wrote example.glb (... bytes)`. See
[Course export](course-export.md).

## Reading the examples

- `<something>` is a **placeholder**: type your own value instead, without the
  angle brackets. `<lap file>` becomes, for example, `laps\my_lap.json`.
- `[--option]` in square brackets is **optional**: leave it out if you don't need it.
- A path with spaces needs **double quotes**: `"C:\My Games\lap.json"`.

## When something goes wrong

| You see | What to do |
|---|---|
| `'python' is not recognized` | Python is not installed, or "Add to PATH" was not ticked. Run the installer again and tick it, then open a new terminal. |
| `'heat3d-forza-maps' is not recognized` | Step 4 was skipped, or ran in another Python. Run it again; `python -m heat3d_ext_forza --help` works from the tool's folder either way. |
| `heat3d-forza-maps needs 3DHeat GameFiles: ...` | GameFiles is not installed. Run step 4 again, or set `HEAT3D_GAMEFILES` to a GameFiles folder. |
| `heat3d-forza-maps needs Pillow: ...` (or lz4, numpy) | Run the `pip install` the line names. |
| `no installed Forza track found` | The game is not in a Steam library or `C:\XboxGames`. Pass its track folder with `--track` ([How a Forza course is made](course-forza-horizon.md#finding-the-installed-game)). |
| `none of the installed tracks (...) has terrain at x ..., z ...` | The lap is from a game or map that is not installed. |
| `can't open file` / `not found` with a path | The path has spaces and no quotes, or a typo. Put it in double quotes. |

More messages and their fixes:
[Troubleshooting](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html)
on the GameFiles site.
