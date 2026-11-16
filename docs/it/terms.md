---
title: Termini e licenza
nav_order: 12
lang: "it"
source: terms.md
source_hash: "e6bd7ab93f27"
nav_exclude: true
search_exclude: true
---
# Termini e licenza {#terms-and-licence}

## Il gioco è di Microsoft {#the-game-is-microsofts}

Forza Horizon e Forza Motorsport, i loro tracciati, le auto e le texture appartengono a
Microsoft (Playground Games e Turn 10 Studios). 3DHeat Forza non è affiliato a Microsoft,
Playground Games o Turn 10 Studios né da essi approvato. Forza e i nomi e marchi correlati
appartengono ai rispettivi proprietari.

Questo repository non contiene **nessun file dei giochi** né alcun percorso o auto o texture
ricavati da essi - niente risorse del gioco, niente codice del gioco, nessuna DLL - e lo
strumento **non scarica mai contenuti di gioco**: legge la copia **installata sulla tua
macchina**.

## Nessuna chiave: nessuna distribuita, nessuna recuperata {#no-keys-none-shipped-none-recovered}

Gli archivi `.minizip` di ForzaTech e i loro modelli, texture e file di posizionamento non
sono cifrati, e lo strumento non contiene chiavi, non ne recupera, non legge la memoria di
altri processi e non inietta nulla nel gioco. I giri vengono dalla telemetria che il gioco
pubblica da sé.

## L'output non è da ridistribuire {#output-is-not-for-redistribution}

Ciò che esce è geometria per il **contesto spaziale**: il suolo, la strada e ciò che le sta
accanto, ridotti a un budget, così i giri si possono analizzare sul posto. Resta sulla tua macchina.

- Tieni i `.glb` esportati dei percorsi, il file auto (`.h3dcars`) e le texture al loro
  interno per la tua analisi, sulla macchina su cui sono stati creati.
- Non pubblicare, condividere o vendere percorsi, auto, modelli o texture esportati.
- Il `.gitignore` del repository tiene fuori dal controllo di versione i file di gioco, le
  esportazioni, i giri e le registrazioni in base al tipo di file (`*.glb`, `*.h3dcars`,
  `*.minizip`, `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` e altri).

## I formati {#the-formats}

I formati di ForzaTech non sono documentati.
Nessuno dei lettori qui è derivato dal codice sorgente di un altro progetto: ogni offset è
stato misurato sui file, e il modo in cui ciascuno è stato stabilito è scritto in
[ForzaTech](reader-forzatech.md).

## Perché è uno strumento separato {#why-this-is-a-separate-tool}

Ogni lettore di gioco è un piccolo progetto a sé, con il proprio file di licenza, le proprie release e il proprio issue tracker: può essere installato, aggiornato, mantenuto - o ritirato su richiesta di un titolare dei diritti - da solo, senza toccare il visualizzatore o gli altri strumenti.

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) tiene i lettori
generici dei formati dei motori e le parti comuni; questo strumento tiene quelli di Forza.

Titolari dei diritti: aprite una issue su [github.com/Holdi601/3DHeat-Ext-Forza/issues](https://github.com/Holdi601/3DHeat-Ext-Forza/issues) - rispondiamo rapidamente e rimuoviamo qualsiasi cosa su richiesta.

## La licenza di questo strumento {#this-tools-licence}

Tutto ciò che è stato scritto per questo repository è sotto licenza **MIT**
([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSE)): usalo, cambialo,
distribuiscilo, anche a scopo commerciale.

Pacchetti di terze parti, tutti permissivi ([`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSES.md)):

| Pacchetto | Licenza | Usato per |
|---|---|---|
| 3DHeat GameFiles | MIT | lo scrittore glTF, i file dei giri, il corridoio, i tipi di suolo, il budget di dettaglio, le librerie Steam |
| numpy | BSD-3-Clause | decodifica delle mesh |
| lz4 | BSD-3-Clause | i blocchi LZ4 degli archivi `.minizip` |
| Pillow | MIT-CMU (HPND) | texture a compressione a blocchi, output JPEG |
| pytest | MIT | solo per lo sviluppo |

Le licenze sono state lette dai metadati dei pacchetti nel settembre 2026. Se i termini di un
componente sono cambiati dopo, fa fede la sorgente.
