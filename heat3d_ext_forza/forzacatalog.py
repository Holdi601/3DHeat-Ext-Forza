"""
The car catalogue of an installed Forza: every car archive with its number,
make, model and year, joined with what else is known on this machine about it.

- The archives under `media/Cars` give the key (`BMW_E36M3_97`), the car
  numbers the telemetry calls `carOrdinal` (from the animation clip names, as
  `forzacars` reads them) and make and year from the name. Only the archive's
  list of entries is read.
- A car list as FH Companion keeps it (`fhc-cars-1`, under
  `%LOCALAPPDATA%/FHCompanion/cars`), when there is one: the car's full name,
  its stock class and performance index, its type and country.
- The laps in a lap library (FH Companion's by default), when there are any:
  each lap's header states the car's drivetrain, cylinders and peak power as it
  was driven (with its upgrades, so `...Driven`), and its class and index.
  Only the first bytes of each lap are read.

The game's own car database is not read. The output is
`<HEAT3D_LEVELS>/forza/catalog.json` in the viewer's catalogue format
(`3dheat-catalog`, version 1). It names cars, and the model of each is the
car's entry in the local car file (`forza.h3dcars`).
"""

from __future__ import annotations

import json
import os
import re
import zipfile
from collections import Counter
from pathlib import Path

from .forzacars import CLIPS, GAME, name_parts

FORMAT = "3dheat-catalog"

#: The telemetry's drivetrain numbers.
DRIVETRAINS = {0: "FWD", 1: "RWD", 2: "AWD"}

_HEAD = {
    key: re.compile(rf'"{key}":\s*(-?\d+)')
    for key in ("carOrdinal", "performanceIndex", "drivetrain", "cylinders", "peakKilowatts")
}
_CLASS = re.compile(r'"Class":"([A-Z0-9]+)"')


def companion_home() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "FHCompanion"


def archive_ordinals(archive: Path) -> list[int]:
    """The car numbers an archive's animation clips name."""
    with zipfile.ZipFile(archive) as z:
        return sorted({int(m.group(1)) for m in (CLIPS.search(n) for n in z.namelist()) if m})


def read_car_list(path: Path | None) -> dict[int, dict]:
    """A companion car list by car number; empty without one."""
    if path is None or not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("format") != "fhc-cars-1":
        return {}
    out: dict[int, dict] = {}
    for car in data.get("cars", []):
        for number in car.get("ids") or [car.get("id")]:
            if isinstance(number, int):
                out[number] = car
    return out


def read_lap_heads(library: Path | None, *, limit: int = 4096) -> dict[int, dict]:
    """What the laps of a library say about each car number: drivetrain, cylinders, power, classes driven."""
    seen: dict[int, dict] = {}
    if library is None or not library.is_dir():
        return seen
    for lap in library.rglob("*.json"):
        try:
            with lap.open("rb") as fh:
                head = fh.read(limit).decode("utf-8", "replace")
        except OSError:
            continue
        found = {k: int(m.group(1)) for k, rx in _HEAD.items() if (m := rx.search(head))}
        if "carOrdinal" not in found:
            continue
        car = seen.setdefault(found["carOrdinal"], {"laps": 0, "drivetrain": Counter(), "cylinders": Counter(),
                                                    "peakKilowatts": Counter(), "classes": Counter(), "pi": []})
        car["laps"] += 1
        for key in ("drivetrain", "cylinders", "peakKilowatts"):
            if key in found:
                car[key][found[key]] += 1
        if "performanceIndex" in found:
            car["pi"].append(found["performanceIndex"])
        if (m := _CLASS.search(head)) is not None:
            car["classes"][m.group(1)] += 1
    return seen


def neutral_key(name: str, make: str, model: str, year: int | None) -> str:
    """The car as a real vehicle, independent of any game: its name and year."""
    base = name or f"{make} {model.replace('_', ' ')}"
    base = re.sub(r"\s+'\d{2}$", "", base).strip()
    return f"{base} {year}" if year else base


def build_catalog(archives: list[Path], car_list: dict[int, dict], laps: dict[int, dict], *,
                  game_build: str = "", source: str = "") -> dict:
    items = []
    for archive in archives:
        try:
            ordinals = archive_ordinals(archive)
        except (zipfile.BadZipFile, OSError):
            continue
        if not ordinals:
            continue  # props and traffic without a car number
        make, model, year = name_parts(archive.stem)
        listed = next((car_list[n] for n in ordinals if n in car_list), None)
        if listed:
            make = listed.get("make") or make
            year = listed.get("year") or year
        name = (listed or {}).get("name") or f"{make} {model.replace('_', ' ')}"
        numbers: dict = {}
        if listed and isinstance(listed.get("pi"), int):
            numbers["pi"] = listed["pi"]
        if listed and isinstance(listed.get("price"), int):
            numbers["price"] = listed["price"]
        driven = [laps[n] for n in ordinals if n in laps]
        item: dict = {
            "id": archive.stem,
            "key": neutral_key(name, make, model, year),
            "kind": "vehicle",
            "name": name,
            "class": (listed or {}).get("class") or "",
            "group": (listed or {}).get("type") or "",
            "nation": (listed or {}).get("country") or "",
            "make": make,
            "year": year,
            "ordinals": ordinals,
            "model": f"forza/forza.h3dcars#{archive.stem}",
            "numbers": numbers,
        }
        if driven:
            total: dict[str, Counter] = {k: Counter() for k in ("drivetrain", "cylinders", "peakKilowatts", "classes")}
            pis: list[int] = []
            for d in driven:
                for k in total:
                    total[k].update(d[k])
                pis += d["pi"]
            if total["drivetrain"]:
                item["drivetrainDriven"] = DRIVETRAINS.get(total["drivetrain"].most_common(1)[0][0], "")
            if total["cylinders"]:
                numbers["cylindersDriven"] = total["cylinders"].most_common(1)[0][0]
            if total["peakKilowatts"]:
                numbers["peakKilowattsDriven"] = max(total["peakKilowatts"])
            if pis:
                numbers["piDriven"] = [min(pis), max(pis)]
            item["classesDriven"] = sorted(total["classes"])
            item["laps"] = sum(d["laps"] for d in driven)
        items.append(item)
    items.sort(key=lambda i: (i["make"], i["name"], i["year"] or 0))
    return {"format": FORMAT, "version": 1, "game": GAME, "gameBuild": game_build, "source": source, "items": items}


def game_build(game: Path) -> str:
    """The installed build, from the game's own manifest when it states one."""
    for name in ("MicrosoftGame.Config", "appxmanifest.xml"):
        p = game / name
        if p.is_file():
            m = re.search(r'Version="([\d.]+)"', p.read_text("utf-8", "replace"))
            if m:
                return m.group(1)
    return ""
