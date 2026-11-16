---
title: Regeln und Lizenzen
nav_order: 12
lang: "de"
source: terms.md
source_hash: "e6bd7ab93f27"
nav_exclude: true
search_exclude: true
---
# Regeln und Lizenzen {#terms-and-licence}

## Das Spiel gehört Microsoft {#the-game-is-microsofts}

Forza Horizon und Forza Motorsport, ihre Strecken, Autos und Texturen gehören Microsoft (Playground Games und Turn 10 Studios). 3DHeat Forza ist nicht mit Microsoft, Playground Games oder Turn 10 Studios verbunden und wird von ihnen nicht unterstützt. Forza und die zugehörigen Namen und Marken gehören ihren Inhabern.

Dieses Repository enthält **keine Datei des Spiels** und keine Strecke, kein Auto und keine Textur, die aus einer solchen Datei gemacht wurde - keine Spielinhalte, keinen Spielcode, keine DLLs. Das Werkzeug **lädt nie Spielinhalte herunter**: Es liest die Kopie, die **auf deinem Rechner installiert** ist.

## Keine Schlüssel: keiner mitgeliefert, keiner wiederhergestellt {#no-keys-none-shipped-none-recovered}

ForzaTechs `.minizip`-Archive und ihre Modelle, Texturen und Platzierungsdateien sind nicht verschlüsselt. Das Werkzeug enthält keinen Schlüssel, stellt keinen wieder her, liest keinen Speicher eines anderen Prozesses und schleust nichts in das Spiel ein. Die Runden kommen aus der Telemetrie, die das Spiel selbst veröffentlicht.

## Die Ausgabe ist nicht zur Weitergabe gedacht {#output-is-not-for-redistribution}

Was herauskommt, ist Geometrie für **räumlichen Kontext**: der Boden, die Straße und was daneben steht, auf ein Budget verkleinert, damit Runden an Ort und Stelle analysiert werden können. Sie bleibt auf deinem Rechner.

- Behalte exportierte `.glb`-Strecken, die Autodatei (`.h3dcars`) und die Texturen darin für deine eigene Analyse, auf dem Rechner, auf dem sie entstanden sind.
- Veröffentliche, teile oder verkaufe exportierte Strecken, Autos, Modelle oder Texturen nicht.
- Die `.gitignore` des Repositorys hält Spieldateien, Exporte, Runden und Aufzeichnungen nach Dateityp aus der Versionsverwaltung heraus (`*.glb`, `*.h3dcars`, `*.minizip`, `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` und weitere).

## Die Formate {#the-formats}

ForzaTechs Formate sind nicht dokumentiert. Keiner der Leser hier ist vom Quellcode eines anderen Projekts abgeleitet: Jeder Offset wurde an den Dateien gemessen, und wie jeder bestimmt wurde, steht auf [ForzaTech](reader-forzatech.md).

## Warum dies ein eigenes Werkzeug ist {#why-this-is-a-separate-tool}

Jeder Spiele-Leser ist ein eigenes kleines Projekt mit eigener Lizenzdatei, eigenen Releases und eigenem Issue-Tracker. So lässt er sich für sich allein installieren, aktualisieren und pflegen - oder auf Wunsch eines Rechteinhabers zurückziehen -, ohne dass der Viewer oder die anderen Werkzeuge davon berührt werden.

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) enthält die generischen Leser für Engine-Formate und die gemeinsame Infrastruktur. Dieses Werkzeug enthält die Leser für Forza.

Rechteinhaber: Bitte ein Issue unter [github.com/Holdi601/3DHeat-Ext-Forza/issues](https://github.com/Holdi601/3DHeat-Ext-Forza/issues) eröffnen - wir antworten schnell und entfernen auf Anfrage alles.

## Die Lizenz dieses Werkzeugs {#this-tools-licence}

Alles, was für dieses Repository geschrieben wurde, steht unter der **MIT-Lizenz** ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSE)): Du darfst es benutzen, ändern und weitergeben, kommerziell oder nicht.

Fremde Pakete, alle freizügig ([`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSES.md)):

| Paket | Lizenz | Wofür |
|---|---|---|
| 3DHeat GameFiles | MIT | der glTF-Schreiber, die Rundendateien, der Korridor, die Bodenarten, das Detailbudget, die Steam-Bibliotheken |
| numpy | BSD-3-Clause | das Dekodieren der Meshes |
| lz4 | BSD-3-Clause | die LZ4-Blöcke der `.minizip`-Archive |
| Pillow | MIT-CMU (HPND) | blockkomprimierte Texturen, JPEG-Ausgabe |
| pytest | MIT | nur für die Entwicklung |

Die Lizenzen wurden im September 2026 aus den Paketmetadaten gelesen. Hat sich die Bedingung einer Komponente danach geändert, gilt die Quelle.
