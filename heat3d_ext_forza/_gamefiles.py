"""
Finding 3DHeat GameFiles, the library this tool's readers are built on.

Installed with pip it is simply importable. From a plain checkout it is looked
for, in order, in `HEAT3D_GAMEFILES`, in `<this repo>/../../gamefiles` (this
tool inside a 3DHeat checkout, under `exporters/ext/`) and in
`<this repo>/../3DHeat-GameFiles` (the two cloned side by side).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

#: What to do when it is nowhere: one line, for the command to print.
MISSING = (
    "needs 3DHeat GameFiles: pip install git+https://github.com/Holdi601/3DHeat-GameFiles.git, "
    "or set HEAT3D_GAMEFILES to its folder"
)


def _importable() -> bool:
    try:
        # A module of it rather than the bare name: an empty `heat3d_gamefiles`
        # folder on the path imports as a namespace package and holds nothing.
        import heat3d_gamefiles.glb  # noqa: F401
    except ImportError:
        for name in [n for n in sys.modules if n == "heat3d_gamefiles" or n.startswith("heat3d_gamefiles.")]:
            del sys.modules[name]
        return False
    return True


def find() -> bool:
    """Make `heat3d_gamefiles` importable; False when it is nowhere to be found."""
    if _importable():
        return True
    repo = Path(__file__).resolve().parents[1]
    for folder in (os.environ.get("HEAT3D_GAMEFILES", "").strip(), repo.parent.parent / "gamefiles",
                   repo.parent / "3DHeat-GameFiles"):
        if folder and (Path(folder) / "heat3d_gamefiles" / "__init__.py").is_file():
            sys.path.insert(0, str(Path(folder).resolve()))
            if _importable():
                return True
            sys.path.pop(0)
    return False
