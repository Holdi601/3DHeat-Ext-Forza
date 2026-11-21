"""
The standalone app's description of this tool (app/spec.py): the Forza
install it reads, the recorded courses as its maps (a course is exported from
its laps alone, the ground around the driving cut out of the install; a new
course, new laps on one or a game update are found by app/manifest.py), and a
single lap, the cars and the catalogue as tasks.
`python -m heat3d_ext_forza.standalone_spec` runs the app from a checkout; the
release executables run the same.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import Check, GameSpec, Input, MapSource, Spec, Task

#: The lap files a course is read from (lapinput.read_folder); `course.json` is metadata.
LAP_SUFFIXES = (".json", ".npz", ".csv")


def _gamefiles() -> bool:
    from ._gamefiles import find

    return find()


def _game_of(p: Path) -> Path | None:
    """A Forza game folder (it holds `media/Tracks`) from it, its Store `Content` folder or what is above it."""
    for g in (p, p / "Content", p.parent, p.parent.parent):
        if (g / "media" / "Tracks").is_dir():
            return g
    return None


def _find(given: str | None) -> Path | None:
    if given:
        return _game_of(Path(given).expanduser())
    if not _gamefiles():
        return None
    from .forzainstall import game_folders, track_folders

    commons = tuple(lib / "steamapps" / "common" for lib in paths.steam_libraries())
    games = game_folders(commons)
    with_tracks = [g for g in games if track_folders((g.parent,), defaults=False)]
    return (with_tracks or games or [None])[0]


def library() -> Path | None:
    """The recorded lap library (FH Companion's), when there is one."""
    if not _gamefiles():
        return None
    from heat3d_gamefiles.lapinput import UnreadableLap, default_library

    try:
        lib = default_library()
    except UnreadableLap:
        return None
    return lib if lib.is_dir() else None


def _track_manifests(game: Path) -> list[Path]:
    """Each track's entry lists (`ChunkContentsMiniZip<n>.txt`): small, and changed by a game update."""
    tracks = game / "media" / "Tracks"
    try:
        return sorted(p for p in tracks.glob("*/ChunkContentsMiniZip*.txt") if p.is_file())
    except OSError:
        return []


def _maps(game: Path) -> list[MapSource]:
    lib = library()
    if lib is None:
        return []
    from .cli import _course_files

    courses = sorted(p for p in lib.iterdir() if p.is_dir() and " (course_" in p.name)
    shared = _track_manifests(game)
    out = []
    for course, target in _course_files(courses, Path("courses")):
        laps = sorted(p for p in course.rglob("*") if p.suffix.lower() in LAP_SUFFIXES
                      and p.name != "course.json" and p.is_file())
        if laps:
            out.append(MapSource(target.stem, course.name.split(" (course_")[0], [*laps, *shared]))
    return out


def _extract(game: Path, m: MapSource, out: Path, log) -> list[Path]:
    from . import cli

    folder = m.sources[0]
    lib = library()
    # The course's own folder: the one under the library that holds its first lap.
    course = next((p for p in folder.parents if lib is not None and p.parent == lib), folder.parent)
    target = out / "courses" / f"{m.id}.glb"
    target.parent.mkdir(parents=True, exist_ok=True)
    # The `course` verb, as typed: a lap (here a course's laps) is all it needs.
    code = cli._run(cli._parser().parse_args(["course", str(course), "-o", str(target)]))
    if code != 0 or not target.is_file():
        raise RuntimeError(f"heat3d-forza-maps course exited {code}")
    return [target]


_BUILD = re.compile(r'"buildid"\s*"(\d+)"')


def _build(game: Path) -> str | None:
    """Steam's build id of the install, from its own app manifest; None for other stores."""
    library_root = game.parent.parent.parent  # <lib>/steamapps/common/<game>
    appid = paths.steam_app_id(library_root, game.name)
    if not appid:
        return None
    try:
        text = (library_root / "steamapps" / f"appmanifest_{appid}.acf").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = _BUILD.search(text)
    return m.group(1) if m else None


def _checks(found: dict, levels: Path) -> list[Check]:
    from ._gamefiles import MISSING

    ok = _gamefiles()
    checks = [Check("gamefiles", "3DHeat GameFiles (the library the readers are built on)", ok,
                    "found" if ok else MISSING)]
    lib = library()
    checks.append(Check(
        "laps", "Recorded laps (a course is exported from its laps)", lib is not None,
        str(lib) if lib else "no lap library found; courses come from laps recorded with FH Companion. "
                            "A single lap file can be exported with Export a lap.",
    ))
    return checks


SPEC = Spec(
    id="heat3d-forza",
    name="3DHeat Forza",
    repo="Holdi601/3DHeat-Ext-Forza",
    version=__version__,
    tools={"heat3d-forza-maps": "heat3d_ext_forza.cli:main"},
    default_tool="heat3d-forza-maps",
    description="Forza courses, races and cars for the 3DHeat viewer",
    module="heat3d_ext_forza.standalone_spec",
    games=[GameSpec(
        key="forza", label="Forza", find=_find, subdir="forza", build=_build,
        maps=_maps, extract=_extract,
        existing_outputs=lambda out, m: [out / "courses" / f"{m.id}.glb"],
        output_version="1.0.0",
        platforms=("windows-x64", "linux-x64"),
    )],
    checks=_checks,
    tasks=[
        Task(
            "course", "Export a lap",
            [Input("lap", "A lap or course file", "file")],
            lambda v, levels: ["heat3d-forza-maps", "course", v["lap"]],
            help="the ground around one lap, into the levels folder's forza/courses",
        ),
        Task(
            "cars", "Cars (one file for the viewer)", [],
            lambda v, levels: ["heat3d-forza-maps", "cars"],
            help="forza.h3dcars in the levels folder's forza folder, from your install; it stays on this machine",
        ),
        Task(
            "catalog", "Car catalogue", [],
            lambda v, levels: ["heat3d-forza-maps", "catalog"],
            help="catalog.json in the levels folder's forza folder",
        ),
    ],
    min_free_gb=5.0,
    notice="Not affiliated with or endorsed by Microsoft.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
