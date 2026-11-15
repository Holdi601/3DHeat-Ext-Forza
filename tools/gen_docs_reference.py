"""Write docs/cli-reference.md from the code itself, so the reference cannot drift.

The options come from the program's own `--help`; the course's parts and the
file's extras from the names the code gives them.

    python tools/gen_docs_reference.py          # rewrite the page
    python tools/gen_docs_reference.py --check  # exit 1 when the page is stale
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cli-reference.md"
COMMAND = "heat3d-forza-maps"
VERBS = ["course", "courses", "races", "cars", "terrain", "identify", "list", "extract"]


def run(args):
    env = dict(os.environ, HEAT3D_NO_UPDATE="1", COLUMNS="88", PYTHONIOENCODING="utf-8",
               PYTHONPATH=str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    r = subprocess.run([sys.executable, "-m", "heat3d_ext_forza"] + args, capture_output=True, text=True,
                       env=env, encoding="utf-8", cwd=ROOT)
    return (r.stdout or r.stderr).rstrip()


def outputs():
    sys.path.insert(0, str(ROOT))
    from heat3d_ext_forza._gamefiles import find

    find()
    from heat3d_gamefiles.surfaces import BY_KEY, part_name

    from heat3d_ext_forza import cli, forzaplacement as placement

    tiled = ", ".join(f"`{part_name(BY_KEY[k])} x<X> z<Z>`" for k in ("terrain", "verge", "road"))
    flat = ", ".join(f"`{part_name(BY_KEY[k])}`" for k in ("water", "tyremarks", "markings"))
    placed = ", ".join(f"`{p}`" for p in placement.FALLBACK_COLOURS)
    return ["### `.glb` parts", "",
            f"Ground, per 512 m terrain tile (its grid name): {tiled}; then {flat}.", "",
            f"Placed and world-space models: {placed}; a part with its own texture adds the texture's name "
            "after a space.", "",
            f"A race's own layer: `{placement.EVENT_PART.format('<category>')}` (extras "
            "`{\"layer\": \"event\", \"route\": <id>}`); another switched-on layer: "
            f"`{placement.LAYER_PART.format('<category>')}` (extras `{{\"layer\": \"layer\"}}`); "
            f"a venue's own ground: `{placement.VENUE_PART}` (extras `{{\"layer\": \"venue\"}}`).", "",
            "### `asset.extras`", "",
            f"`course_format` ({cli.COURSE_FORMAT}), `route`, and unless `--no-placed`: `event_copies`, "
            "`event_kinds`, `hidden`, `venue`, `layers`.", ""]


def build():
    out = ["---", "title: Command reference", "nav_order: 90", "---", "", "# Command reference", "",
           "Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.",
           "The other pages explain each command step by step.", "",
           f"## `{COMMAND}`", "", "```text", run(["--help"]), "```", ""]
    for v in VERBS:
        out += [f"## `{v}`", "", "```text", run([v, "--help"]), "```", ""]
    out += ["## Output", ""]
    return "\n".join(out + outputs())


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT))
