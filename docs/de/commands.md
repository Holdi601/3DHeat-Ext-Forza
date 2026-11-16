---
title: Befehle
nav_order: 3
lang: "de"
source: commands.md
source_hash: "32f5e35285be"
nav_exclude: true
search_exclude: true
---
# Befehle {#commands}

Jeder Befehl läuft als `heat3d-forza-maps <command> ...` (oder aus dem Ordner des Werkzeugs ohne Installation als `python -m heat3d_ext_forza <command> ...`).

| Befehl | Nimmt | Tut |
|---|---|---|
| [`course`](#course) | eine Runde | exportiert die Strecke um sie herum |
| [`courses`](#courses) | eine aufgezeichnete Rundenbibliothek | führt `course` für jede Strecke darin aus |
| [`races`](#races) | ein installiertes Forza | listet jedes Rennen, das das Spiel festlegt: was es hinzufügt, was es versteckt, die Veranstaltungsorte und den Stand seines Exports |
| [`terrain`](#terrain) | einen Forza-Streckenordner | schneidet einen Bereich nach Weltkoordinaten aus |
| [`cars`](#cars) | ein installiertes Forza | jedes Auto in niedriger Detailstufe, in einer Datei für den Tab Rennanalyse des Viewers |
| [`identify`](#identify) | eine Datei | sagt, ob sie ein Forza-`.minizip`-Archiv oder ein ForzaTech-Modell ist, und was darin steckt |
| [`list`](#list) | eine `.minizip` | listet ihre Einträge auf |
| [`extract`](#extract) | eine `.minizip` | schreibt einen Eintrag auf die Festplatte |

**Beispiele lesen:** `<x>` bedeutet, ersetze es durch deinen eigenen Wert, ohne die spitzen Klammern. `[...]` ist optional. Setze einen Pfad mit Leerzeichen in "doppelte Anführungszeichen", zum Beispiel `"C:\Games\My Game"`. Neu dabei? Siehe [Bevor du anfängst](before-you-start.md). Die vollständige `--help` jedes Befehls steht in der [Befehlsreferenz](../cli-reference.md).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) führt dieses Werkzeug mit deinen Argumenten unverändert aus, für seine eigenen `course`, `courses`, `races`, `cars` und `terrain` bei einer Forza-Runde oder -Strecke. Für seine `identify`, `list` und `extract` fragt es nach den Forza-Dateien, die seine eigenen Leser nicht kennen. Deshalb nimmt `course` auch GameFiles' `--level` und `--install`, und `list` und `extract` nehmen `--key`. Sie werden angenommen und nicht benutzt.

Bei jedem Start kann das Programm zuerst nach einer neueren Version suchen. `HEAT3D_NO_UPDATE=1` schaltet diese Prüfung ab.

Quelle: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py).

## Exit-Codes {#exit-codes}

| Code | Bedeutung |
|---|---|
| 0 | fertig |
| 1 | die Arbeit ist fehlgeschlagen: eine Runde, die sich nicht lesen lässt, eine Runde ohne Fahrt, kein Gelände unter der Fahrt, eine Strecke in `courses`, die fehlschlug, eine `.minizip`, die sich nicht lesen lässt oder deren Namensliste nicht zu ihr gehört, ein Eintrag, der nicht im Archiv steht |
| 2 | nichts zu lesen oder falsche Argumente: kein Forza installiert, keine Strecke unter der Fahrt, keine Rundenbibliothek, eine Runde aus einem anderen Spiel, keine Forza-Datei, ein Pfad, der nicht existiert, eine fehlende Abhängigkeit (GameFiles, numpy, lz4, Pillow), `terrain` mit beiden oder keinem von `--box` und `--route`, ein Argument, das argparse ablehnt |

Jeder Fehler ist eine Zeile (oder zwei) auf der Standardfehlerausgabe, die sagt, was zu tun ist. Es gibt keinen Python-Traceback.

---

## course {#course}

```
heat3d-forza-maps course <lap> [-o FILE] [options]
```

Das exportiert die Strecke um eine Runde: den Boden in einem Streifen links und rechts der Fahrt, und was auf ihm steht, als eine `.glb`. Den Rest findet es selbst: wo das Spiel installiert ist, auf welcher seiner Strecken die Runde gefahren wurde und welches der Rennen des Spiels es war. Siehe [Streckenexport](course-export.md).

`<lap>` kann eines der folgenden sein (Einzelheiten unter [Rundeneingaben](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

- eine Rundendatei: Routen-JSON, Runden-JSON von FH Companion, `heat3d-lap`-JSON, `.npz` oder `.csv` mit den Spalten x, y, z
- ein Ordner mit Rundendateien, der rekursiv durchsucht wird (eine ganze aufgezeichnete Strecke)
- ein **Name** einer Strecke, der in der FH-Companion-Bibliothek unter `%LOCALAPPDATA%\FHCompanion\laps` nachgeschlagen wird

### Optionen {#options}

| Option | Standard | Bedeutung |
|---|---|---|
| `-o`, `--out FILE` | `<course name>.glb` im aktuellen Ordner, oder in `$HEAT3D_LEVELS/forza/courses/`, wenn das gesetzt ist | wohin geschrieben wird; der Name wird in Kleinbuchstaben geschrieben, und Folgen anderer Zeichen werden zu `_` |
| `--margin M` | 80 | Meter Boden, die auf jeder Seite der Fahrt behalten werden |
| `--texture-size {2048,1024,512}` | 2048 | Pixel der Bodentextur je 512-m-Kachel (2048 = 25 cm pro Pixel) |
| `--no-textures` | aus | nur einfarbige Flächen: eine weit kleinere Datei. Das überspringt auch die Trennung von Fahrbahn und Randstreifen |
| `--season {summer,autumn,winter,spring}` | summer | welche Jahreszeit die Bodenkarten und Modelltexturen hat |
| `--no-placed` | aus | nur das Gelände: keine Bordsteine, Barrieren, Schilder, Gebäude |
| `--trees` | aus | auch Bäume, Büsche und zerstörbare Objekte platzieren |
| `--detail-budget N` | automatisch | eine Obergrenze für Dreiecke für alles Platzierte; siehe [Detailstufen und Budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html) |
| `--track DIR` | gesucht | der Streckenordner (unter `media\Tracks`, mit `GeoChunk0.minizip`), wenn das installierte Spiel nicht durchsucht werden soll |
| `--game {forza,beamng,acrally}` | was die Rundendatei sagt, sonst `forza` | aus welchem Spiel die Runde stammt (siehe unten) |
| `--level`, `--install` | | für GameFiles' Kommandozeile angenommen, nicht benutzt |

### Welches Spiel {#which-game}

Das Spiel kommt aus `--game`, dann aus dem Feld `game` einer `heat3d-lap`-Datei (oder aus der Zeile `# {...}` mit der Beschreibung einer CSV), und fällt sonst auf Forza zurück. Ein Ordner bekommt das Spiel, das seine Dateien nennen, wenn sie nur eines nennen. Eine Datei, die keins nennt (eine Runde aus FH Companion, `course.json`, eine CSV ohne Beschreibungszeile), zählt nicht.

| Wert | Was passiert |
|---|---|
| beginnt mit `forza` | der Forza-Export |
| `beamng` | abgelehnt, Exit-Code 2: `export it with heat3d-beamng-maps course` |
| `assetto-corsa-rally` oder `acrally` | abgelehnt, Exit-Code 2: `export it with heat3d-acrally-maps course` |
| `assetto-corsa-evo` | abgelehnt: "keeps all its content in one package obfuscated with a key, and this tool recovers none" |
| `iracing` | abgelehnt: "tracks ship in a protected format that is not a file-extraction target" |
| alles andere | abgelehnt: "there is no course reader for <game> yet" |

Die letzten drei schlagen auch Alternativen vor: die Strecke aus dem Spielverlauf nachbauen (3DHeat GameCapture) oder die Runden ohne Strecke analysieren. Denn der Tab Rennanalyse des Viewers zeichnet aus ihnen eine Straße.

### Beispiele {#examples}

```
# A course from the FH Companion library, by name
heat3d-forza-maps course "Example Circuit"

# One lap file, a narrower band, a smaller file
heat3d-forza-maps course lap.json -o example.glb --margin 40 --texture-size 1024

# Winter textures, trees included
heat3d-forza-maps course "Example Circuit" --season winter --trees

# A hard ceiling of 500,000 placed triangles
heat3d-forza-maps course lap.json --detail-budget 500000

# A track folder given directly (game installed somewhere it is not searched)
heat3d-forza-maps course lap.json --track "D:\Games\<Forza>\media\Tracks\<map>"
```

Was ein Lauf ausgibt, auf einer erfundenen Strecke, die die Tests bauen (auf einer echten Strecke gehen die Zahlen in die Hunderttausende Dreiecke, und es sagt, welche Strecke und welches Rennen es gefunden hat):

![Lauf auf einer erfundenen Strecke](../assets/img/course-run.svg)

## courses {#courses}

```
heat3d-forza-maps courses [-o FOLDER] [options]
```

Das führt `course` für jeden Streckenordner in einer aufgezeichneten Rundenbibliothek aus und schreibt je eine `<name>.glb`.

| Option | Standard | Bedeutung |
|---|---|---|
| `-o`, `--out FOLDER` | `courses`, oder `$HEAT3D_LEVELS/forza/courses`, wenn das gesetzt ist | der Ordner, in den geschrieben wird (wird angelegt, falls er fehlt) |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | die Rundenbibliothek |
| `--only TEXT [TEXT ...]` | alle | nur die Strecken, deren Ordnernamen einen dieser Texte enthalten (ohne Groß- und Kleinschreibung) |
| `--force` | aus | schon Exportiertes, das eine `.glb` hat, noch einmal exportieren |
| `--track DIR` | gesucht | wie bei `course` |
| `--margin M` | 80 | wie bei `course` |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | wie bei `course` |

Als Streckenordner zählt ein direkter Unterordner der Bibliothek, dessen Name ` (course_` enthält. So benennt FH Companion sie, zum Beispiel `Example Circuit (course_1200_3400_to_1175_3400)`. Der Teil ab ` (course_` fällt aus dem Namen heraus.

So verläuft ein Lauf:

- Eine Strecke, deren `.glb` schon existiert, wird übersprungen (`kept`), außer `--force` ist gesetzt. So macht ein unterbrochener Lauf dort weiter, wo er aufgehört hat.
- Eine `.glb`, die eine ältere Version ohne die eigene Schicht des Rennens und ohne Veranstaltungsorte geschrieben hat (ihr `asset.extras.course_format` fehlt oder ist niedriger als das aktuelle), wird erneut exportiert, als wäre `--force` nur für sie gesetzt.
- Zwei Streckenordner mit demselben Namen vor ` (course_` (ein Recorder, der eine neue Strecke nach einer alten benannt hat) überschreiben sich nicht. Der zuerst angelegte Ordner behält `<name>.glb`, der andere wird als `<name>_<start>.glb` geschrieben. `<start>` ist der Startpunkt, Minuszeichen stehen als `m` (zum Beispiel `example_circuit_m120_m340.glb`).
- Eine Strecke, die fehlschlägt (Runden, die sich nicht lesen lassen, zu wenig Speicher, kein Gelände ...), wird als `FAILED` gemeldet, und der Lauf geht weiter.
- Am Ende gibt es eine Tabelle mit Status, Größe in MB, benötigten Sekunden und Name, danach `<n> of <total> courses in <folder>`.
- Der Exit-Code ist 1, wenn eine Strecke fehlgeschlagen ist, und 2, wenn es keine Rundenbibliothek gibt.

```
heat3d-forza-maps courses -o courses --only circuit sprint --texture-size 1024
```

## races {#races}

```
heat3d-forza-maps races [-o FOLDER] [--markdown FILE] [options]
```

Listet jedes Rennen auf, das ein installiertes Forza aus seinen Streckendefinitionen festlegt (siehe [Wie eine Forza-Strecke entsteht](course-forza-horizon.md#which-race)), und prüft die Exporte in einem `courses`-Ordner gegen sie. Es liest das Spiel und die Rundenbibliothek. Geschrieben wird nur die optionale Tabelle.

| Option | Standard | Bedeutung |
|---|---|---|
| `-o`, `--out FOLDER` | wie bei `courses` | der Ordner, in den `courses` schreibt und dessen Dateien geprüft werden |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | die Rundenbibliothek |
| `--track DIR` | gesucht | der Streckenordner, wenn es nicht der des installierten Spiels ist |
| `--markdown FILE` | keine | schreibt die Tabelle zusätzlich dorthin, als Markdown |

Eine Zeile je Rennen und eine je aufgezeichneter Strecke, auf der es gefahren wurde:

| Spalte | Bedeutung |
|---|---|
| route | die Routen-ID |
| course | die aufgezeichnete Strecke, die ihr zugeordnet wurde, falls vorhanden |
| own assets | Kopien, die das Rennen zur frei befahrbaren Welt hinzufügt |
| drawn | davon die Kopien, deren Modell die Strecke mitliefert |
| kinds | die hinzugefügten Kopien nach Art (Barrieren, Requisiten, Decals, Infrastruktur, ...) |
| not geometry | Zuschauermarker und Kollisionssplines, gezählt |
| hidden | Objekte der frei befahrbaren Welt, die das Rennen entfernt |
| venue | die Bodenmodelle von Veranstaltungsorten, an denen die KI-Linie des Rennens auf 10 m vorbeiführt |
| export | `current`, `older format` (wird von `courses` erneut exportiert), `not exported`, oder leer bei einem Rennen ohne aufgezeichnete Strecke |

Am Ende steht eine Zählung: `<n> races: <a> with assets of their own, <v> through a venue, <d> driven in the lap library, <s> recorded courses to export again`.

```
heat3d-forza-maps races -o courses --markdown races.md
```

## terrain {#terrain}

```
heat3d-forza-maps terrain <track folder> -o FILE (--box X0 Z0 X1 Z1 | --route FILE) [options]
```

Das ist der Ausschnitt, bei dem alles von Hand angegeben wird: Du gibst den Streckenordner und einen Bereich an, keine Runde. Das ist nützlich, wenn der gewünschte Bereich eine Box ist statt einer Fahrt.

| Option | Standard | Bedeutung |
|---|---|---|
| `<path>` | Pflicht | ein Forza-Streckenordner unter `media\Tracks` (mit `GeoChunk*.minizip`) |
| `-o`, `--out FILE` | Pflicht | die zu schreibende `.glb` |
| `--box X0 Z0 X1 Z1` | | der Bereich, in Metern des Spiels (x und z, so wie die Telemetrie sie meldet); Ecken in beliebiger Reihenfolge |
| `--route FILE` | | eine Routen-JSON mit `"bounds": {"min": [x, y, z], "max": [x, y, z]}`, wie `heat3d_capture route` und `heat3d_capture laps` sie schreiben; wird als UTF-8 gelesen, mit oder ohne Byte-Order-Mark |
| `--margin M` | **100** | Meter, die zu den Grenzen einer Route hinzukommen, und die Breite des Korridors, wenn die Route eine Linie hat |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | wie bei `course` |

Gib genau eines von `--box` und `--route` an, sonst ist der Exit-Code 2. Bei `--route` ist der Ausschnitt die `bounds` der Route (`min`/`max`, x und z), um den Rand erweitert. Enthält die Datei außerdem mindestens 10 Positionen, verengt sich der Ausschnitt auf einen Korridor von `--margin` Metern um sie. Platzierte Modelle bekommen ihre Detailstufe dann nach dem Abstand zu dieser Linie. Bei `--box` bleibt die ganze Box erhalten, und die Detailstufe geht an das, was der Mitte der Box am nächsten steht.

Die Höhe spielt beim Ausschnitt nie eine Rolle. Eine Box außerhalb der Karte oder im Meer ergibt "no terrain there" (Exit-Code 1), kein Fehler über die Koordinaten.

```
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --box 0 0 512 512 -o piece.glb
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --route route.json -o map.glb
```

## cars {#cars}

```
heat3d-forza-maps cars [-o FILE] [--game FOLDER]
```

Jedes Auto eines installierten Forza in der niedrigen Detailstufe des Spiels, in einer Datei für den Tab Rennanalyse des Viewers. Dauert Sekunden und schreibt etwa 5 MB. Siehe [Forza-Autos](forza-cars.md).

## identify {#identify}

```
heat3d-forza-maps identify <path>
```

Liest die Datei und sagt, was sie ist, an ihren Bytes, nicht an ihrer Endung: ein ForzaTech-`.minizip`-Archiv (die Kennung `PGZP`: Version, Anzahl der Einträge und Segmente, und ob die `ChunkContentsMiniZip<n>.txt` mit den Namen seiner Einträge daneben liegt) oder ein ForzaTech-Modell, `.modelbin` (Version, Anzahl der Chunks, die häufigsten Chunk-Tags). Alles andere endet mit Exit-Code 2 und `<file>: not a Forza file` auf der Standardfehlerausgabe. Siehe [Forza-Dateien untersuchen](inspecting-files.md).

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

| Option | Standard | Bedeutung |
|---|---|---|
| `<.minizip>` | Pflicht | ein ForzaTech-`.minizip`, etwa die `GeoChunk0.minizip` einer Strecke |
| `--filter TEXT` | keiner | nur Pfade, die TEXT enthalten, ohne Groß- und Kleinschreibung |
| `--limit N` | 50 | gibt höchstens N Einträge aus (die Gesamtzahl wird immer ausgegeben) |
| `--key HEX` | keiner | angenommen, nicht benutzt: eine `.minizip` ist nicht verschlüsselt |

Jede Zeile zeigt die unkomprimierte Größe, die Komprimierung (`lz4`, `deflate` oder `stored`) und den Pfad, so wie die Namensliste neben dem Archiv ihn schreibt.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

| Option | Standard | Bedeutung |
|---|---|---|
| `<entry>` | Pflicht | der Pfad genau so, wie `list` ihn ausgibt, oder `#<number>` |
| `--out FILE` | der Dateiname des Eintrags (nach dem letzten `/` oder `\`), im aktuellen Ordner | wohin geschrieben wird; übergeordnete Ordner werden angelegt |
| `--key HEX` | keiner | angenommen, nicht benutzt |

## Umgebungsvariablen {#environment-variables}

| Variable | Wirkung |
|---|---|
| `HEAT3D_LEVELS` | ein Ordner für jeden Export ohne `-o`: Strecken in `<HEAT3D_LEVELS>/forza/courses/`, das Autopaket in `<HEAT3D_LEVELS>/forza/`. Ist sie nicht gesetzt, landen sie im aktuellen Ordner |
| `HEAT3D_GAMEFILES` | ein GameFiles-Ordner, wenn GameFiles nicht mit pip installiert ist |
| `HEAT3D_NO_UPDATE` | jeder Wert außer leer, `0`, `false`, `no` schaltet die Suche nach Updates aus |
| `LOCALAPPDATA` | wo die FH-Companion-Bibliothek und der Update-Cache gesucht werden |
| `HEAT3D_COURSE` | nur für Tests: die Strecke, die der Test der installierten Bordsteine benutzt; siehe [Diese Doku pflegen](maintaining.md#tests) |
