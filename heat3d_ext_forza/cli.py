"""
Command line for the Forza reader (Forza Horizon and Forza Motorsport, the
ForzaTech engine).

    heat3d-forza-maps course   <lap> [-o map.glb]
    heat3d-forza-maps courses  [-o folder] [--only name ...]
    heat3d-forza-maps races    [--markdown table.md]
    heat3d-forza-maps cars     [-o forza.h3dcars]
    heat3d-forza-maps terrain  <forza track folder> -o map.glb
                               (--box x0 z0 x1 z1 | --route route.json)
    heat3d-forza-maps identify <path>
    heat3d-forza-maps list     <.minizip> [--filter text] [--limit n]
    heat3d-forza-maps extract  <.minizip> <entry> [--out file]

`course` is the one to reach for: give it a lap and it exports the ground around
it. It works out where the game is installed, which of its tracks the lap was
driven on, which of the game's own routes it follows, and what to cut, so the
only thing anyone has to know is which lap they mean. `courses` does that for
every course in a recorded library. `terrain` is the same cut with all of that
spelled out by hand, for when the answer is a box rather than a drive.

`identify`, `list` and `extract` take the game's own files: a `.minizip`
archive (with the `ChunkContentsMiniZip<n>.txt` beside it naming its entries)
and the ForzaTech models inside one.

Exit status: 0 done, 1 failed, 2 nothing to read (no Forza installed, no lap
library, no track under the driving, not a Forza file, a missing dependency).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__

PROG = "heat3d-forza-maps"

#: The tools that export the courses of the other games a lap can come from.
OTHER_TOOLS = {
    "beamng": ("BeamNG.drive", "heat3d-beamng-maps"),
    "assetto-corsa-rally": ("Assetto Corsa Rally", "heat3d-acrally-maps"),
    "acrally": ("Assetto Corsa Rally", "heat3d-acrally-maps"),
}


def _identify(path: Path) -> list[str] | None:
    """What a Forza file is, read from its bytes; None when it is none of them."""
    from .forzatech import UnsupportedForza, read_model
    from .minizip import MAGIC as MINIZIP_MAGIC

    lines = [f"{path.name}  ({path.stat().st_size:,} bytes)"]
    if _head(path, 4) == MINIZIP_MAGIC:
        return lines + _identify_minizip(path)
    try:
        model = read_model(path)
    except UnsupportedForza:
        return None
    lines.append(f"  ForzaTech model, version {model.version}")
    lines.append(f"    chunks     {len(model)}")
    lines.append(
        "    holds      "
        + ", ".join(f"{n}x{t}" for t, n in list(model.counts().items())[:6])
    )
    lines.append("    note       chunk contents are not decoded")
    return lines


def _head(path: Path, size: int) -> bytes:
    with path.open("rb") as handle:
        return handle.read(size)


def _identify_minizip(path: Path) -> list[str]:
    from .minizip import Contents, MiniZip, UnsupportedMiniZip, manifest_of

    try:
        archive = MiniZip(path)
    except UnsupportedMiniZip as exc:
        return ["  ForzaTech .minizip archive, but not one this reads", f"    {exc}"]
    with archive:
        lines = [
            f"  ForzaTech .minizip archive, version {archive.version}",
            f"    entries    {archive.count:,} in {archive.segments:,} segments",
        ]
    manifest = manifest_of(path)
    if manifest is not None and manifest.exists():
        names = len(Contents(manifest))
        disagree = (
            f" - {names:,} names for {archive.count:,} entries, so they do not belong together"
            if names != archive.count
            else ""
        )
        lines.append(f"    names      {manifest.name}{disagree}")
    else:
        # The archive stores no names; without the manifest an entry is a number.
        lines.append("    names      no manifest beside it, so entries go by number (#0, #1, ...)")
    return lines


class _Listing:
    """
    What `list` and `extract` need of an archive: its entry names, and for
    each its size, how it is stored, and its bytes.
    """

    def __init__(self, names) -> None:
        self.names = sorted(names)
        self._known = set(self.names)

    def list(self, pattern: str | None = None) -> list[str]:
        if not pattern:
            return list(self.names)
        needle = pattern.lower()
        return [n for n in self.names if needle in n.lower()]

    def __contains__(self, name: str) -> bool:
        return name in self._known

    def describe(self, name: str) -> tuple[int, str]:
        raise NotImplementedError

    def read(self, name: str) -> bytes:
        raise NotImplementedError

    def close(self) -> None:
        pass


class _MiniZipListing(_Listing):
    """
    A `.minizip`, by the names in the manifest beside it, or by entry number
    (`#12`) where there is none. The number works either way.
    """

    CODECS = {0x00: "stored", 0x08: "deflate", 0x1F: "lz4"}

    def __init__(self, path: Path) -> None:
        from .minizip import Contents, MiniZip, UnsupportedMiniZip, manifest_of

        self.archive = MiniZip(path)
        manifest = manifest_of(path)
        if manifest is not None and manifest.exists():
            names = Contents(manifest).names
            if len(names) != self.archive.count:
                self.archive.close()
                raise UnsupportedMiniZip(
                    f"{manifest.name} names {len(names):,} entries but {path.name} holds "
                    f"{self.archive.count:,}; the two do not belong together"
                )
        else:
            names = [f"#{i}" for i in range(self.archive.count)]
        self._index: dict[str, int] = {}
        for number, name in enumerate(names):
            self._index.setdefault(name, number)
        super().__init__(self._index)

    def _number(self, name: str) -> int | None:
        if name in self._index:
            return self._index[name]
        if name.startswith("#") and name[1:].isdigit() and int(name[1:]) < self.archive.count:
            return int(name[1:])
        return None

    def __contains__(self, name: str) -> bool:
        return self._number(name) is not None

    def describe(self, name):
        entry = self.archive.entry(self._number(name))
        return entry.size, self.CODECS.get(entry.codec, f"unknown({entry.codec})")

    def read(self, name):
        return self.archive.read(self._number(name))

    def close(self) -> None:
        self.archive.close()


def _reader_errors() -> tuple[type[BaseException], ...]:
    """Everything reading a `.minizip` raises to say it cannot be read."""
    import struct

    from .minizip import UnsupportedMiniZip

    return (UnsupportedMiniZip, struct.error, OSError)


def _write_course(
    out, track, target, args, low, high, route=None, corridor=None, route_id=None, route_assets=None
) -> Path:
    """
    Bake, place, plan and write: the part of an export both verbs share.

    Textures are baked per tile from the track's own maps unless turned off,
    and a tile whose maps are missing falls back to flat colour rather than
    failing the export - detail is optional, geometry is not. The same goes for
    placed models: kerbs, barriers and the rest are added from the track's
    placement files, each with its own texture where the game gives it one,
    and with the detail going to what stands nearest `route`, the driving.
    """
    import numpy as np

    from heat3d_gamefiles.glb import Part, compute_normals, write_glb

    from .courseexport import bake_tiles, lift_decals, plan_parts, planar_uvs

    images = {}
    if not args.no_textures and out.tile_keys:
        images = bake_tiles(
            track, out.tile_keys, size=args.texture_size, season=args.season
        )
        missing = len(out.tile_keys) - len(images)
        note = f", {missing} without maps" if missing else ""
        print(
            f"\n  baked {len(images)} ground textures at {args.texture_size} px "
            f"({512 / args.texture_size * 100:.0f} cm a pixel){note}"
        )

    plan = plan_parts(out, images)
    total = sum(plan.counts.values())
    print("\n  what the ground is made of:")
    for label, many in sorted(plan.counts.items(), key=lambda kv: -kv[1]):
        print(f"    {many:9,} triangles  {many / total:5.1%}  {label}")

    ground_normals = out.normals if out.normals is not None else compute_normals(out.positions, out.faces)
    parts, decal_positions, decal_normals = lift_decals(plan.parts, out.positions, ground_normals)
    positions = [out.positions, decal_positions]
    normals = [ground_normals, decal_normals]
    uvs = [
        planar_uvs(out) if plan.textured else np.zeros((len(out.positions), 2), np.float32),
        np.zeros((len(decal_positions), 2), np.float32),
    ]
    textured = plan.textured
    if not args.no_placed:
        from .forzaplacement import DEFAULT_CATEGORIES, VEGETATION, place_in_track

        categories = DEFAULT_CATEGORIES + (VEGETATION if args.trees else ())
        placed = place_in_track(
            track,
            low,
            high,
            categories=categories,
            budget=args.detail_budget,
            season=args.season,
            textures=not args.no_textures,
            route=route,
            corridor=corridor,
            route_id=route_id,
            route_assets=route_assets,
        )
        if placed.parts:
            print(
                f"\n  placed on it ({placed.triangles():,} triangles of a "
                f"{placed.budget:,} budget, {len(placed.textures)} textures):"
            )
            print(placed.summary())
        offset = len(out.positions) + len(decal_positions)
        for name, mesh in sorted(placed.parts.items()):
            positions.append(mesh.positions)
            normals.append(mesh.normals)
            uvs.append(mesh.uvs if mesh.uvs is not None else np.zeros((len(mesh.positions), 2), np.float32))
            texture = placed.textures.get(mesh.texture) if mesh.texture else None
            textured = textured or texture is not None
            layer = _layer_extras(name.split(" ")[0], route_id)
            parts.append(
                Part(
                    name=name,
                    faces=mesh.faces + offset,
                    colour=None if texture is not None else mesh.colour,
                    texture=texture,
                    extras=layer,
                )
            )
            offset += len(mesh.positions)

    about = {"course_format": COURSE_FORMAT, "route": route_id}
    if not args.no_placed:
        about.update(
            event_copies=sum(placed.event.values()),
            event_kinds=sorted(placed.event),
            hidden=placed.hidden,
            venue=sorted(placed.venue),
            layers=sorted(placed.layers),
        )
    written = write_glb(
        target,
        np.concatenate(positions),
        parts=parts,
        normals=np.concatenate(normals),
        uvs=np.concatenate(uvs).astype(np.float32) if textured else None,
        extras=about,
    )
    print(f"\nwrote {written} ({written.stat().st_size:,} bytes)")
    return written


#: What a Forza course file holds, as its glTF `asset.extras.course_format`
#: says: 2 adds the race's own layer, a venue's ground and the world-space
#: models. `courses` re-exports a file older than this.
COURSE_FORMAT = 2


def course_format(path: Path) -> int:
    """The `course_format` a course file was written with; 0 if it does not say."""
    import json
    import struct

    try:
        with open(path, "rb") as handle:
            head = handle.read(20)
            if len(head) < 20 or head[:4] != b"glTF":
                return 0
            (length,) = struct.unpack_from("<I", head, 12)
            document = json.loads(handle.read(length))
    except (OSError, ValueError):
        return 0
    return int(document.get("asset", {}).get("extras", {}).get("course_format", 0))


def _layer_extras(part: str, route_id) -> dict | None:
    """
    What a part is, for a viewer that switches layers on and off: the race's
    own layer (`event`), another switched-on layer (`layer`) or a venue's own
    ground (`venue`). The free-roam world carries nothing.
    """
    from .forzaplacement import EVENT_PART, LAYER_PART, VENUE_PART

    if part.startswith(EVENT_PART.format("")):
        return {"layer": "event", "route": route_id}
    if part.startswith(LAYER_PART.format("")):
        return {"layer": "layer"}
    if part == VENUE_PART:
        return {"layer": "venue"}
    return None


def _course(args) -> int:
    """
    A lap in, the ground around it out.

    Everything between those two is derivable and so is derived: where the
    game is installed, which of its tracks these coordinates belong to, and
    what to cut. The alternative is a command line carrying a forty-character
    path to a folder inside a game someone already has installed, which nobody
    should have to look up to export a corner of a racetrack.
    """
    from heat3d_gamefiles import levelshome
    from heat3d_gamefiles.lapinput import UnreadableLap, read

    try:
        driven = read(args.lap)
    except UnreadableLap as exc:
        print(exc, file=sys.stderr)
        return 1
    game = (getattr(args, "game", None) or driven.game or "forza").lower()
    if game in OTHER_TOOLS:
        title, tool = OTHER_TOOLS[game]
        print(f"{driven.name} is a {title} lap, not a Forza one: export it with `{tool} course`", file=sys.stderr)
        return 2
    if not game.startswith("forza"):
        print(_no_course(game), file=sys.stderr)
        return 2
    target = args.out or levelshome.default(_slug(driven.name) + ".glb", "forza", "courses")
    target.parent.mkdir(parents=True, exist_ok=True)
    return export_course(driven, target, args)


#: Why a game's lap cannot be turned into a course from its files yet. Said
#: plainly, with the route that does work for every game.
_WHY_NOT = {
    "assetto-corsa-evo": (
        "Assetto Corsa EVO keeps all its content in one package obfuscated "
        "with a key, and this tool recovers none"
    ),
    "iracing": "iRacing's tracks ship in a protected format that is not a file-extraction target",
}


def _no_course(game: str) -> str:
    reason = _WHY_NOT.get(game, f"there is no course reader for {game} yet")
    return (
        f"no course export for this lap: {reason}.\n"
        "  Courses can be exported from Forza (this tool), BeamNG.drive (heat3d-beamng-maps) and "
        "Assetto Corsa Rally (heat3d-acrally-maps) laps. For the rest, reconstruct the course from gameplay\n"
        "  (gamecapture), or analyse the laps without one - the "
        "Race tab draws a road from them."
    )


def _slug(name: str) -> str:
    """A course name as a file name: `Example Circuit` -> `example_circuit`."""
    import re

    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "course"


def export_course(driven, target: Path, args) -> int:
    """
    Export the ground and everything on it along one course's driving.

    The cut is a corridor `args.margin` metres either side of the driven line,
    not the driving's bounding box: the same thing for a circuit, and a tenth
    of it for a point-to-point sprint, whose box is mostly hillside nobody
    drives past.
    """
    from heat3d_gamefiles.corridor import Corridor

    from .forzainstall import find_track
    from .forzaterrain import extract_from_track

    if len(driven) < 2:
        print(f"{driven.name} holds no driving", file=sys.stderr)
        return 1

    corridor = Corridor(driven.positions, args.margin)
    low, high = driven.box(args.margin)
    laps = f"{driven.laps} laps, " if driven.laps > 1 else ""
    print(
        f"{driven.name}: {laps}{len(driven):,} samples, {driven.metres:,.0f} m driven"
    )

    track = args.track
    if track is None:
        try:
            track = find_track(low, high)
        except FileNotFoundError as exc:
            print(exc, file=sys.stderr)
            return 2
        print(f"  on {track.name}, in {_game_name(track)}")

    corridor, low, high = _with_venues(track, driven, corridor, low, high, args.margin)

    from .forzaroute import match, read_routes
    from .forzaroute import route_assets as assets_of

    route, fit = match(driven.positions, read_routes(track))
    route_id = route.id if route is not None else None
    assets = assets_of(track, route_id) if route_id is not None else None
    if route is not None:
        print(f"  the game's route {route.id} (driven line within {fit:.0f} m of it)")
        if assets is not None:
            markers = ", ".join(f"{n:,} {k}" for k, n in sorted(assets.markers.items()))
            print(
                f"  its own layer: {assets.copies:,} copies of {len(assets.models)} models, "
                f"{len(assets.hidden):,} free-roam objects hidden"
                + (f"; not drawn: {markers}" if markers else "")
            )
    else:
        print("  no route of the game's matches the driving; only the free-roam world is placed")
    print(
        f"  cutting {args.margin:,.0f} m either side of the driving: "
        f"{corridor.area / 1e6:,.2f} km2 of a {high[0] - low[0]:,.0f} by "
        f"{high[1] - low[1]:,.0f} m box"
    )
    out = extract_from_track(track, low, high, corridor=corridor)
    if not len(out.faces):
        print(
            f"\nno terrain there. {track.name} has tiles nearby but none that "
            "cover the driving, which usually means the lap and the track are "
            "from different games.",
            file=sys.stderr,
        )
        return 1

    print()
    print(out.summary())
    _write_course(
        out, track, target, args, low, high, route=driven.positions, corridor=corridor,
        route_id=route_id, route_assets=assets,
    )
    return 0


def _game_name(track: Path) -> str:
    """The game a track folder is in: `<game>/media/Tracks/<track>`, or `<game>/Content/...` from the Store."""
    game = track.parents[2]
    return game.parent.name if game.name.lower() == "content" else game.name


def _with_venues(track, driven, corridor, low, high, margin):
    """
    Widen the cut to the whole of every venue the driving passes through.

    A stadium circuit uses part of its stadium's floor, and the grandstands,
    walls and barriers that make it a stadium stand around the rest of it. A
    venue is drawn whole or it is not the venue: so where the driving touches
    a site's own ground (see `forzaplacement.WORLD_REACH`), the corridor takes
    in all of that ground's footprint, and everything placed on it comes too.
    """
    import numpy as np

    from heat3d_gamefiles.corridor import Corridor

    from .forzaplacement import Track

    with Track(track) as opened:
        venues = opened.venues(low, high, corridor)
    if not venues:
        return corridor, low, high
    step = max(10.0, margin / 2)
    points = [np.asarray(driven.positions, dtype=np.float64)[:, [0, 2]]]
    for _stem, lo, hi in venues:
        xs = np.arange(lo[0], hi[0] + step, step)
        zs = np.arange(lo[2], hi[2] + step, step)
        gx, gz = np.meshgrid(xs, zs, indexing="ij")
        points.append(np.stack([gx.ravel(), gz.ravel()], axis=1))
    plane = np.concatenate(points)
    corridor = Corridor(plane, margin)
    low = (min(low[0], float(plane[:, 0].min()) - margin), min(low[1], float(plane[:, 1].min()) - margin))
    high = (max(high[0], float(plane[:, 0].max()) + margin), max(high[1], float(plane[:, 1].max()) + margin))
    names = ", ".join(sorted({stem for stem, _lo, _hi in venues})[:3])
    print(f"  through a venue ({names}): cutting all of its ground, {corridor.area / 1e6:,.2f} km2")
    return corridor, low, high


def _cars(args) -> int:
    """
    Every car of an installed Forza, at the game's own reduced quality, in one
    file for the viewer's race tab. Run it again when the game gets new cars.
    """
    from heat3d_gamefiles import levelshome

    from .forzacars import cars_of_game, read_car, write_pack
    from .forzainstall import game_folders

    if args.game:
        games = [Path(args.game)]
    else:
        games = [g for g in game_folders() if cars_of_game(g)]
    if not games:
        print("no installed Forza with cars found; name its folder with --game", file=sys.stderr)
        return 2
    game = games[-1]
    archives = cars_of_game(game)
    if not archives:
        print(f"{game} has no media/Cars folder", file=sys.stderr)
        return 2
    print(f"reading {len(archives)} cars from {game}")
    cars, without, failed = [], [], []
    for archive in archives:
        try:
            car = read_car(archive)
        except Exception as error:
            failed.append(f"{archive.name}: {error}")
            continue
        if car is None:
            without.append(archive.name)
        else:
            cars.append(car)
    out = args.out or levelshome.default("forza.h3dcars", "forza")
    out.parent.mkdir(parents=True, exist_ok=True)
    size = write_pack(cars, out, source=game.name)
    print(f"{out}: {len(cars)} cars, {size / 1e6:.1f} MB")
    if without:
        print(f"no stand-in model in {len(without)}: {', '.join(without)}")
    for line in failed:
        print(f"failed: {line}", file=sys.stderr)
    return 1 if failed else 0


def _courses(args) -> int:
    """
    Every course in a recorded lap library, one file each.

    Carries on past a course that fails, and says at the end which did; a
    course already exported is skipped unless `--force`, so a run that was
    interrupted picks up where it stopped.
    """
    import time

    from heat3d_gamefiles import levelshome
    from heat3d_gamefiles.lapinput import UnreadableLap, default_library, read

    try:
        library = Path(args.library) if args.library else default_library()
    except UnreadableLap as exc:
        print(exc, file=sys.stderr)
        return 2
    if not library.is_dir():
        print("no recorded lap library found; name one with --library", file=sys.stderr)
        return 2
    folder = Path(args.out) if args.out else levelshome.default("courses", "forza")
    folder.mkdir(parents=True, exist_ok=True)
    courses = sorted(
        p for p in Path(library).iterdir() if p.is_dir() and " (course_" in p.name
    )
    if args.only:
        wanted = [w.lower() for w in args.only]
        courses = [p for p in courses if any(w in p.name.lower() for w in wanted)]
    results = []
    for number, (course, target) in enumerate(_course_files(courses, folder), 1):
        name = course.name.split(" (course_")[0]
        if target.exists() and not args.force and course_format(target) >= COURSE_FORMAT:
            results.append((name, "kept", target.stat().st_size, 0.0))
            continue
        print(f"\n=== {number}/{len(courses)}: {name} ===")
        started = time.time()
        try:
            driven = read(course)
            status = export_course(driven, target, args)
        except (UnreadableLap, OSError, ValueError, MemoryError) as exc:
            print(f"  failed: {exc}", file=sys.stderr)
            status = 1
        took = time.time() - started
        size = target.stat().st_size if target.exists() and status == 0 else 0
        results.append((name, "written" if status == 0 else "FAILED", size, took))

    print("\n" + "-" * 72)
    for name, status, size, took in results:
        extra = f"{size / 1e6:8.1f} MB" if size else " " * 11
        timing = f"{took:6.0f} s" if took else ""
        print(f"  {status:8} {extra}  {timing:>8}  {name}")
    failed = [r for r in results if r[1] == "FAILED"]
    print(f"\n{len(results) - len(failed)} of {len(results)} courses in {folder}")
    return 1 if failed else 0


def _course_files(courses: list[Path], folder: Path) -> list[tuple[Path, Path]]:
    """
    Each recorded course and the file it is written to: its name as a file
    name. Where two courses carry one name (a recorder that named a new circuit
    after an old one), the one recorded first keeps it and the other is named
    after where it starts as well, so neither overwrites the other.
    """
    import os

    def created(course: Path) -> float:
        try:
            found = os.stat(course)
        except OSError:
            return float("inf")
        return getattr(found, "st_birthtime", found.st_ctime)

    by_slug: dict[str, list[Path]] = {}
    for course in courses:
        by_slug.setdefault(_slug(course.name.split(" (course_")[0]), []).append(course)
    target_of = {}
    for slug, group in by_slug.items():
        for rank, course in enumerate(sorted(group, key=lambda c: (created(c), c.name))):
            if rank:
                start = course.name.split("(course_", 1)[-1].split("_to_")[0]
                target_of[course] = folder / f"{slug}_{_slug(start.replace('-', 'm'))}.glb"
            else:
                target_of[course] = folder / f"{slug}.glb"
    return [(course, target_of[course]) for course in courses]


def _races(args) -> int:
    """
    Every race the installed game defines, and what each adds to the world.

    For each route the game ships a definition of: how many copies of its own
    assets it places (and how many of those the track has models for), what
    kinds they are, how many free-roam objects it hides, whether its line
    passes through a venue's own ground, which recorded course was driven on it
    and whether that course's export (in `--out`) already carries the race's
    layer. With `--markdown` the table is written there too.
    """
    import numpy as np

    from heat3d_gamefiles import levelshome

    from .forzainstall import track_folders
    from .forzaplacement import Track
    from .forzaroute import defined_routes, match, read_routes, route_assets

    tracks = [args.track] if args.track else [t for t in track_folders() if defined_routes(t)]
    if not tracks:
        print("no installed Forza with route definitions found; name its track folder with --track", file=sys.stderr)
        return 2
    track = Path(tracks[0])
    routes = {r.id: r for r in read_routes(track)}
    defined = defined_routes(track)
    print(f"{len(defined)} races defined in {_game_name(track)} ({track.name}), {len(routes)} with an AI line")

    recorded: dict[int, list[tuple[str, Path]]] = {}
    from heat3d_gamefiles.lapinput import UnreadableLap, default_library, read

    try:
        library = Path(args.library) if args.library else default_library()
    except UnreadableLap:
        library = None
    folder = Path(args.out) if args.out else levelshome.default("courses", "forza")
    if library is not None and library.is_dir():
        courses = sorted(p for p in library.iterdir() if p.is_dir() and "course_" in p.name)
        for course, target in _course_files([c for c in courses if " (course_" in c.name], folder) + [
            (c, folder / (_slug(c.name) + ".glb")) for c in courses if " (course_" not in c.name
        ]:
            try:
                driven = read(course)
            except (UnreadableLap, OSError, ValueError):
                continue
            route, _fit = match(driven.positions, list(routes.values()))
            if route is not None:
                recorded.setdefault(route.id, []).append((course.name.split(" (course_")[0], target))

    with Track(track) as opened:
        venues = [(stem, lo, hi) for stem, part, lo, hi in opened.world_models() if part.startswith("ground:venue")]
        rows = []
        for route_id in sorted(defined):
            assets = route_assets(track, route_id)
            shipped = {stem for stem in assets.models if stem in opened.clusters}
            drawn = sum(len(v) for k, v in assets.models.items() if k in shipped)
            kinds: dict[str, int] = {}
            for stem, copies in assets.models.items():
                kinds[assets.kinds[stem]] = kinds.get(assets.kinds[stem], 0) + len(copies)
            line = routes[route_id].points if route_id in routes else None
            if line is None and assets.models:
                line = np.concatenate(list(assets.models.values()))[:, :3]
            touched = []
            if line is not None and len(line):
                plane = line[:, [0, 2]]
                for stem, lo, hi in venues:
                    if ((plane[:, 0] >= lo[0] - 10) & (plane[:, 0] <= hi[0] + 10)
                            & (plane[:, 1] >= lo[2] - 10) & (plane[:, 1] <= hi[2] + 10)).any():
                        touched.append(stem)
            for name, target in recorded.get(route_id, [(None, None)]):
                exported = target is not None and target.exists()
                current = exported and course_format(target) >= COURSE_FORMAT
                rows.append(
                    dict(
                        route=route_id,
                        course=name or "",
                        copies=assets.copies,
                        drawn=drawn,
                        kinds=", ".join(f"{k} {n}" for k, n in sorted(kinds.items(), key=lambda kv: -kv[1])),
                        markers=", ".join(f"{k} {n}" for k, n in sorted(assets.markers.items())),
                        hidden=len(assets.hidden),
                        venue=", ".join(sorted(touched)),
                        export=("current" if current else "older format") if exported else ("not exported" if name else ""),
                    )
                )

    print(f"\n{'route':>6} {'copies':>7} {'drawn':>6} {'hidden':>6}  venue  export          course")
    for row in rows:
        print(
            f"{row['route']:>6} {row['copies']:>7,} {row['drawn']:>6,} {row['hidden']:>6,}  "
            f"{'yes' if row['venue'] else 'no ':5}  {row['export']:15} {row['course']}"
        )
    races = {row["route"] for row in rows}
    with_layer = {row["route"] for row in rows if row["copies"]}
    with_venue = {row["route"] for row in rows if row["venue"]}
    driven_on = {row["route"] for row in rows if row["course"]}
    stale = [row for row in rows if row["export"] in ("older format", "not exported")]
    print(
        f"\n{len(races)} races: {len(with_layer)} with assets of their own, {len(with_venue)} through a venue, "
        f"{len(driven_on)} driven in the lap library, {len(stale)} recorded courses to export again"
    )
    if args.markdown:
        lines = [
            "| route | recorded course | own assets | drawn | kinds | not geometry | hidden | venue | export |",
            "|---:|---|---:|---:|---|---|---:|---|---|",
        ]
        for row in rows:
            lines.append(
                f"| {row['route']} | {row['course']} | {row['copies']} | {row['drawn']} | {row['kinds']} | "
                f"{row['markers']} | {row['hidden']} | {row['venue'] or 'no'} | {row['export']} |"
            )
        Path(args.markdown).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {args.markdown}")
    return 0


def _route_box(path: Path, margin: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    The ground a recorded lap covers, widened a little.

    The margin is not cosmetic. A lap is a line, and a line's bounding box in the
    plane is the road and nothing either side of it — no verge, no barrier, no
    hill the road runs along. A hundred metres is enough to see what the driver
    saw.
    """
    import json

    # utf-8-sig, as `lapinput` reads JSON: a file written by a .NET tool, or
    # saved by Notepad, starts with a byte-order mark that plain utf-8 refuses.
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    box = data.get("bounds") if isinstance(data, dict) else None
    if not box:
        raise SystemExit(
            f"{path} has no bounds; --route takes a route file with "
            '"bounds": {"min": [x, y, z], "max": [x, y, z]}'
        )
    low, high = box["min"], box["max"]
    return (
        (low[0] - margin, low[2] - margin),
        (high[0] + margin, high[2] + margin),
    )


