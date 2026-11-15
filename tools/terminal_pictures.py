"""Draw the documentation's terminal pictures from real runs of the command.

    python tools/terminal_pictures.py

`cars-help.svg` is `cars --help`; `course-run.svg` is `course` on the made-up
track the tests build (tests/test_course_cli.py), so no game file and no real
lap is ever in a picture. Terminal pictures stay English.
"""
import contextlib
import html
import io
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "assets" / "img"
COMMAND = "heat3d-forza-maps"


def picture(title, command, output):
    lines = [(f"$ {command}", "#7ee787")] + [(l, "#d6d9df") for l in output.rstrip("\n").split("\n")]
    width = int(32 + 7.8 * max(len(l) for l, _ in lines))
    height = 46 + 18 * (len(lines) - 1) + 22
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'role="img" aria-label="{html.escape(title)}">',
           f'<rect width="{width}" height="{height}" rx="8" fill="#1e1f24"/>',
           f'<rect width="{width}" height="26" rx="8" fill="#2c2e35"/><rect y="18" width="{width}" height="8" fill="#2c2e35"/>',
           '<circle cx="16" cy="13" r="5" fill="#ff5f57"/><circle cx="32" cy="13" r="5" fill="#febc2e"/>'
           '<circle cx="48" cy="13" r="5" fill="#28c840"/>',
           f'<text x="{width / 2:.1f}" y="17" fill="#9aa0aa" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
           f'font-size="12" text-anchor="middle">{html.escape(title)}</text>',
           '<g font-family="Consolas,Menlo,DejaVu Sans Mono,monospace" font-size="13" xml:space="preserve" '
           'style="white-space:pre">']
    for i, (line, colour) in enumerate(lines):
        body = html.escape(line, quote=False).replace(" ", "&#160;")
        out.append(f'<text x="16" y="{46 + 18 * i}" fill="{colour}" xml:space="preserve" style="white-space:pre">'
                   f'{body}</text>')
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


def run(argv):
    from heat3d_ext_forza.cli import main

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        try:
            main(argv)
        except SystemExit:
            pass
    return buffer.getvalue()


def main():
    sys.path.insert(0, str(ROOT))
    os.environ["HEAT3D_NO_UPDATE"] = "1"
    os.environ["COLUMNS"] = "88"
    os.environ.pop("HEAT3D_LEVELS", None)
    from heat3d_ext_forza._gamefiles import find

    find()
    from tests.test_course_cli import write_lap, write_track

    help_text = run(["cars", "--help"])
    (IMG / "cars-help.svg").write_text(picture("cars --help", f"{COMMAND} cars --help", help_text),
                                       encoding="utf-8", newline="\n")
    here = os.getcwd()
    with tempfile.TemporaryDirectory() as folder:
        os.chdir(folder)
        try:
            write_track(Path("Tracks") / "Example")
            write_lap(Path("lap.csv"))
            argv = ["course", "lap.csv", "--track", "Tracks/Example", "-o", "course.glb", "--margin", "40",
                    "--texture-size", "512"]
            text = run(argv)
        finally:
            os.chdir(here)
    (IMG / "course-run.svg").write_text(
        picture("course: a lap into a course", f"{COMMAND} {' '.join(argv)}", text), encoding="utf-8", newline="\n")
    print("wrote cars-help.svg, course-run.svg")


if __name__ == "__main__":
    main()
