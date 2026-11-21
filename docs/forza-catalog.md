---
title: Car catalogue
nav_order: 7
---

# Car catalogue: `catalog`

Writes the list of an installed Forza's cars for the viewer: each car's number
(the one the telemetry sends), make, model and year, so the viewer can name,
group and filter the cars in your laps.

```
heat3d-forza-maps catalog
```

It writes `catalog.json` under `$HEAT3D_LEVELS/forza/` (else the current
folder; `-o` names another file).

What it reads:

- the car archives under the game's `media/Cars`: only their list of entries,
  for the car number; make and year come from the archive's name;
- if present, FH Companion's car list (`%LOCALAPPDATA%\FHCompanion\cars`, or
  `--car-list`): full name, stock class and index, type and country;
- if present, your lap library (FH Companion's, or `--library`): the first
  bytes of each lap, for the drivetrain, cylinders, power and class each car was
  driven with.

The catalogue stays on your machine; nothing is uploaded.
