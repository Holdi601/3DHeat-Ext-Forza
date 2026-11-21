"""The standalone spec on a synthetic Forza install and lap library (tiny fake files, no game data)."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from heat3d_ext_forza import cli, standalone_spec as S
from heat3d_ext_forza.app import entry


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")


def install(tmp_path: Path) -> Path:
    game = tmp_path / "common" / "SomeForza"
    track = game / "media" / "Tracks" / "World"
    track.mkdir(parents=True)
    (track / "GeoChunk0.minizip").write_bytes(b"z")
    (track / "ChunkContentsMiniZip0.txt").write_text("a|0\n")
    return game


def course(lib: Path, name: str, laps: int = 1) -> Path:
    folder = lib / f"{name} (course_1_2_to_3_4)" / "B" / "Car (car1)" / "tune" / "untagged"
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(laps):
        (folder / f"2026-01-0{i + 1}_lap.json").write_text("{}")
    (folder.parents[3] / "course.json").write_text("{}")
    return folder.parents[3]


def test_find_and_maps(tmp_path, monkeypatch):
    game = install(tmp_path)
    assert S._find(str(game)) == game
    assert S._find(str(game / "media" / "Tracks")) == game
    assert S._find(str(tmp_path / "nowhere")) is None
    lib = tmp_path / "laps"
    course(lib, "Alpha Circuit", 2)
    (lib / "loose folder").mkdir()
    monkeypatch.setattr(S, "library", lambda: lib)
    [m] = S._maps(game)
    assert (m.id, m.title) == ("alpha_circuit", "Alpha Circuit")
    assert [p.name for p in m.sources] == ["2026-01-01_lap.json", "2026-01-02_lap.json", "ChunkContentsMiniZip0.txt"]


def test_course_gains_and_changes(tmp_path, monkeypatch, capsys):
    game = install(tmp_path)
    lib = tmp_path / "laps"
    course(lib, "Alpha Circuit")
    course(lib, "Bravo Sprint")
    monkeypatch.setattr(S, "library", lambda: lib)
    exported = []

    def fake_run(args):
        """`course` without a game: writes a placeholder where it was told to."""
        assert args.verb == "course" and Path(args.lap).parent == lib
        exported.append(Path(args.lap).name)
        args.out.write_bytes(b"glb")
        return 0

    monkeypatch.setattr(cli, "_run", fake_run)
    g = dataclasses.replace(S.SPEC.games[0], find=lambda given: game, build=lambda root: "42")
    spec = dataclasses.replace(S.SPEC, games=[g])

    def status():
        entry.main(spec, ["status", "--json"])
        doc = json.loads(capsys.readouterr().out)["games"][0]
        return {m["id"]: m["state"] for m in doc["maps"]}

    assert status() == {"alpha_circuit": "new", "bravo_sprint": "new"}
    assert entry.main(spec, ["extract", "--new", "--progress-json"]) == 0
    capsys.readouterr()
    man = json.loads((tmp_path / "levels" / "forza" / ".heat3d-extract.json").read_text())
    assert man["entries"]["alpha_circuit"]["outputs"] == ["forza/courses/alpha_circuit.glb"]
    assert "media/Tracks/World/ChunkContentsMiniZip0.txt" in man["entries"]["alpha_circuit"]["sources"]

    # A new course is new, another lap on one makes it changed, the rest stay current.
    course(lib, "Charlie Trail")
    course(lib, "Bravo Sprint", 2)
    assert status() == {"alpha_circuit": "current", "bravo_sprint": "changed", "charlie_trail": "new"}
    exported.clear()
    assert entry.main(spec, ["extract", "--new", "--changed", "--progress-json"]) == 0
    capsys.readouterr()
    assert sorted(exported) == ["Bravo Sprint (course_1_2_to_3_4)", "Charlie Trail (course_1_2_to_3_4)"]

    # A game update that changes a track's entry list makes every course changed.
    (game / "media" / "Tracks" / "World" / "ChunkContentsMiniZip0.txt").write_text("a|0\nb|1\n")
    assert set(status().values()) == {"changed"}


def test_tasks_and_tools():
    assert S.SPEC.version == (Path(__file__).resolve().parents[1] / "VERSION").read_text().strip()
    assert S.SPEC.tasks[0].argv({"lap": "x.json"}, Path("levels")) == ["heat3d-forza-maps", "course", "x.json"]
    assert entry.run_tool(S.SPEC, "heat3d-forza-maps", ["--help"]) == 0