def _terrain(args) -> int:
    from .forzaterrain import extract_from_track

    if bool(args.box) == bool(args.route):
        print("give exactly one of --box and --route", file=sys.stderr)
        return 2
    route = corridor = None
    if args.route:
        from heat3d_gamefiles.corridor import Corridor
        from heat3d_gamefiles.lapinput import UnreadableLap, read_file

        low, high = _route_box(args.route, args.margin)
        try:
            route = read_file(args.route)
        except UnreadableLap:
            route = None
        # A route file that only carries its bounds is a box, not a line.
        if route is not None and len(route) >= 10:
            corridor = Corridor(route, args.margin)
    else:
        x0, z0, x1, z1 = args.box
        low, high = (min(x0, x1), min(z0, z1)), (max(x0, x1), max(z0, z1))

    span = (high[0] - low[0], high[1] - low[1])
    print(
        f"cutting {span[0]:,.0f} by {span[1]:,.0f} metres "
        f"at x {low[0]:,.0f}..{high[0]:,.0f}, z {low[1]:,.0f}..{high[1]:,.0f}"
    )
    out = extract_from_track(args.path, low, high, corridor=corridor)
    if not len(out.faces):
        print(
            "no terrain there.\n"
            "  The coordinates are the game's own metres, as its telemetry reports\n"
            "  them. A box outside the map, or in the sea, is empty rather than an\n"
            "  error.",
            file=sys.stderr,
        )
        return 1

    print(out.summary())
    _write_course(out, args.path, args.out, args, low, high, route=route, corridor=corridor)
    return 0


