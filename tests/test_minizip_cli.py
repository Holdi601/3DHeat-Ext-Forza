"""
`identify`, `list` and `extract` as someone runs them on a `.minizip`, and the
answer for a file that is not a Forza one.

The archive is built the way the game ships it (see `forza_fixtures`), and the
command line is given nothing but the file: the format has to come from the
bytes. A file the tool cannot open has to say so in a line and exit non-zero,
not end in a traceback.
"""

from __future__ import annotations

import pytest

from heat3d_ext_forza.cli import main
from heat3d_ext_forza.minizip import DEFLATE, LZ4, STORED

from .forza_fixtures import build_contents, build_minizip, build_modelbin
from .test_forza_geometry import grid


def run(capsys, *argv) -> tuple[int, str, str]:
    code = main([str(a) for a in argv])
    out, err = capsys.readouterr()
    return code, out, err


def one_line(err: str) -> bool:
    return "Traceback" not in err and len(err.strip().splitlines()) == 1


@pytest.fixture
def minizip(tmp_path):
    payloads = [b"terrain " * 40, b"a guardrail", b"x" * 300]
    path = build_minizip(tmp_path / "GeoChunk2.minizip", payloads, codecs=[LZ4, STORED, DEFLATE])
    return path, payloads


class TestIdentify:
    def test_a_minizip_is_an_archive_this_reads(self, capsys, minizip):
        path, _ = minizip
        build_contents(path.with_name("ChunkContentsMiniZip2.txt"), ["a.modelbin", "b.modelbin", "c.pb"])

        code, out, _ = run(capsys, "identify", path)

        assert code == 0
        assert "ForzaTech .minizip archive, version 101" in out
        assert "3 in 1 segments" in out
        assert "ChunkContentsMiniZip2.txt" in out
        assert "not implemented" not in out and "not a format" not in out

    def test_a_minizip_without_its_manifest_goes_by_number(self, capsys, minizip):
        code, out, _ = run(capsys, "identify", minizip[0])

        assert code == 0 and "entries go by number" in out

    def test_a_forzatech_model(self, capsys, tmp_path):
        points, faces = grid(3)
        path = tmp_path / "tile.modelbin"
        path.write_bytes(build_modelbin(positions=points, faces=faces))

        code, out, _ = run(capsys, "identify", path)

        assert code == 0 and "ForzaTech model, version" in out

    def test_something_else_is_not_a_forza_file(self, capsys, tmp_path):
        path = tmp_path / "notes.txt"
        path.write_bytes(b"hello there " * 20)

        code, out, err = run(capsys, "identify", path)

        assert code == 2 and out == ""
        assert one_line(err) and "not a Forza file" in err


class TestListAndExtract:
    def test_a_minizip_by_the_names_beside_it(self, capsys, tmp_path, minizip):
        path, payloads = minizip
        build_contents(path.with_name("ChunkContentsMiniZip2.txt"), ["scene\a.modelbin", "scene\b.modelbin", "c.pb"])

        code, out, _ = run(capsys, "list", path, "--filter", "scene")
        assert code == 0
        assert "2 entries matching 'scene'" in out
        assert "lz4" in out and "stored" in out

        target = tmp_path / "out" / "b.modelbin"
        code, out, _ = run(capsys, "extract", path, "scene\b.modelbin", "--out", target)
        assert code == 0 and target.read_bytes() == payloads[1]

    def test_a_minizip_without_names_by_number(self, capsys, tmp_path, minizip):
        path, payloads = minizip

        code, out, _ = run(capsys, "list", path)
        assert code == 0 and "#2" in out and "deflate" in out

        target = tmp_path / "third.bin"
        assert run(capsys, "extract", path, "#2", "--out", target)[0] == 0
        assert target.read_bytes() == payloads[2]

    def test_the_limit_and_the_key_are_taken(self, capsys, minizip):
        """The command line heat3d-gamefiles passes on unchanged."""
        code, out, _ = run(capsys, "list", minizip[0], "--limit", "1", "--key", "00" * 32)

        assert code == 0 and "3 entries" in out and "... 2 more" in out

    def test_a_manifest_that_does_not_belong_is_refused(self, capsys, minizip):
        path, _ = minizip
        build_contents(path.with_name("ChunkContentsMiniZip2.txt"), ["only.modelbin"])

        code, _, err = run(capsys, "list", path)

        assert code == 1 and one_line(err) and "do not belong together" in err

    def test_an_entry_that_is_not_there(self, capsys, minizip):
        code, _, err = run(capsys, "extract", minizip[0], "#9")

        assert code == 1 and "not in the archive: #9" in err

    def test_a_file_that_is_no_minizip(self, capsys, tmp_path):
        path = tmp_path / "notes.txt"
        path.write_bytes(b"hello there " * 200)

        for verb in (["list", path], ["extract", path, "a.txt"]):
            code, _, err = run(capsys, *verb)
            assert code == 2 and one_line(err)
            assert "is not a ForzaTech .minizip" in err

    def test_a_file_that_is_not_there(self, capsys, tmp_path):
        code, _, err = run(capsys, "list", tmp_path / "missing.minizip")

        assert code == 2 and "no such file" in err
