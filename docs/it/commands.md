---
title: Comandi
nav_order: 3
lang: "it"
source: commands.md
source_hash: "32f5e35285be"
nav_exclude: true
search_exclude: true
---
# Comandi {#commands}

Ogni comando si esegue come `heat3d-forza-maps <comando> ...` (oppure, dalla cartella
dello strumento senza installarlo, come `python -m heat3d_ext_forza <comando> ...`).

| Comando | Richiede | Fa |
|---|---|---|
| [`course`](#course) | un giro | esporta il percorso attorno a quel giro |
| [`courses`](#courses) | una libreria di giri registrati | esegue `course` su ogni percorso che contiene |
| [`races`](#races) | un Forza installato | elenca ogni gara che il gioco definisce: cosa aggiunge, cosa nasconde, le location, lo stato della sua esportazione |
| [`terrain`](#terrain) | una cartella di tracciato Forza | ritaglia una regione tramite coordinate del mondo |
| [`cars`](#cars) | un Forza installato | ogni auto a basso dettaglio, in un unico file per la scheda Analisi di gara del visualizzatore |
| [`identify`](#identify) | un file | dice se è un `.minizip` di Forza o un modello ForzaTech, e cosa contiene |
| [`list`](#list) | un `.minizip` | elenca le sue voci |
| [`extract`](#extract) | un `.minizip` | scrive una voce su disco |

**Come leggere gli esempi:** `<x>` significa sostituiscilo con il tuo valore, senza le
parentesi angolari; `[...]` è facoltativo; un percorso con spazi va racchiuso tra
"virgolette doppie", per esempio `"C:\Games\My Game"`. Non l'hai mai usato? Vedi
[Prima di cominciare](before-you-start.md). La guida completa `--help` di ogni comando è nel
[Riferimento dei comandi](../cli-reference.md).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) esegue questo strumento
con i tuoi argomenti invariati per i suoi `course`, `courses`, `races`, `cars` e
`terrain` su un giro o un tracciato di Forza, e chiede ai suoi `identify`, `list` e
`extract` i file di Forza che i suoi lettori non conoscono. Per questo `course`
accetta anche `--level` e `--install` di GameFiles, e `list` ed `extract` accettano
`--key`: vengono accettati e non usati.

Ogni volta che il programma parte, può prima controllare se c'è una release più recente.
`HEAT3D_NO_UPDATE=1` disattiva questo controllo.

Sorgente: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py).

## Codici di uscita {#exit-codes}

| Codice | Significato |
|---|---|
| 0 | fatto |
| 1 | il lavoro non è riuscito: un giro illeggibile, un giro senza guida, nessun terreno sotto la guida, un percorso in `courses` che è fallito, un `.minizip` che non si può leggere o la cui lista di nomi non gli appartiene, una voce che non è nell'archivio |
| 2 | niente da leggere, oppure argomenti errati: nessun Forza installato, nessun tracciato sotto la guida, nessuna libreria di giri, un giro di un altro gioco, un file che non è di Forza, un percorso che non esiste, una dipendenza mancante (GameFiles, numpy, lz4, Pillow), `terrain` con entrambi o nessuno tra `--box` e `--route`, un argomento che argparse rifiuta |

Ogni errore è una riga (o due) sullo standard error, che dice cosa fare, non un
traceback di Python.

---

## course {#course}

```
heat3d-forza-maps course <giro> [-o FILE] [opzioni]
```

Esporta il percorso attorno a un giro: il suolo in una fascia su entrambi i lati
della guida, e ciò che vi sorge sopra, in un unico `.glb`. Il resto lo ricava da
solo: dove è installato il gioco, su quale dei suoi tracciati è stato guidato il
giro, e quale delle gare del gioco è. Vedi [Esportazione del percorso](course-export.md).

`<giro>` può essere uno qualsiasi di questi (dettagli in
[Input dei giri](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

- un file di giro: JSON di percorso, JSON di giro di FH Companion, JSON `heat3d-lap`, `.npz`, o `.csv` con colonne x, y, z
- una cartella di file di giro, cercata ricorsivamente (un intero percorso registrato)
- il **nome** di un percorso, cercato nella libreria di FH Companion in `%LOCALAPPDATA%\FHCompanion\laps`

### Opzioni {#options}

| Opzione | Predefinito | Significato |
|---|---|---|
| `-o`, `--out FILE` | `<nome del percorso>.glb` nella cartella corrente, oppure in `$HEAT3D_LEVELS/forza/courses/` se è impostata | dove scrivere; il nome viene scritto in minuscolo, e le sequenze di altri caratteri diventano `_` |
| `--margin M` | 80 | metri di suolo conservati su entrambi i lati della guida |
| `--texture-size {2048,1024,512}` | 2048 | pixel della texture del suolo per tassello di 512 m (2048 = 25 cm per pixel) |
| `--no-textures` | disattivato | solo colori piatti: un file molto più piccolo. Salta anche la divisione tra strada e banchina |
| `--season {summer,autumn,winter,spring}` | summer | le mappe del suolo e le texture dei modelli di quale stagione |
| `--no-placed` | disattivato | solo terreno: niente cordoli, barriere, cartelli, edifici |
| `--trees` | disattivato | colloca anche alberi, cespugli e oggetti da frantumare |
| `--detail-budget N` | automatico | un limite massimo di triangoli per tutto ciò che viene collocato; vedi [Livelli di dettaglio e budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html) |
| `--track DIR` | cercato | la cartella del tracciato (sotto `media\Tracks`, con `GeoChunk0.minizip`) se non si deve cercare nel gioco installato |
| `--game {forza,beamng,acrally}` | ciò che dice il file del giro, altrimenti `forza` | da quale gioco viene il giro (vedi sotto) |
| `--level`, `--install` | | accettati per la riga di comando di GameFiles, non usati |

### Quale gioco {#which-game}

Il gioco viene preso da `--game`, poi dal campo `game` di un file `heat3d-lap` (o
dalla riga di descrizione `# {...}` di un CSV), altrimenti è Forza. Una cartella
prende il gioco che i suoi file nominano, quando ne nominano uno solo; un file che
non ne nomina nessuno (un giro di FH Companion, `course.json`, un CSV senza riga di
descrizione) non conta.

| Valore | Cosa succede |
|---|---|
| inizia con `forza` | l'esportazione di Forza |
| `beamng` | rifiutato, codice di uscita 2: `export it with heat3d-beamng-maps course` |
| `assetto-corsa-rally` oppure `acrally` | rifiutato, codice di uscita 2: `export it with heat3d-acrally-maps course` |
| `assetto-corsa-evo` | rifiutato: "keeps all its content in one package obfuscated with a key, and this tool recovers none" |
| `iracing` | rifiutato: "tracks ship in a protected format that is not a file-extraction target" |
| qualsiasi altro | rifiutato: "there is no course reader for <game> yet" |

Gli ultimi tre suggeriscono anche le alternative: ricostruire il percorso dal gioco
(3DHeat GameCapture), oppure analizzare i giri senza un percorso, perché la scheda
Analisi di gara del visualizzatore disegna una strada a partire da essi.

### Esempi {#examples}

```
# Un percorso dalla libreria di FH Companion, per nome
heat3d-forza-maps course "Example Circuit"

# Un solo file di giro, una fascia più stretta, un file più piccolo
heat3d-forza-maps course lap.json -o example.glb --margin 40 --texture-size 1024

# Texture invernali, alberi compresi
heat3d-forza-maps course "Example Circuit" --season winter --trees

# Un tetto rigido di 500.000 triangoli collocati
heat3d-forza-maps course lap.json --detail-budget 500000

# Una cartella di tracciato data direttamente (gioco installato in un posto non cercato)
heat3d-forza-maps course lap.json --track "D:\Games\<Forza>\media\Tracks\<map>"
```

Cosa stampa un'esecuzione, su un tracciato inventato che i test costruiscono (su un
tracciato vero i numeri arrivano a centinaia di migliaia di triangoli, e dice quale
tracciato e quale gara ha trovato):

![esecuzione di course su un tracciato inventato](../assets/img/course-run.svg)

## courses {#courses}

```
heat3d-forza-maps courses [-o CARTELLA] [opzioni]
```

Esegue `course` su ogni cartella di percorso di una libreria di giri registrati,
scrivendo un `<nome>.glb` per ciascuna.

| Opzione | Predefinito | Significato |
|---|---|---|
| `-o`, `--out CARTELLA` | `courses`, oppure `$HEAT3D_LEVELS/forza/courses` se è impostata | la cartella in cui scrivere (creata se manca) |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la libreria di giri |
| `--only TEXT [TEXT ...]` | tutti | solo i percorsi i cui nomi di cartella contengono uno di questi testi (senza distinguere maiuscole e minuscole) |
| `--force` | disattivato | esporta di nuovo ciò che ha già un `.glb` |
| `--track DIR` | cercato | come per `course` |
| `--margin M` | 80 | come per `course` |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | come per `course` |

Cosa conta come cartella di percorso: una sottocartella diretta della libreria il cui
nome contiene ` (course_`, che è come FH Companion chiama i percorsi, per esempio
`Example Circuit (course_1200_3400_to_1175_3400)`. La parte da ` (course_` in poi
viene tolta dal nome.

Come si comporta un'esecuzione:

- Un percorso il cui `.glb` esiste già viene saltato (`kept`), a meno che non si dia `--force`, così un'esecuzione interrotta riprende da dove si era fermata.
- Un `.glb` scritto da una versione precedente, senza il layer e le location della gara (il suo `asset.extras.course_format` manca o è più basso di quello attuale), viene esportato di nuovo, come se `--force` fosse dato solo per lui.
- Due cartelle di percorso con lo stesso nome prima di ` (course_` (un registratore che ha dato a un nuovo percorso il nome di uno vecchio) non si sovrascrivono: la cartella creata per prima tiene `<nome>.glb`, l'altra viene scritta come `<nome>_<start>.glb`, dove `<start>` è il punto di partenza, con i segni meno scritti come `m` (per esempio `example_circuit_m120_m340.glb`).
- Un percorso che fallisce (giri illeggibili, memoria esaurita, nessun terreno...) viene segnalato come `FAILED`, e l'esecuzione prosegue.
- Alla fine stampa una tabella con stato, dimensione in MB, secondi impiegati e nome, poi `<n> of <total> courses in <cartella>`.
- Il codice di uscita è 1 se un percorso è fallito, 2 se non c'è nessuna libreria di giri.

```
heat3d-forza-maps courses -o courses --only circuit sprint --texture-size 1024
```

## races {#races}

```
heat3d-forza-maps races [-o CARTELLA] [--markdown FILE] [opzioni]
```

Elenca ogni gara che un Forza installato definisce, dalle sue definizioni dei percorsi
(vedi [Come nasce un percorso Forza](course-forza-horizon.md#which-race)), e controlla
le esportazioni in una cartella `courses` rispetto a esse. Legge il gioco e la libreria
di giri; non scrive nulla tranne la tabella facoltativa.

| Opzione | Predefinito | Significato |
|---|---|---|
| `-o`, `--out CARTELLA` | come per `courses` | la cartella su cui scrive `courses`, i cui file vengono controllati |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la libreria di giri |
| `--track DIR` | cercato | la cartella del tracciato, se non quella del gioco installato |
| `--markdown FILE` | nessuno | scrive anche la tabella lì, in Markdown |

Una riga per gara, e una per ogni percorso registrato guidato su di essa:

| Colonna | Significato |
|---|---|
| route | l'id del percorso |
| course | il percorso registrato abbinato, se c'è |
| own assets | copie che la gara aggiunge al mondo a percorrenza libera |
| drawn | di queste, le copie il cui modello il tracciato contiene |
| kinds | le copie aggiunte per tipo (barriere, oggetti di scena, decalcomanie, infrastrutture, ...) |
| not geometry | marcatori di spettatori e spline di collisione, contati |
| hidden | oggetti del mondo a percorrenza libera che la gara rimuove |
| venue | i modelli di suolo delle location che la linea AI della gara attraversa entro 10 m |
| export | `current`, `older format` (esportato di nuovo da `courses`), `not exported`, oppure vuoto per una gara senza percorso registrato |

Termina con un conteggio: `<n> races: <a> with assets of their own, <v> through a
venue, <d> driven in the lap library, <s> recorded courses to export again`.

```
heat3d-forza-maps races -o courses --markdown races.md
```

## terrain {#terrain}

```
heat3d-forza-maps terrain <cartella del tracciato> -o FILE (--box X0 Z0 X1 Z1 | --route FILE) [opzioni]
```

È il ritaglio con tutto specificato a mano: dai la cartella del tracciato e una
regione, non un giro. È utile quando l'area che vuoi è un riquadro e non un percorso di guida.

| Opzione | Predefinito | Significato |
|---|---|---|
| `<percorso>` | obbligatorio | una cartella di tracciato Forza sotto `media\Tracks` (con `GeoChunk*.minizip`) |
| `-o`, `--out FILE` | obbligatorio | il `.glb` da scrivere |
| `--box X0 Z0 X1 Z1` | | la regione, in metri del gioco (x e z, come li riporta la telemetria); angoli in qualsiasi ordine |
| `--route FILE` | | un JSON di percorso con `"bounds": {"min": [x, y, z], "max": [x, y, z]}`, come lo scrivono `heat3d_capture route` e `heat3d_capture laps`; letto come UTF-8, con o senza byte-order mark |
| `--margin M` | **100** | metri aggiunti attorno ai limiti di un percorso, e la larghezza del corridoio quando il percorso ha una linea |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | come per `course` |

Dai esattamente uno tra `--box` e `--route`, altrimenti il codice di uscita è 2. Con
`--route`, il ritaglio sono i `bounds` del percorso (`min`/`max`, x e z) allargati dal
margine. Se il file contiene anche almeno 10 posizioni, il ritaglio si restringe a un
corridoio di `--margin` metri attorno a esse, e i modelli collocati ricevono il loro
dettaglio in base alla distanza da quella linea. Con `--box`, viene conservato l'intero
riquadro, e il dettaglio va a ciò che sta più vicino al centro del riquadro.

L'altezza non fa mai parte del ritaglio. Un riquadro fuori dalla mappa, o in mare,
dà "no terrain there" (codice di uscita 1), non un errore sulle coordinate.

```
heat3d-forza-maps terrain "<gioco>\media\Tracks\<map>" --box 0 0 512 512 -o piece.glb
heat3d-forza-maps terrain "<gioco>\media\Tracks\<map>" --route route.json -o map.glb
```

## cars {#cars}

```
heat3d-forza-maps cars [-o FILE] [--game CARTELLA]
```

Ogni auto di un Forza installato al livello di dettaglio basso del gioco, in un unico
file per la scheda Analisi di gara del visualizzatore. Richiede secondi e scrive circa 5 MB. Vedi
[Auto di Forza](forza-cars.md).

## identify {#identify}

```
heat3d-forza-maps identify <percorso>
```

Legge il file e dice cos'è, dai suoi byte, non dalla sua estensione: un archivio
ForzaTech `.minizip` (la firma `PGZP`: versione, numero di voci e segmenti, e se la
lista `ChunkContentsMiniZip<n>.txt` che ne nomina le voci è accanto) oppure un modello
ForzaTech, `.modelbin` (versione, numero di chunk, i tag di chunk più comuni). Qualsiasi
altra cosa termina con codice 2 e `<file>: not a Forza file` sullo standard error. Vedi
[Ispezionare i file Forza](inspecting-files.md).

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

| Opzione | Predefinito | Significato |
|---|---|---|
| `<.minizip>` | obbligatorio | un `.minizip` ForzaTech, come il `GeoChunk0.minizip` di un tracciato |
| `--filter TEXT` | nessuno | solo i percorsi che contengono TEXT, senza distinguere maiuscole e minuscole |
| `--limit N` | 50 | stampa al massimo N voci (il totale viene sempre stampato) |
| `--key HEX` | nessuno | accettato, non usato: un `.minizip` non è cifrato |

Ogni riga mostra la dimensione non compressa, la compressione (`lz4`, `deflate` o
`stored`) e il percorso, come lo scrive la lista di nomi accanto all'archivio.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <voce> [--out FILE]
```

| Opzione | Predefinito | Significato |
|---|---|---|
| `<voce>` | obbligatorio | il percorso esattamente come lo stampa `list`, oppure `#<numero>` |
| `--out FILE` | il nome del file della voce (dopo l'ultimo `/` o `\`), nella cartella corrente | dove scrivere; le cartelle superiori vengono create |
| `--key HEX` | nessuno | accettato, non usato |

## Variabili d'ambiente {#environment-variables}

| Variabile | Effetto |
|---|---|
| `HEAT3D_LEVELS` | una cartella per ogni esportazione fatta senza `-o`: i percorsi in `<HEAT3D_LEVELS>/forza/courses/`, il pacchetto auto in `<HEAT3D_LEVELS>/forza/`. Se non è impostata, finiscono nella cartella corrente |
| `HEAT3D_GAMEFILES` | una cartella di 3DHeat GameFiles, quando GameFiles non è installato con pip |
| `HEAT3D_NO_UPDATE` | qualsiasi valore diverso da vuoto, `0`, `false`, `no` disattiva il controllo degli aggiornamenti |
| `LOCALAPPDATA` | dove vengono cercati la libreria di FH Companion e la cache degli aggiornamenti |
| `HEAT3D_COURSE` | solo per i test: il percorso usato dal test del cordolo sul gioco installato; vedi [Manutenzione](maintaining.md#tests) |