def _export_options(p) -> None:
    """The options `course`, `courses` and `terrain` share: what goes into the file."""
    from heat3d_gamefiles.detail import DEFAULT_BUDGET

    p.add_argument(
        "--texture-size",
        type=int,
        choices=(2048, 1024, 512),
        default=2048,
        help="ground texture per 512 m tile, in pixels (2048 = 25 cm a pixel)",
    )
    p.add_argument(
        "--no-textures",
        action="store_true",
        help="flat colours only: a far smaller file, and no ground detail",
    )
    p.add_argument(
        "--season",
        choices=("summer", "autumn", "winter", "spring"),
        default="summer",
        help="which season's ground maps and model textures to use",
    )
    p.add_argument(
        "--no-placed",
        action="store_true",
        help="terrain only: leave out kerbs, barriers, tyre walls, signs and buildings",
    )
    p.add_argument(
        "--trees",
        action="store_true",
        help="also place trees and bushes (many triangles, and they hide the road)",
    )
    p.add_argument(
        "--detail-budget",
        type=int,
        default=None,
        help=(
            "a ceiling on triangles for everything placed; the costliest models drop "
            "to coarser levels of detail until it fits, and past that the furthest "
            "copies are left out (default: enough to keep every copy, and at least "
            f"{DEFAULT_BUDGET:,}; kerbs always stay at full detail)"
        ),
    )


