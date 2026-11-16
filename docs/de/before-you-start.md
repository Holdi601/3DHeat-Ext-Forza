---
title: Bevor du anfängst
nav_order: 2
lang: "de"
source: before-you-start.md
source_hash: "df38b4a84aaa"
nav_exclude: true
search_exclude: true
---
# Bevor du anfängst {#before-you-start}

Du kennst die Kommandozeile noch nicht? Diese Seite bringt dich in etwa zehn Minuten von null zu einem laufenden Werkzeug. Du tippst Befehle in ein Fenster namens **Terminal**, und das Werkzeug antwortet mit Text.

## 1. Python installieren {#install-python}

1. Geh zu [python.org/downloads](https://www.python.org/downloads/) und lade **Python 3.10 oder neuer** herunter.
2. Starte den Installer. Setze auf seinem ersten Bildschirm den Haken bei **"Add python.exe to PATH"**, dann klicke auf **Install Now**.

Du brauchst außerdem ein installiertes Forza, über Steam oder den Microsoft Store (Xbox-App). Das Werkzeug findet es von selbst.

## 2. Das Werkzeug holen {#get-the-tool}

- **Mit git:** `git clone https://github.com/Holdi601/3DHeat-Ext-Forza.git`
- **Ohne git:** Auf der [GitHub-Seite](https://github.com/Holdi601/3DHeat-Ext-Forza) klickst du auf den grünen Button **Code** und dann auf **Download ZIP**, und entpackst die Datei.

## 3. Ein Terminal im Ordner des Werkzeugs öffnen {#open-a-terminal-in-the-tools-folder}

- Öffne im Explorer den Ordner, der `README.md` enthält. Klicke in die Adressleiste, tippe `cmd` und drücke Enter. Ein schwarzes Fenster öffnet sich, das schon in diesem Ordner ist.
- Oder öffne das **Windows Terminal** und wechsle mit `cd` dorthin:

  ```
  cd "C:\Users\you\Downloads\3DHeat-Ext-Forza"
  ```

## 4. Das Werkzeug installieren {#install-the-tool}

```
python -m pip install -e .
```

Das installiert den Befehl `heat3d-forza-maps` und was er braucht: [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) (die Bibliothek, auf der die Leser aufbauen), numpy, lz4 und Pillow. Du solltest Zeilen sehen, die mit `Successfully installed ...` enden.

Hast du schon eine Kopie von GameFiles und willst sie nicht noch einmal installieren? Setze `HEAT3D_GAMEFILES` auf ihren Ordner. Ein GameFiles-Ordner namens `3DHeat-GameFiles` neben diesem wird ebenfalls von selbst gefunden.

## 5. Prüfen, ob es funktioniert {#check-that-it-works}

```
heat3d-forza-maps --help
```

Du solltest `usage: heat3d-forza-maps [-h]` sehen und eine Liste der Befehle (`identify`, `list`, `extract`, `course`, ...). Das heißt: Es hat geklappt, das Werkzeug ist bereit.

## 6. Eine erste Strecke {#a-first-course}

Wenn du Runden mit FH Companion aufzeichnest, gib `course` den Namen einer Strecke, so wie die Bibliothek ihn zeigt:

```
heat3d-forza-maps course "Example Circuit"
```

Oder gib ihm eine Rundendatei (eine der Formen aus [Rundeneingaben](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

```
heat3d-forza-maps course lap.json -o example.glb
```

Es sagt, welche Strecke und welches Rennen es gefunden hat, woraus der Boden besteht und was es darauf platziert hat. Am Ende steht `wrote example.glb (... bytes)`. Siehe [Streckenexport](course-export.md).

## Die Beispiele lesen {#reading-the-examples}

- `<etwas>` ist ein **Platzhalter**: Tippe stattdessen deinen eigenen Wert, ohne die spitzen Klammern. `<lap file>` wird zum Beispiel zu `laps\my_lap.json`.
- `[--option]` in eckigen Klammern ist **optional**: Lass es weg, wenn du es nicht brauchst.
- Ein Pfad mit Leerzeichen braucht **doppelte Anführungszeichen**: `"C:\My Games\lap.json"`.

## Wenn etwas schiefgeht {#when-something-goes-wrong}

| Du siehst | Was zu tun ist |
|---|---|
| `'python' is not recognized` | Python ist nicht installiert, oder "Add to PATH" war nicht angehakt. Starte den Installer erneut, setze den Haken und öffne dann ein neues Terminal. |
| `'heat3d-forza-maps' is not recognized` | Schritt 4 wurde übersprungen oder lief in einem anderen Python. Führe ihn erneut aus; `python -m heat3d_ext_forza --help` funktioniert in jedem Fall aus dem Ordner des Werkzeugs. |
| `heat3d-forza-maps needs 3DHeat GameFiles: ...` | GameFiles ist nicht installiert. Führe Schritt 4 erneut aus oder setze `HEAT3D_GAMEFILES` auf einen GameFiles-Ordner. |
| `heat3d-forza-maps needs Pillow: ...` (oder lz4, numpy) | Führe den `pip install`-Befehl aus, den die Zeile nennt. |
| `no installed Forza track found` | Das Spiel steht nicht in einer Steam-Bibliothek oder in `C:\XboxGames`. Gib den Ordner seiner Strecke mit `--track` an ([Wie eine Forza-Strecke entsteht](course-forza-horizon.md#finding-the-installed-game)). |
| `none of the installed tracks (...) has terrain at x ..., z ...` | Die Runde stammt von einem Spiel oder einer Karte, die nicht installiert ist. |
| `can't open file` / `not found` mit einem Pfad | Der Pfad hat Leerzeichen und keine Anführungszeichen, oder er hat einen Tippfehler. Setze ihn in doppelte Anführungszeichen. |

Mehr Meldungen und ihre Behebung:
[Fehlerbehebung](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html)
auf der GameFiles-Seite.
