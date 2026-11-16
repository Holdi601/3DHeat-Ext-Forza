---
title: "Wie eine Forza-Strecke entsteht"
nav_order: 1
lang: "de"
source: course-forza-horizon.md
source_hash: "ce7adab4b167"
nav_exclude: true
search_exclude: true
---
# Wie eine Forza-Strecke entsteht {#how-a-forza-course-is-made}

Der Forza-Export liest die Strecke direkt aus den ForzaTech-Archiven des Spiels: Gelände, bei dem Fahrbahn, Randstreifen und Gras unterschieden werden, eine Bodentextur, die aus den eigenen Bodenkarten des Spiels eingebacken wird, und jedes platzierte Modell mit seiner eigenen Textur (Bordsteine, Leitplanken, Reifenwände, Schilder, Requisiten, Gebäude). Außerdem findet er, welches der Rennen des Spiels die Runde war, und fügt hinzu, was das Spiel für genau dieses Rennen ausgibt (seine eigene Schicht: Barrieren, Zelte, Portale, Tribünen, Flaggen). Dazu kommt der Boden jedes Veranstaltungsorts, durch den die Fahrt führt, etwa der Boden eines Stadions.

```
heat3d-forza-maps course "Example Circuit"
heat3d-forza-maps course lap.json -o course.glb --season winter
heat3d-forza-maps courses -o courses
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --route lap.json -o map.glb
```