def _list(archive: _Listing, args) -> int:
    names = archive.list(args.filter)
    print(f"{len(names):,} entries" + (f" matching {args.filter!r}" if args.filter else ""))
    for name in names[: args.limit]:
        size, how = archive.describe(name)
        print(f"  {size:>12,}  {how:<6} {name}")
    if len(names) > args.limit:
        print(f"  ... {len(names) - args.limit:,} more")
    return 0


def _extract(archive: _Listing, args) -> int:
    import re

    if args.entry not in archive:
        print(f"not in the archive: {args.entry}", file=sys.stderr)
        return 1
    data = archive.read(args.entry)
    # A Forza manifest names entries with backslashes, and an archive without
    # one by number (`#12`, written as `12`).
    out = args.out or Path(re.split(r"[/\\]", args.entry)[-1].lstrip("#") or "entry")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"{len(data):,} bytes -> {out}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description=(
            "Courses, races and cars out of an installed Forza (Horizon or Motorsport, "
            "the ForzaTech engine) for the 3DHeat viewer."
        ),
        epilog=(
            "It reads the files of your own install; what it writes stays on "
            "your machine."
        ),
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="verb", required=True)

    p = sub.add_parser("identify", help="say what a Forza file is (a .minizip archive or a ForzaTech model)")
    p.add_argument("path", type=Path)

    archives = "a ForzaTech .minizip (its ChunkContentsMiniZip<n>.txt beside it names the entries)"
    key_help = "accepted for the same command line as heat3d-gamefiles; a .minizip needs no key"

    p = sub.add_parser("list", help="list what is inside a .minizip archive")
    p.add_argument("path", type=Path, help=archives)
    p.add_argument("--filter", default=None, help="only paths containing this text")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--key", default=None, help=key_help)

    p = sub.add_parser("extract", help="write one entry of a .minizip archive to disk")
    p.add_argument("path", type=Path, help=archives)
    p.add_argument("entry", help="the path as list prints it (a .minizip without its manifest: #number)")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--key", default=None, help=key_help)

    p = sub.add_parser(
        "course", help="export the ground around a lap, working out the rest"
    )
    _export_options(p)
    p.add_argument(
        "lap",
        help=(
            "a lap or course: a file written by heat3d_capture, a lap or course "
            "folder from a recorded library, or just a course's name"
        ),
    )
    p.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help=(
            "where to write the .glb (default: the course's name, in "
            "$HEAT3D_LEVELS/forza/courses when that is set, else here)"
        ),
    )
    p.add_argument(
        "--track",
        type=Path,
        default=None,
        help="the track folder, if the installed game should not be searched for",
    )
    p.add_argument(
        "--margin",
        type=float,
        default=80.0,
        help="metres of ground to keep either side of the driving (default 80)",
    )
    p.add_argument(
        "--game",
        choices=("forza", "beamng", "acrally"),
        default=None,
        help=(
            "which game the lap is from (default: what the lap file says, else Forza); "
            "a BeamNG.drive or AC Rally lap is refused with the tool that exports it"
        ),
    )
    p.add_argument("--level", default=None, help="accepted for heat3d-gamefiles' command line; not used for Forza")
    p.add_argument("--install", type=Path, default=None, help="accepted for heat3d-gamefiles' command line; not used for Forza")

    p = sub.add_parser(
        "courses", help="export every course in a recorded lap library, one file each"
    )
    _export_options(p)
    p.add_argument(
        "-o", "--out", default=None, help="folder to write into (default $HEAT3D_LEVELS/forza/courses, else ./courses)"
    )
    p.add_argument(
        "--library",
        default=None,
        help="the lap library (default: FH Companion's, under %%LOCALAPPDATA%%)",
    )
    p.add_argument("--only", nargs="+", default=None, help="just the courses whose names contain these")
    p.add_argument("--force", action="store_true", help="export again what is already there")
    p.add_argument("--track", type=Path, default=None, help="the track folder, if not the installed game's")
    p.add_argument("--margin", type=float, default=80.0, help="metres either side of the driving (default 80)")

    p = sub.add_parser(
        "races", help="every race an installed Forza defines: its own assets, venues, and the exports of it"
    )
    p.add_argument(
        "-o", "--out", default=None, help="the folder `courses` writes to (default as for `courses`)"
    )
    p.add_argument("--library", default=None, help="the lap library (default: FH Companion's)")
    p.add_argument("--track", type=Path, default=None, help="the track folder, if not the installed game's")
    p.add_argument("--markdown", type=Path, default=None, help="also write the table here")

    p = sub.add_parser("cars", help="every car of an installed Forza at low detail, in one file for the viewer")
    p.add_argument(
        "-o", "--out", type=Path, default=None,
        help="the file to write (default $HEAT3D_LEVELS/forza/forza.h3dcars, else ./forza.h3dcars)",
    )
    p.add_argument("--game", type=Path, default=None, help="the game's folder, if not the installed one found")

    p = sub.add_parser(
        "terrain", help="cut a piece of Forza terrain out, by world coordinates"
    )
    _export_options(p)
    p.add_argument("path", type=Path, help="a track folder under media/Tracks")
    p.add_argument("-o", "--out", type=Path, required=True)
    p.add_argument(
        "--box",
        type=float,
        nargs=4,
        metavar=("X0", "Z0", "X1", "Z1"),
        default=None,
        help="the region to cut, in the game's metres",
    )
    p.add_argument(
        "--route",
        type=Path,
        default=None,
        help=(
            'a route JSON with "bounds" {"min": [x, y, z], "max": [x, y, z]}, as '
            "heat3d_capture route and laps write it; its x and z extent is the region, "
            "and its positions, if it has at least 10, narrow it to a corridor"
        ),
    )
    p.add_argument(
        "--margin",
        type=float,
        default=100.0,
        help="metres to add around a route, so the verge comes with the road",
    )
    return parser


