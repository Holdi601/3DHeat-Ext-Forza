---
title: Ispezionare i file Forza
nav_order: 7
lang: "it"
source: inspecting-files.md
source_hash: "e6cee3695640"
nav_exclude: true
search_exclude: true
---
# Ispezionare i file Forza: `identify`, `list`, `extract` {#inspecting-forza-files-identify-list-extract}

**In parole semplici:** un tracciato di Forza è conservato in pochi file d'archivio molto
grandi. Questi tre comandi dicono cos'è un file, mostrano cosa contiene un archivio, e ne
copiano fuori una cosa. Non ti servono per esportare un percorso; servono per guardarci dentro.

## identify {#identify}

```
heat3d-forza-maps identify <file>
```

1. **Trova un file.** Gli archivi di un tracciato sono in
   `<cartella del gioco>\media\Tracks\<map>\`: `GeoChunk0.minizip` fino a `GeoChunk3.minizip`,
   ciascuno con un `ChunkContentsMiniZip<n>.txt` accanto.
2. **Eseguilo.** Esempio (numeri sintetici):

   ```
   > heat3d-forza-maps identify GeoChunk0.minizip
   GeoChunk0.minizip  (12,345,678,901 bytes)
     ForzaTech .minizip archive, version 101
       entries    98,304 in 192 segments
       names      ChunkContentsMiniZip0.txt
   ```

   L'archivio stesso non conserva nomi (vedi [ForzaTech](reader-forzatech.md)). `names`
   indica quale lista li nomina; se non ce n'è una accanto, le voci vengono identificate
   per numero (`#0`, `#1`, ...), e una lista il cui numero di righe non coincide con quello
   delle voci viene segnalata come non appartenente.
3. **Un modello** estratto da un archivio (`.modelbin`) viene anch'esso nominato: la sua
   versione, quanti chunk ha, e i tag di chunk più comuni. Il contenuto dei chunk non viene
   decodificato qui.

Qualsiasi cosa che non sia nessuna delle due cose scrive `<file>: not a Forza file` sullo
standard error ed esce con codice 2. Il formato viene deciso dai byte, mai dall'estensione.

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

```
> heat3d-forza-maps list GeoChunk0.minizip --filter autoterrain --limit 3
1,024 entries matching 'autoterrain'
        65,536  lz4    scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin
        61,440  lz4    scene\tbheightfield\autoterrain_x0_z0_cluster001.i.modelbin
        70,112  lz4    scene\tbheightfield\autoterrain_x0_z1023_cluster000.i.modelbin
  ... 1,021 more
```

Ogni riga mostra la dimensione decompressa, la compressione (`lz4`, `deflate` o `stored`), e il
percorso come lo scrive la lista di nomi, con il prefisso della macchina di build tolto e le
barre rovesciate del gioco mantenute. `--filter` cerca in qualsiasi parte del percorso,
senza distinguere maiuscole e minuscole; `--limit` (predefinito 50) limita le righe, non il conteggio.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <voce> [--out FILE]
```

```
> heat3d-forza-maps extract GeoChunk0.minizip "scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin"
65,536 bytes -> autoterrain_x0_z0_cluster000.i.modelbin
```

La voce è il percorso esattamente come lo stampa `list`, oppure `#<numero>`. Senza `--out`
viene scritta nella cartella corrente con il suo nome di file. Una voce che non è nell'archivio
esce con codice 1 (`not in the archive: ...`).

Quello che estrai dagli archivi del gioco è il contenuto del gioco: serve per il tuo
sguardo all'interno, non per essere passato ad altri ([Termini](terms.md)).
