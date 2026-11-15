import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# The tests never ask GitHub for a newer release.
os.environ["HEAT3D_NO_UPDATE"] = "1"

# 3DHeat GameFiles, the library the readers build on: installed, or found the
# way the command finds it (HEAT3D_GAMEFILES, a 3DHeat checkout, a clone beside).
from heat3d_ext_forza._gamefiles import MISSING, find  # noqa: E402

if not find():
    import pytest

    pytest.exit(f"the tests {MISSING}", returncode=2)
