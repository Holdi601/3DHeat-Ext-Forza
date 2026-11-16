---
title: Regeln und Lizenzen
nav_order: 12
lang: "de"
source: terms.md
source_hash: "6c61ae2ba60f"
nav_exclude: true
search_exclude: true
---
# Regeln und Lizenzen {#terms-and-licence}

Diese Seite hält fest, was die Lizenzen sagen. Sie ist keine Rechtsberatung.

## Das Spiel gehört Microsoft {#the-game-is-microsofts}

Forza Horizon und Forza Motorsport, ihre Strecken, Autos und Texturen gehören Microsoft (Playground Games und Turn 10 Studios), die dieses Projekt nicht unterstützen. Dieses Repository enthält **keine Datei des Spiels** und keine Strecke, kein Auto und keine Textur, die aus einer solchen Datei gemacht wurde. Das Werkzeug **lädt nie Spielinhalte herunter**: Es liest die Kopie, die **auf deinem Rechner installiert** ist.

Was du ihm vorgibst, bleibt deine Verantwortung. Spiele haben eigene Lizenzbedingungen, und EULAs verbieten oft Reverse Engineering. Das sind durchsetzbare Verträge, und die Pflicht liegt bei der Person, die das Werkzeug ausführt. Keine Gestaltung hier nimmt sie ihr ab.

## Keine Schlüssel: keiner mitgeliefert, keiner wiederhergestellt {#no-keys-none-shipped-none-recovered}

**Es liest Container.** Das Lesen eines Archivformats ist gewöhnliche Dateiverarbeitung. ForzaTechs `.minizip`-Archive und ihre Modelle, Texturen und Platzierungsdateien sind nicht verschlüsselt. Das Werkzeug enthält keinen Schlüssel, stellt keinen wieder her, liest keinen Speicher eines anderen Prozesses und schleust nichts in das Spiel ein. Die Runden kommen aus der Telemetrie, die das Spiel selbst veröffentlicht.

## Die Ausgabe ist nicht zur Weitergabe gedacht {#output-is-not-for-redistribution}

Was herauskommt, ist Geometrie für **räumlichen Kontext**: der Boden, die Straße und was daneben steht, auf ein Budget verkleinert, damit Runden an Ort und Stelle analysiert werden können. Es ist das Wenigste, was die Archive enthalten, und es ist trotzdem Inhalt des Herausgebers.

- Behalte exportierte `.glb`-Strecken, die Autodatei (`.h3dcars`) und die Texturen darin für deine eigene Analyse, auf dem Rechner, auf dem sie entstanden sind.
- Veröffentliche, teile oder verkaufe exportierte Strecken, Autos, Modelle oder Texturen nicht.
- Die `.gitignore` des Repositorys hält Spieldateien, Exporte, Runden und Aufzeichnungen nach Dateityp aus der Versionsverwaltung heraus (`*.glb`, `*.h3dcars`, `*.minizip`, `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` und weitere).

## Die Formate {#the-formats}

ForzaTechs Formate sind nicht dokumentiert. Sie zu lesen ist Reverse Engineering eines Containers. Keiner der Leser hier ist vom Quellcode eines anderen Projekts abgeleitet: Jeder Offset wurde an den Dateien gemessen, und wie jeder bestimmt wurde, steht auf [ForzaTech](reader-forzatech.md).

## Warum dies ein eigenes Werkzeug ist {#why-this-is-a-separate-tool}

Die Leser der Spiele jeder Firma liegen in ihrem eigenen Repository. So betrifft eine Lizenzfrage oder ein Löschantrag zu einem Spiel nur das Werkzeug dieses Spiels. [3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) enthält die generischen Leser für Engine-Formate und die gemeinsame Infrastruktur. Dieses Werkzeug enthält die Leser für Forza. Müsste dieses Repository verschwinden, verschwindet mit ihm nichts anderes.

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
