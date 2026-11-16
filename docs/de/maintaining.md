---
title: Diese Doku pflegen
nav_order: 91
lang: "de"
source: maintaining.md
source_hash: "5a5a685c8282"
nav_exclude: true
search_exclude: true
---
# Diese Doku pflegen {#maintaining-these-docs}

Eine Checkliste für jede Veröffentlichung, damit die Seiten nie hinter dem Code zurückbleiben.

1. **Die Referenz neu erzeugen.** `python tools/gen_docs_reference.py` schreibt [Befehlsreferenz](../cli-reference.md) neu, aus dem eigenen `--help` des Programms und den Namen seiner Teile. `python tools/gen_docs_reference.py --check` endet mit Exit-Code 1, wenn die committete Seite veraltet ist.
2. **Die Terminal-Bilder neu zeichnen**, wenn sich eine Ausgabe ändert: `python tools/terminal_pictures.py` führt `cars --help` und `course` auf der erfundenen Strecke aus, die die Tests bauen. Nie auf einer echten Strecke oder mit einer echten Runde.
3. **Liste auf, was sich geändert hat.** `git log v<VERSION>..HEAD --oneline`, wobei `<VERSION>` die zuletzt veröffentlichte Version ist (die Datei `VERSION` bei der Veröffentlichung). Gib jedem neuen Feature, jeder Option und jeder Ausgabe einen Platz auf einer Seite und eine Zeile im Abschnitt **Docs** von [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/CHANGELOG.md).
4. **Unabhängige Prüfung.** Jemand, der die Seiten nicht geschrieben hat, liest die README und jede geänderte Seite, die Bilder eingeschlossen, dreimal: als Anfänger, der noch nie ein Terminal benutzt hat, als Achtjähriger und als Experte, der jede Option gegen `--help` prüft. Beispiele verwenden nur erfundene Namen und Zahlen.
5. **Behebe**, was die Prüfung findet.
6. **Übersetzungen.** Jede übersetzte Seite merkt sich den Hash der englischen Seite, aus der sie entstanden ist. Übersetze die Seiten neu, deren englische Quelle sich geändert hat, und prüfe dann jede Sprache: klarer Text, richtige Beschriftungen der Diagramme, dieselben Wörter wie die übersetzte Oberfläche des Viewers.
7. **Führe die Tests aus** (siehe unten).
8. **Hochladen** (push) erst nach dem Okay des Eigentümers.

## Tests {#tests}

```
python -m pip install -e .[test]
python -m pytest
```

Alles läuft mit erfundenen Daten: Archive, Modelle, Texturen, Platzierungsdateien und ganze Streckenordner schreiben die Tests selbst (`tests/forza_fixtures.py`). `course` läuft von Anfang bis Ende auf einem davon, nur aus einer Runde, und findet das erfundene Spiel so, wie es ein echtes findet.

Ein paar Tests lesen außerdem ein installiertes Forza, wenn es eins gibt, und überspringen sich, wenn nicht: Jedes Modellarchiv bildet eine geschlossene Chunk-Kette, jedes Auto steht auf seinen Rädern, und Bordsteine liegen am Boden neben der gefahrenen Linie der meistgefahrenen aufgezeichneten Rundstrecken der FH-Companion-Bibliothek. `HEAT3D_COURSE=<course folder>` wählt die Strecke für den letzten. Sie lesen das Spiel und schreiben nie in das Repository.

Die Tests brauchen 3DHeat GameFiles: installiert, oder gefunden auf dieselbe Weise wie der Befehl es findet (`HEAT3D_GAMEFILES`, der Ordner `gamefiles` einer 3DHeat-Kopie, oder ein Ordner `3DHeat-GameFiles` neben diesem).

## Übersetzungen: die Befehle {#translations-the-commands}

Die Seite ist in die 40 Sprachen des 3DHeat-Viewers übersetzt: Englisch in `docs/`, jede andere Sprache in `docs/<lang>/` mit denselben Dateinamen. `tools/docs_i18n.py` erledigt die Buchführung:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Übersetze nur, was `todo` auflistet: Markdown, Links, Code, Datei- und Spaltennamen bleiben, wie sie sind. Titel und Bildbeschreibungen werden übersetzt, und für Buttons und Bereiche verwende die eigenen Wörter des 3DHeat-Viewers (seine `src/i18n/locales/<lang>/`). Generierte Referenzseiten und Terminal-Bilder bleiben englisch. Auf der Seite zeigt eine veraltete Übersetzung das an und verlinkt die englische Seite; eine fehlende fällt auf Englisch zurück. Das Sprachmenü der Kopfzeile und die Weiterleitung der Startseite nach der Browsersprache kommen aus `docs/_includes/`.
