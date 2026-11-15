"""
The band either side of the driving that an export keeps, as the terrain cut
uses it.

For a circuit it and the bounding box are nearly the same thing; for a sprint
the box is ten times larger, and every square metre of it outside the band is
hillside decoded, textured and written for nothing. (The band itself is tested
with 3DHeat GameFiles, where `corridor` lives.)
"""

from __future__ import annotations

import numpy as np

from heat3d_gamefiles.corridor import Corridor
from heat3d_ext_forza.forzaterrain import NAME_STEP, extract

from .test_forzaterrain import make_track


class TestCuttingTerrain:
    def test_a_tile_the_band_does_not_touch_is_not_read(self, tmp_path):
        """Two tiles in the box, the driving in one of them."""
        archive, contents = make_track(tmp_path, [(0, 0, ""), (NAME_STEP, 0, "")])
        route = np.array([[100.0, 0.0, 100.0], [300.0, 0.0, 300.0]])
        with archive:
            boxed = extract(archive, contents, (0.0, 0.0), (1024.0, 512.0))
            banded = extract(archive, contents, (0.0, 0.0), (1024.0, 512.0), corridor=Corridor(route, 50.0))
        assert boxed.tiles == 2 and banded.tiles == 1
        assert 0 < len(banded.faces) < len(boxed.faces)

    def test_what_is_kept_lies_in_the_band(self, tmp_path):
        archive, contents = make_track(tmp_path, [(0, 0, "")])
        route = np.array([[0.0, 0.0, 256.0], [512.0, 0.0, 256.0]])
        band = Corridor(route, 60.0)
        with archive:
            out = extract(archive, contents, (0.0, 0.0), (512.0, 512.0), corridor=band)
        assert len(out.faces)
        assert band.triangles(out.positions, out.faces).all()
        assert out.faces.max() < len(out.positions)
        assert len(out.surfaces) == len(out.faces) == len(out.tile_of)