Quellen: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py) (`export_course`, `_write_course`),
[`forzainstall.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzainstall.py),
[`forzaterrain.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaterrain.py),
[`forzatexture.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzatexture.py),
[`courseexport.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/courseexport.py),
[`forzaplacement.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaplacement.py),
[`forzamaterial.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzamaterial.py),
[`forzaroute.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaroute.py).
Die Containerformate selbst stehen auf [ForzaTech](reader-forzatech.md).

## Das installierte Spiel finden {#finding-the-installed-game}

Niemand soll einen Pfad wie `D:\Games\steamapps\common\<Forza>\media\Tracks\<map>` von Hand eintippen müssen, daher wird der Pfad selbst ermittelt:

1. **Steam-Bibliotheken.** Die Datei `config\libraryfolders.vdf` von Steam wird aus `C:\Program Files (x86)\Steam` oder `C:\Program Files\Steam` gelesen, und jeder Eintrag `"path"` darin ist eine Bibliothek. Der Ordner `steamapps\common` jeder Bibliothek wird durchsucht.
2. **Microsoft Store.** `C:\XboxGames` wird durchsucht, falls es existiert. Dort liegt das Spiel eine Ebene tiefer, in `<game>\Content`.
3. Ein **Spielordner** ist jedes Unterverzeichnis dieser Ordner, das einen Ordner `media\Tracks` hat, egal wie es heißt.
4. Ein **Streckenordner** ist jeder Ordner unter `media\Tracks`, der eine `GeoChunk0.minizip` enthält. Er zählt nach seinem Inhalt, nicht nach seinem Namen, daher wird auch eine Strecke unter einem Namen gefunden, den noch niemand gesehen hat.

Liegt das Spiel woanders, gib den Streckenordner mit `--track` an. Siehe [Fehlerbehebung](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html#finding-the-game) ("no installed Forza track found" - keine installierte Forza-Strecke gefunden).

`--track <folder>` überspringt all das.

Ein Streckenordner enthält, was der Export liest:

| Datei | Was sie ist |
|---|---|
| `GeoChunk0.minizip` ... `GeoChunk3.minizip` | die Archive: jedes Modell, jede Textur und jede Platzierungsdatei, ohne Namen darin |
| `ChunkContentsMiniZip0.txt` ... `3.txt` | eine Zeile pro Archiveintrag, in der Reihenfolge der Einträge: die einzige Quelle für Namen |
| `AssetManifest.xml` | jede Textur der Strecke, mit dem Hash, über den die Materialien sie ansprechen |

## Welche Strecke {#which-track}

Ein Spiel liefert mehr als einen Streckenordner aus (die offene Welt, eine Garage oder zwei). Die richtige wird nach **Koordinaten, nicht nach Namen** gewählt:

- Die Begrenzungsbox der Runde, erweitert um `--margin`, ist die Frage.
- Für jeden Streckenordner werden die vier `ChunkContentsMiniZip*.txt`-Manifeste als Text gelesen, ohne ein Archiv zu öffnen. Jeder Geländekachelname (`autoterrain_x<X>_z<Z>..._cluster<N>.i.modelbin`) trägt seine Rasterposition. Das Werkzeug zählt, wie viele verschiedene Kacheln innerhalb der Box liegen.
- Die Strecke mit den meisten Kacheln dort gewinnt. Hat keine eine, hält der Export an mit der Meldung: "none of the installed tracks (...) has terrain at x ..., z .... Those are the game's own metres, as its telemetry reports them." (keine der installierten Strecken (...) hat Gelände bei x ..., z .... Das sind die eigenen Meter des Spiels, so wie seine Telemetrie sie meldet.)

Eine ganze Strecke wird in deutlich unter einer Sekunde ermittelt. Ein Namensvergleich könnte die falsche Karte wählen, und eine falsche Karte sieht genauso plausibel aus wie die richtige.

Die Konsole zeigt `on <track>, in <game folder>`.

## Welches Rennen {#which-race}

Das Spiel liefert jedes seiner Rennen als Route mit einer Nummer, seiner **Routen-ID**. Zu jeder Route gehören zwei Dateien:

| Datei | Was sie enthält |
|---|---|
| `media\OpenWorld\<map>\AITracks\Route<id>.owt` | die KI-Fahrlinie des Rennens: ein Knoten mit 56 Byte je Punkt ab Byte `0x60`, die Knotenzahl bei `0x24`, jeder Knoten beginnt mit seiner Position (x, y, z) in Metern des Spiels |
| `media\Stripped\gs\<map>\routedefinitions.zip` | je Rennen eine `route<id>_<map>.rtd`: einfaches XML, das aufführt, was das Rennen zur Welt hinzufügt und was es wegnimmt (siehe [Die eigene Schicht des Rennens](#the-races-own-layer)) |

Die Runde wird einer Route zugeordnet, indem sie mit jeder KI-Linie verglichen wird, deren Box die Box der Runde überlappt:

- Von jeder Probe der Runde der Abstand zum nächsten Punkt der Linie; und von jedem Punkt der Linie der Abstand zur nächsten Probe der Runde.
- Die beiden Mediane werden addiert. Gewonnen hat die Route mit der kleinsten Summe, wenn die Summe unter **30 m** liegt (`MATCH`).
- Beide Richtungen werden gebraucht: Ein kurzer Sprint liegt entlang einer langen Route, die dieselbe Straße nutzt, und eine lange Runde deckt eine kurze Route ab.

Die Konsole meldet `the game's route <id> (driven line within <n> m of it)`, oder dass keine Route passt. Ohne Treffer wird nur die frei befahrbare Welt platziert.

## Gelände {#terrain}

So wird das Gelände gefunden (in `forzaterrain.py`):

- Die Manifeste nennen das Gelände als räumlichen Index: `scene\tbheightfield\autoterrain_x-2046_z1023_cluster012.i.modelbin`.
- Die beiden Zahlen sind Rasterkoordinaten, die in Schritten von **1023** laufen, und jeder Rasterschritt ist eine Kachel von **512 m**. Die Kachel `x-2046` ist `-2046 / 1023 = -2`, was bei `-2 * 512 = -1024` m beginnt. Liest man die Namen als Meter, verfehlt jede Suche um den Faktor zwei und liefert trotzdem Gelände, nur aus dem falschen Teil der Karte.
- Eine Kachel kann dreimal vorkommen: als normale Kachel, `_cb` und `_ul`. Alle drei decken dasselbe Land ab. Pro Kachel wird eine genommen, in dieser Reihenfolge der Bevorzugung, denn sie alle zusammenzuführen würde die Geometrie verdreifachen, in übereinanderliegenden Flächen.
- Eine Kachel wird nur gelesen, wenn sie die Box der Runde **und** den Korridor berührt. Eine Kachel, die der Korridor nicht berührt, wird nie entpackt.
- Jede `.modelbin` einer gewählten Kachel wird nur auf **Detailstufe 0** dekodiert. Eine Kachel trägt vier Stufen über demselben Boden, und würden alle exportiert, läge derselbe Quadratmeter viermal in der Datei.
- Jedes Mesh trägt seine eigene Skalierung und Verschiebung im Weltraum, sodass eine Kachel dort landet, wo das Spiel sie hinlegt, ohne eine Instanztransformation. Dreiecke, deren Fläche die Box überlappt, bleiben, dann nur die, die in den Korridor reichen.
- Ein Mesh in einem Format, das der Leser ablehnt, wird übersprungen und gezählt (`N meshes could not be read`), damit ein dünnes Ergebnis erklärt ist.

Die Geländezusammenfassung gibt die Anzahl der Vertices, Dreiecke, Meshes und Kacheln sowie die x/y/z-Ausdehnung aus.

### Fahrbahn, Randstreifen, Gelände, Markierungen, Wasser {#road-verge-terrain-markings-water}

Materialnamen sagen nicht, wo die Straße ist. Rund um eine Rennstrecke nutzen 94 % des Bodens ein Straßen-Shader-Material, weil Gelände nahe einer Straße mit ihm gezeichnet wird und der Shader pro Pixel entscheidet, ob Asphalt oder Gras. Daher:

| Art | Entschieden durch |
|---|---|
| Straßenstreifen | das **Vertex-Layout**: Straßenstreifen sind der einzige Boden mit einem zweiten UV-Satz (Kanal 1); ein Dreieck, dessen drei Vertices ihn alle haben, ist Straße |
| Asphalt oder Randstreifen | innerhalb eines Straßenstreifens die **Asphaltmaske** der Kachel am Schwerpunkt des Dreiecks: 0,5 oder mehr ist `road`, weniger ist `verge` |
| Markierungen | Materialname passt auf `whiteline`, `yellowline` oder `decal` |
| Reifenspuren | Materialname passt auf `tyremark` oder `skid` (vor den Markierungen geprüft, weil Reifenspuren als `tyremark_decal_*` ausgeliefert werden) |
| Wasser | Materialname passt auf `water`, `lake`, `river`, `paddy`, `ocean` oder `sea` |
| Gelände | alles andere |

An den aufgezeichneten Runden der Testrennstrecke landen fast alle Proben auf Dreiecken von Straßenstreifen, und die große Mehrheit auf dem Asphalt-Teil, sobald die Maske den Randstreifen abgetrennt hat.

Die Asphaltmaske gibt es nur, wenn Bodentexturen eingebacken werden. Mit `--no-textures` oder bei einer Kachel, deren Karten fehlen, bleiben Straßenstreifen als `road` ganz, und es wird kein Randstreifen abgetrennt. Fehlende Karten kosten Detail, nie Geometrie.

### Gemalte Schichten werden angehoben {#painted-layers-are-lifted}

Fahrbahnmarkierungen und Reifenspuren werden als eigene Dreiecke ausgeliefert, die genau in der Straße liegen. Das Spiel zeichnet sie mit einem Tiefenversatz. Zeichnet man sie so, wie sie sind, kämpfen Straße und Farbe um jeden Pixel. Der Export gibt jeder Markierungs- und Reifenspur-Gruppe eine eigene Kopie ihrer Vertices, angehoben um **5 cm** (`DECAL_LIFT`) entlang der Oberflächennormale, damit die Straße darunter nicht mit angehoben wird.

### Normalen {#normals}

Normalen des Geländes kommen aus dem Archiv. Die x-Komponente der Normale steht als vierter Short der Position, die y- und z-Komponente im Attribut `NORMAL` (siehe [ForzaTech](reader-forzatech.md)). Fehlt bei einem Vertex der Extraktion eine Normale, werden die Normalen für den ganzen Boden stattdessen aus den Dreiecken berechnet.

## Die Bodentextur {#the-ground-texture}

Jede Geländekachel liefert drei Karten für ihr 512-m-Quadrat, in fünf Auflösungen (`_quality1` bis `_quality5`, die größte 2048 px, das sind 25 cm pro Pixel):

| Karte | Dateinamensmuster | Was sie enthält (gemessen) |
|---|---|---|
| main | `mainmap_x<X>_z<Z>_x<season>x_diff` | R, G: Detail-Normale (x, z). A: niedrig auf Asphalt und auf rauem Boden |
| sub | `submap_x<X>_z<Z>_x<season>x_diff` | Schichtgewichte. B: hoch auf Asphalt (239 auf der gefahrenen Linie, 165 daneben) |
| gloss | `autoglossf0_x<X>_z<Z>_x<season>x_glos` | G: niedrig auf Asphalt (147 gegen 215). B: steigt im Wald |

Keine dieser Karten ist ein Farbfoto. Es sind die Eingaben, mit denen der Terrain-Shader des Spiels seine Materialschichten mischt, und diese Schichten werden nicht dekodiert. Die eingebackene Textur ist daher **eine Deutung, keine Kopie des Aussehens im Spiel**. Sie behält *wo* jede Bodenart liegt, bei 25 cm, und malt sie in festen Farben:

| Boden | Lineares RGB | Gewicht |
|---|---|---|
| Gras (kurz, nahe der Strecke) | 0,30, 0,44, 0,18 | die Basis |
| rau (weiter draußen) | 0,40, 0,42, 0,22 | `smoothstep(88 -> 72, main.A) * (1 - asphalt)` |
| Wald | 0,13, 0,23, 0,10 | `smoothstep(4 -> 24, gloss.B)` |
| Asphalt | 0,20, 0,20, 0,21 | `smoothstep(188 -> 228, sub.B) * smoothstep(200 -> 168, gloss.G)` |

Für Asphalt müssen beide Karten übereinstimmen. Eine allein lässt graues Gesprenkel im Gras, wo die Blockkompression Ringe zieht. Das Ergebnis wird durch die Detail-Normale der Hauptkarte gegen ein festes Licht (`0.55 + 0.6 * lambert`) schattiert, damit Bordsteinkanten, Böschungen und Spurrillen als Relief wirken, und als 8-Bit-sRGB geschrieben.

Ausrichtung: Pixelzeile 0 ist die **Nordkante** der Kachel (größtes z), Spalte 0 ihre **Westkante** (kleinstes x). Das wurde gefunden, indem aufgezeichnete Runden auf die Asphaltmaske projiziert wurden, in allen acht Arten, wie ein Quadrat gespiegelt oder gedreht werden kann. Genau eine Art legt sie auf Asphalt. Die UVs ergeben sich daraus: `u = (x - x0) / 512`, `v = 1 - (z - z0) / 512`.

Die Karten werden in der besten Auflösung bis Qualität 5 gelesen und auf die Größe der Hauptkarte umgerechnet. Ist das Farbbild größer als `--texture-size`, wird es dann mit Lanczos-Filter auf diese Größe verkleinert. Die Asphaltmaske bleibt immer in voller Auflösung, weil sie die Geometrie bestimmt. `--season` wählt die `x<season>x`-Karten. Eine Kachel ohne Karten für diese Jahreszeit wird in flachen Farben gezeichnet, und die Konsole meldet `N without maps` (N ohne Karten).

## Platzierte Modelle {#placed-models}

Das Gelände trägt seine eigene Weltposition. Sonst trägt nichts eine. Wo jede Kopie eines Modells steht, steht in `.pgeo`-Platzierungsdateien, eine pro Kategorie und pro räumlicher Zelle: `scene\proc\cellsize\<size>\<x>_<z>\c<size>_<category>_....pgeo`. Der Aufbau der Datensätze steht bei [ForzaTech](reader-forzatech.md#placement-files-pgeo).

### Was gelesen wird {#what-is-read}

- Platzierungsdateien werden **nach Name** gefiltert. Die Zellgröße und die Zellposition im Pfad ergeben das Quadrat der Zelle (`x * size` bis `(x + 1) * size`), und nur Zellen, die die Box der Runde überlappen, in einer gewünschten Kategorie, werden geöffnet.
- Standardmäßig: `barriers`, `props`, `signs`, `buildings`, `infrastructure`, `bridges`, `rocks`, `evolving`. `--trees` fügt `trees`, `bushes` und `smashables` hinzu. Diese werden nie gelesen: `grasstemplate`, `crowdtemplate` und `cwdspline` (Gras und Zuschauer: Das Spiel zeichnet sie als animierte Sprites, es gibt keine Geometrie).
- Jede Datei gehört zu einer **Schicht**, gelesen aus ihrem Namen nach `c<size>_<category>_`. Ein Wort für die Detailstufe (`do`, `so`, `ulc`, `ulp`, `cwd`) und eine optionale Abschnittsnummer ergeben die frei befahrbare Welt. Alles andere ist eine Schicht, die das Spiel einschaltet: eine Laufzeitschicht (`rt_0`), eine Aktivität (`_tag_<name>_`), ein Sammelobjekt, alles, was unter `evolving` abgelegt ist. Eine Schicht, die Routen nennt (`rt_x<id>`, zum Beispiel `rt_x1023_x2201`), gehört nur zu diesen Rennen und wird nur gelesen, wenn die Runde einem von ihnen zugeordnet wurde. Siehe [Eingeschaltete Schichten](#switched-on-layers).
- Eine Kopie wird behalten, wenn ihre Position innerhalb der Box und innerhalb des Korridors liegt. Exakte Wiederholungen (dieselbe Position und Ausrichtung bis auf den Millimeter, von zwei benachbarten Zellen aufgelistet) werden zusammengeführt.
- **Bordsteine** sind Requisiten, deren Modellname mit `road_gen_rum` beginnt (Rüttelstreifen). Sie werden als `ground:kerbs` geschrieben, nie vereinfacht und nie weggelassen, weil eine Runde an ihnen gemessen wird.

| Kategorie | Teil | Ersatzfarbe (ohne Textur) |
|---|---|---|
| Bordsteine | `ground:kerbs` | 0,60, 0,12, 0,10 |
| Barrieren | `structure:barriers` | 0,50, 0,50, 0,50 |
| Requisiten | `structure:props` | 0,45, 0,35, 0,25 |
| Schilder | `structure:signs` | 0,70, 0,70, 0,70 |
| Gebäude | `structure:buildings` | 0,55, 0,52, 0,48 |
| Infrastruktur | `structure:infrastructure` | 0,45, 0,45, 0,47 |
| Brücken | `structure:bridges` | 0,45, 0,45, 0,45 |
| Felsen | `structure:rocks` | 0,30, 0,28, 0,25 |
| zerstörbare Objekte | `structure:smashables` | 0,12, 0,22, 0,06 |
| Bäume, Büsche | `structure:trees` | 0,10, 0,20, 0,05 |

### Die Geometrie des Modells {#the-models-geometry}

Ein platzierter Name `<model>_3D` verweist auf die Modelldateien `<model>_cluster###.i.modelbin` (bis zu einem Dutzend). Jedes Dreieck trägt eine Maske der Detailstufen, zu denen es gehört:

- Die Stufen eines Modells sind seine Dreiecke, die ausdrücklich für diese Stufe markiert sind. Die Stufen laufen ohne Lücke ab 0, die feinste zuerst.
- Dreiecke mit der Markierung `0xFFFF` (jede Stufe) sind die zerbrechlichen Teile, etwa die Pfosten einer Leitplanke oder die einzelnen Reifen eines Reifenstapels. Sie überlappen das ganze Modell, und das Spiel zeichnet sie anstelle des Modells, sobald es auseinandergebrochen ist. Sie werden nur von einem Modell ohne ausdrücklich markierte Stufe benutzt.
- Teilnetze, deren Materialshader eine projizierte **Decal** ist, werden weggelassen.

Jede Kopie wird mit ihrer Position, ihren x- und y-Achsen aus dem Datensatz (z = x Kreuz y) und ihrer Skalierung platziert. Normalen werden mit der inversen Skalierung transformiert.

### Welche Textur {#which-texture}

Ein Material nennt seine Texturen nicht. Es listet sie als Hashes, und das `AssetManifest.xml` der Strecke ordnet jeden Hash (`SourceHash`) einem Texturnamen zu. Gelesen wird nur der Abschnitt `<Textures>`, das Lesen endet bei `</Textures>` in einer Datei, die zig Megabyte groß sein kann. Dann:

1. Steckplatz `0x88B483AA` ist die Grundfarbe im Standard-Environment-Shader (jedes abgetastete Material). Bindet das Material dort eine Textur, wird diese benutzt.
2. Sonst entscheidet die Art der Textur selbst, das Wort vor ihrer GUID: `_bclr_`, dann `_diff_`, dann `_colour_`.
3. Geländekarten (`mainmap`, `submap`, `autogloss`) und Tönungspaletten (`tint`, `worldtint`) färben nie ein Modell.

Ein Modell wird also nach dem gefärbt, was sein Material bindet, nicht nach einer Textur, deren Name dem Modell ähnelt. Zum Beispiel nutzt `bar_rur_armco_crct_02_c` die Textur von `..._02_a`.

Die Textur wird aus den Archiven in der kleinsten Auflösung gelesen, die mindestens **256 px** über die Breite reicht (`MODEL_TEXTURE`), auf 256 verkleinert, falls größer, und als RGB-JPEG in der `.glb` gespeichert. Die Farbe eines Leitplankenmodells mit 256 px auf vier Meter ergibt 1,6 cm pro Pixel, und rund 80 solcher Texturen passen neben den Bodenkacheln in den Atlas des Viewers.

**Jahreszeiten.** `--season` tauscht eine Textur gegen ihr Gegenstück der Jahreszeit aus, über den Namen, die GUID wird ignoriert (`..._xsummerx_bclr` zu `..._xwinterx_bclr`, oder `..._bclr` zu `..._winter_bclr`), wenn die Strecke eines hat. Mit `--season winter` wird das Wintermaterial eines Teilnetzes auch dort benutzt, wo seine Variantentabelle eines nennt.

**Varianten.** Der Eintrag eines Teilnetzes beginnt mit einer Tabelle von `(summer, winter)`-Materialien, eines für jede Erscheinung, die eine Kopie tragen kann: fünf Drucke für eine Werbetafel, sechs Lackfarben für einen Reifenstapel. Jeder Platzierungseintrag sagt, welche Variante diese Kopie trägt. Ein Teilnetz mit weniger Varianten als das Modell wiederholt seine eigenen.

**Der Platzhalterblock.** Gemeinsame Gebäudeatlanten reservieren einen festen RGB-Block (255, 64, 0) für Flächen, die der Gebäudeshader aus anderen Texturen einfärbt. Liegt mehr als ein Zwanzigstel einer Textur innerhalb von 12 Stufen dieser Farbe, wird der Block in der durchschnittlichen Farbe der Textur übermalt. Sonst kommt eine Stadt orange heraus.

### Durchsichtige Flächen {#see-through-surfaces}

Maschendrahtzäune und Netze sind einzelne Vierecke mit Löchern im Alpha-Kanal der Textur. Voll gezeichnet wäre ein Zaun eine Wand quer zur Sicht auf die Strecke. Flächen, deren Materialshader auf `alphatest`, `alphablend`, `transmissive`, `anim_flag`, `impostor`, `branch`, `bush` oder `tree` passt, werden geprüft:

- Die Deckkraft der Textur wird über ein 32 x 32-Raster gemittelt.
- Pro Fläche (jedes ausgeschnittene Dreieck, das eine Textur teilt) werden vier Punkte je Dreieck im UV-Raum abgetastet und nach der UV-Fläche des Dreiecks gewichtet.
- Liegt die mittlere Deckkraft bei mindestens 0,05 und unter **0,5**, wird die ganze Fläche weggelassen. Unter 0,05 bedeutet das Alpha für seinen Shader etwas anderes (ein Warnschild, das 0,01 abtastet), und die Fläche bleibt voll.
- Ein Modell, dessen jede Fläche weggelassen wurde, wird gemeldet: `N models left out as see-through (mostly holes in their texture)` (N Modelle als durchsichtig weggelassen, meist Löcher in ihrer Textur).

Das Werkzeug beurteilt die ganze Fläche, nicht ein Dreieck nach dem anderen. Pro Dreieck beurteilt, blieb die Hälfte jedes Vierecks erhalten, und die Zäune kamen als Reihen von Zähnen heraus.

### Gebäude als Ganzes {#buildings-drawn-whole}

Eine Stadt baut ihre Gebäude aus modularen Teilen: Hunderttausende um eine Stadtrennstrecke, Dutzende Millionen Dreiecke selbst in der gröbsten Stufe. Wurden Teile einzeln weggelassen, blieben einzelne Wandplatten stehen. Das Spiel liefert außerdem ganze Gebäude als Ersatz in `scene\hlod_tier_1\` aus, ein Mesh pro Gebäude (Stamm `hlod_tier_1_*`), das bereits in Weltkoordinaten liegt wie das Gelände:

- Die Welt-Box jedes Ersatzes wird aus der Positionsbox seines Meshes gelesen (ein Kopfteil-Lesen, nicht ein Dekodieren). Das dauert für eine ganze Karte Sekunden.
- Ersatzteile, die die Box und den Korridor der Runde berühren, werden benutzt.
- Jedes `buildings`-Teil, dessen Position innerhalb des Grundrisses eines Ersatzes liegt (plus 0,5 m), fällt weg, und stattdessen wird der Ersatz gezeichnet. Sein Abstand zur Fahrlinie wird bis zur nächsten Kante des Gebäudes gemessen.
- Die Zusammenfassung sagt `N buildings drawn whole from the game's own stand-ins (which replace M modular pieces)` (N Gebäude als Ganzes aus den eigenen Ersatzteilen des Spiels gezeichnet, die M modulare Teile ersetzen).

### Eingeschaltete Schichten {#switched-on-layers}

Was eine eingeschaltete Schicht platziert, wird exportiert, aber getrennt von der frei befahrbaren Welt, damit der Viewer sie ein- oder ausblenden kann:

| Schicht | Teil |
|---|---|
| die frei befahrbare Welt | `structure:<category>` (wie bisher) |
| eine Schicht, die die Route des zugeordneten Rennens nennt | `structure:event_<category>` |
| jede andere eingeschaltete Schicht | `structure:layer_<category>` |

Die Zusammenfassung zählt sie: `switched-on layers: <n> copies in <m> (<layer names>)`.

### Modelle, die schon in Weltkoordinaten liegen {#models-already-in-world-coordinates}

Einige Arten von Modellen stehen in keiner Platzierungsdatei. Ihre Meshes tragen ihre eigene Weltposition, wie das Gelände, sodass nichts sie platzieren muss:

| Ordner unter `scene\models\` | Was es ist | Teil |
|---|---|---|
| `plots` | der eigene Boden eines Veranstaltungsorts: der Boden und das Innenfeld eines Stadions, ein Festivalgelände, ein Platz | `ground:venue` |
| `plinths` (und jedes Modell namens `floor`, `ground` oder `road`) | Boden, mit dem eine Straße gestaltet wird: Pflanzkübel, Stufen, das Pflaster eines Parks | `ground:plinths` |
| `hda_infrastructure` (Brücken) | prozedural gebaute Brücken | `structure:bridges` |

- Ein Modell gilt als in Weltkoordinaten, wenn die Mitte seiner Box mehr als **300 m** (`WORLD_REACH`) von seinem eigenen Ursprung entfernt liegt. Modelle aus den Platzierungsdateien liegen höchstens ein paar hundert Meter von ihrem Ursprung entfernt.
- Nicht gezeichnet: Occluder, Kabel über den Straßen, die Kulisse des Meeres, die Dächer und Occluder modularer Gebäude (die Ersatzteile zeichnen diese Gebäude), Kollisions- und Wasservolumen.
- Jedes wird aus der Box seiner Meshes gelesen (ein Kopfteil-Lesen), für eine ganze Karte einige Sekunden, einmal pro Lauf.
- Bodenteile werden nie gröber gezeichnet und nie weggelassen, um in das Budget zu passen, genau wie Bordsteine.

**Ein Veranstaltungsort wird ganz ausgeschnitten.** Berührt die Fahrt den eigenen Boden eines Veranstaltungsorts (`ground:venue`), wird der Korridor auf die ganze Fläche dieses Bodens plus `--margin` erweitert. So kommen die Tribünen, Mauern und Barrieren um ein Stadion mit, nicht nur der Streifen, den die Runden benutzt haben. Die Konsole meldet `through a venue (<model names>): cutting all of its ground, <n> km2`. Sockel erweitern den Ausschnitt nicht.

### Detail und Budget {#detail-and-the-budget}

Die Entfernungsbänder, das Budget und welche Kopien wegfallen, wenn das Budget zu klein ist, stehen unter [Detailstufen und Budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html).

### Zusammenfassung der Platzierung {#placement-summary}

```
  placed on it (1,500,000 triangles of a 1,500,000 budget, 91 textures):
        102 placed     3 models        8,568 triangles  ground:kerbs
      2,278 placed    14 models      ...                structure:barriers
    12 of 107 models drawn at a coarser level to fit the budget
    174 buildings drawn whole from the game's own stand-ins (which replace 5,120 modular pieces)
    120,000 of 125,000 copies left out to fit the budget, the smallest and furthest from the driving first (--detail-budget raises it)
    2 models left out as see-through (mostly holes in their texture): fence_a, net_b
    3 placed names have no model in the archives: ...
    venue: the driving passes through 2 pieces of a site's own ground (plt_example_floor_a, plt_example_lawn_a)
    1 models drawn where the game builds them in place (plinths, bridges)
    event layer (route 1234): 1,200 copies in barriers, decals, infrastructure, props
    40 free-roam objects left out: the race takes them away
    switched-on layers: 12 copies in 2 (rt_0, tag_example)
```

## Die eigene Schicht des Rennens {#the-races-own-layer}

Viele Rennen setzen Dinge, die es in der freien Fahrt nicht gibt: Betonwände und Zäune, die Nebenstraßen absperren, Reifenstapel, Zelte, ein Startportal, Tribünen, Flaggen, Banner. Jedes Rennen führt sie in seiner Streckendefinition auf (`route<id>_<map>.rtd` in `routedefinitions.zip`, einfaches XML in einem einfachen ZIP):

```
<Route>
  <HiddenAssets>
    <Transform guid="..." value="16 numbers" />        free-roam objects the race removes
  </HiddenAssets>
  <RouteAssets>
    <Instance>
      <Model value="tracks\<map>\scene\models\<kind>\...\<model>.model" />
      <Transform value="16 numbers" />                  what the race adds
      <Material value="n" />
    </Instance>
  </RouteAssets>
</Route>
```

- **Was hinzugefügt wird.** Jede Instanz wird wie eine Kopie aus einer Platzierungsdatei gesetzt. Die 16 Zahlen der Transformation sind vier Zeilen: die x-, y- und z-Achse des Modells (je skaliert) und seine Position in Metern des Spiels. Die dritte Zeile ist das Kreuzprodukt der ersten beiden. `Material` ist die Variante, die die Kopie trägt. Der Teil heißt `structure:event_<kind>`, wobei `<kind>` der Ordner unter `scene\models\` ist (barriers, props, infrastructure, signs; alles andere zählt als props). Der Knoten trägt die glTF-Extras `{"layer": "event", "route": <id>}`.
- **Was wegfällt.** Eine Kopie der freien Fahrt, die innerhalb von **0,1 m** der Position eines versteckten Objekts steht, wird weggelassen. Ein versteckter Eintrag, der im Ursprung steht, ist ein Modell in Weltkoordinaten. Seine Instanz-GUID wird in der `AssetManifest.xml` der Strecke nachgeschlagen (die `<Models>`-Liste: die Quelle eines Modells, dann die GUIDs seiner Kopien), um es zu benennen.
- **Boden, den das Rennen versteckt, bleibt erhalten.** Ein Rennen, das den Boden eines Veranstaltungsorts versteckt, legt dort eine eigene Oberfläche. Ist diese Oberfläche nicht unter den Modellen, die die Strecke mitliefert, bleibt der versteckte Boden stehen, als das Nächste an dem, was befahren wird. Die Zusammenfassung sagt das (`kept <model>: the race hides it for a surface of its own that the track does not ship`).
- **Nicht gezeichnet, aber gezählt.** Zuschauermarker (`crowd_proxies`: Das Spiel zeichnet die Menge aus ihnen als Sprites) und Kollisionssplines (`.splinecol`). Die Konsole listet sie auf: `its own layer: <n> copies of <m> models, <k> free-roam objects hidden; not drawn: ...`.
- Routen-Objekte, für die die Strecke kein Modell mitliefert (Lichtschein, einige Schilder, Inhalte, die das Spiel nachlädt), werden unter `placed names have no model in the archives` genannt.

Wie bei allem anderen werden nur Kopien innerhalb des Korridors platziert.

## Die Datei schreiben {#writing-the-file}

Die Teile werden in dieser Reihenfolge geschrieben: pro Kachel `terrain`, `verge`, `road` (jeweils mit dem Bild der Kachel), dann `water`, `tyre marks`, `markings` (flach, die letzten beiden angehoben), dann jeder platzierte Teil nach Name sortiert. Die Koordinaten sind die des Spiels (Meter, Y nach oben). Siehe [Ausgabeformat](https://holdi601.github.io/3DHeat-GameFiles/output-format.html).

Die Datei sagt in ihren glTF-`asset.extras`, was sie enthält:

| Feld | Bedeutung |
|---|---|
| `course_format` | `2`: die eigene Schicht des Rennens, die Veranstaltungsorte und die Modelle in Weltkoordinaten sind darin. [`courses`](commands.md#courses) exportiert eine Datei mit einer niedrigeren Nummer (oder ohne) erneut |
| `route` | die zugeordnete Routen-ID oder `null` |
| `event_copies`, `event_kinds` | wie viele Kopien der eigenen Schicht des Rennens platziert wurden, und ihre Arten |
| `hidden` | Kopien der freien Fahrt, die wegfallen, weil das Rennen sie entfernt |
| `venue` | die Bodenmodelle von Veranstaltungsorten, die die Fahrt durchquert |
| `layers` | die platzierten eingeschalteten Schichten |

## Was es kostet {#what-it-costs}

Grobe Größenordnungen:

| Strecke | Ergebnis |
|---|---|
| ein kurzer Landrundkurs | einige hunderttausend Gelände-Dreiecke, über eine Million platzierte; Sekunden, unter 100 MB |
| eine lange Sprint-Strecke von A nach B | der Korridor ist ein kleiner Teil der Box darum; etwa eine Minute, einige hundert MB |
| ein Stadt-Straßenkurs | Tausende Barrieren, Requisiten und Schilder und ganze Gebäude; mit dem automatischen Budget bis zu mehreren hundert MB |

Ein Quadratkilometer offenes Weltgelände sind etwa eine Million Dreiecke.

## Prüfungen dahinter {#checks-behind-it}

Das sind Messungen, die beim Schreiben des Lesers gemacht wurden, wie im Quelltext angegeben. Sie werden von den Tests nicht erneut ausgeführt, außer das Spiel ist installiert.

- Auf der Testrennstrecke sitzt das Auto etwa seine Bodenfreiheit über dem extrahierten Boden (Median unter 0,2 m).
- Jede geprüfte Kachel liegt innerhalb des 512-m-Quadrats, das ihr Name vorhersagt.
- Aufeinanderfolgende Leitplankenplatzierungen liegen genau 4 m auseinander, und die meisten Enden einer Leitplanke liegen innerhalb von 5 cm vom Anfang der nächsten.
- Bordsteine liegen wenige Zentimeter über dem extrahierten Boden, mit der Fläche nach oben, innerhalb von 5 m von der Fahrlinie (auch ein Test mit installiertem Spiel, siehe [Diese Doku pflegen](maintaining.md#tests)).

## Nicht gezeichnet {#not-drawn}

- Bäume und Büsche, außer mit `--trees`. Gras und Zuschauer nie (das Spiel zeichnet sie als Sprites).
- Die eigenen Modelle eines Rennens, die die Strecke nicht mitliefert (siehe [Die eigene Schicht des Rennens](#the-races-own-layer)).
- Projizierte Decal-Materialien an Modellen.
- Schildaufdrucke, die auf ihre Tafel alphagemischt sind, erscheinen undurchsichtig.
- Die Bodenfarbe ist eine Rekonstruktion, wo Asphalt, Gras und Wald liegen, nicht die eigenen Materialien des Geländes im Spiel.
