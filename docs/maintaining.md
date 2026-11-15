---
title: Maintaining these docs
nav_order: 91
---

# Maintaining these docs

A checklist for each release, so the pages never fall behind the code.

1. **Regenerate the reference.** `python tools/gen_docs_reference.py` rewrites
   [Command reference](cli-reference.md) from the program's own `--help` and
   part names. `python tools/gen_docs_reference.py --check` exits 1 when the
   committed page is stale.
2. **Redraw the terminal pictures** when an output changes:
   `python tools/terminal_pictures.py` runs `cars --help` and `course` on the
   made-up track the tests build. Never a real track or a real lap.
3. **List what changed.** `git log v<VERSION>..HEAD --oneline`, where
   `<VERSION>` is the last released version (the `VERSION` file at release).
   Give every new feature, option and output a place on a page, and a row in
   the **Docs** section of [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/CHANGELOG.md).
4. **Independent review.** Someone who did not write the pages reads the
   README and every changed page, the pictures included, three times: as a
   beginner who has never used a terminal, as an 8-year-old, and as an expert
   who checks every option against `--help`. Examples use made-up names and
   numbers only.
5. **Fix** everything the review finds.
6. **Translations.** Every translated page records the hash of the English page
   it was made from. Translate again the pages whose English source changed,
   then review each language: clear text, correct diagram labels, the same
   words as the viewer's own translated interface.
7. **Run the tests** (below).
8. **Push** only after the owner's go-ahead.

## Tests

```
python -m pip install -e .[test]
python -m pytest
```

Everything runs on made-up data: archives, models, textures, placement files and
whole track folders are written by the tests themselves (`tests/forza_fixtures.py`),
and `course` is run end to end on one, from a lap alone, finding the made-up
game the way it finds a real one.

A few tests also read an installed Forza when there is one, and skip when there
is not: every model archive forms a closed chunk chain, every car stands on its
wheels, and kerbs lie on the ground beside the driven line of the most driven
recorded circuits in the FH Companion library. `HEAT3D_COURSE=<course folder>`
picks the course for that last one. They read the game; they never write into
the repository.

The tests need 3DHeat GameFiles: installed, or found the way the command finds
it (`HEAT3D_GAMEFILES`, the `gamefiles` folder of a 3DHeat checkout, or a
`3DHeat-GameFiles` folder beside this one).

## Translations: the commands

The site is translated into the 3DHeat viewer's 40 languages: English in
`docs/`, each other language in `docs/<lang>/` with the same file names.
`tools/docs_i18n.py` does the bookkeeping:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Translate only what `todo` lists: keep Markdown, links, code, file and column names as they are,
translate titles and picture descriptions, and use the 3DHeat viewer's own words for its buttons
and panels (its `src/i18n/locales/<lang>/`). Generated reference pages and terminal pictures stay
English. On the site, an outdated translation says so and links the English page; a missing one
falls back to English. The header's language menu and the home page's browser-language redirect
come from `docs/_includes/`.