#: What pip installs each third-party module from, for the line that says so.
_PIP_NAMES = {"PIL": "Pillow", "lz4": "lz4", "numpy": "numpy"}


def main(argv: list[str] | None = None) -> int:
    from ._gamefiles import MISSING, find

    if not find():
        print(f"{PROG} {MISSING}", file=sys.stderr)
        return 2
    try:
        from . import update

        update.startup("heat3d_ext_forza")
    except Exception:  # an update check never stops an export
        pass
    args = _parser().parse_args(argv)
    try:
        return _run(args)
    except ModuleNotFoundError as exc:
        top = (exc.name or "").split(".")[0]
        if top not in _PIP_NAMES:
            raise
        print(f"{PROG} needs {_PIP_NAMES[top]}: python -m pip install {_PIP_NAMES[top]}", file=sys.stderr)
        return 2


def _run(args) -> int:
    if args.verb == "course":
        return _course(args)
    if args.verb == "courses":
        return _courses(args)
    if args.verb == "races":
        return _races(args)
    if args.verb == "cars":
        return _cars(args)

    if not args.path.exists():
        print(f"no such file: {args.path}", file=sys.stderr)
        return 2

    if args.verb == "identify":
        found = _identify(args.path) if args.path.is_file() else None
        if found is None:
            print(f"{args.path.name}: not a Forza file", file=sys.stderr)
            return 2
        print("\n".join(found))
        return 0

    if args.verb in ("list", "extract"):
        from .minizip import MAGIC as MINIZIP_MAGIC

        if not args.path.is_file() or _head(args.path, 4) != MINIZIP_MAGIC:
            print(
                f"{args.path.name} is not a ForzaTech .minizip; heat3d-gamefiles list and extract read "
                "the other archives",
                file=sys.stderr,
            )
            return 2
        try:
            archive = _MiniZipListing(args.path)
        except _reader_errors() as exc:
            print(exc, file=sys.stderr)
            return 1
        try:
            return _list(archive, args) if args.verb == "list" else _extract(archive, args)
        except _reader_errors() as exc:
            print(exc, file=sys.stderr)
            return 1
        finally:
            archive.close()

    if args.verb == "terrain":
        return _terrain(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
