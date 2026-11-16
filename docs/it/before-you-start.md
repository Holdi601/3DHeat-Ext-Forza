---
title: Prima di cominciare
nav_order: 2
lang: "it"
source: before-you-start.md
source_hash: "df38b4a84aaa"
nav_exclude: true
search_exclude: true
---
# Prima di cominciare {#before-you-start}

Non hai mai usato la riga di comando? Questa pagina ti porta da zero a uno
strumento funzionante in circa dieci minuti. Scrivi i comandi in una finestra
chiamata **terminale**, e lo strumento risponde con del testo.

## 1. Installa Python {#install-python}

1. Vai su [python.org/downloads](https://www.python.org/downloads/) e scarica
   **Python 3.10 o successivo**.
2. Esegui il programma di installazione. Nella prima schermata spunta **"Add python.exe to PATH"**,
   poi clicca **Install Now**.

Ti serve anche un Forza installato, tramite Steam o Microsoft Store (app Xbox). Lo
strumento lo trova da solo.

## 2. Scarica lo strumento {#get-the-tool}

- **Con git:** `git clone https://github.com/Holdi601/3DHeat-Ext-Forza.git`
- **Senza git:** sulla [pagina GitHub](https://github.com/Holdi601/3DHeat-Ext-Forza),
  clicca il pulsante verde **Code**, poi **Download ZIP**, e decomprimilo.

## 3. Apri un terminale nella cartella dello strumento {#open-a-terminal-in-the-tools-folder}

- In Esplora file apri la cartella che contiene `README.md`. Clicca la barra degli
  indirizzi, scrivi `cmd` e premi Invio. Si apre una finestra nera, già in quella cartella.
- Oppure apri **Windows Terminal** e vai lì con `cd`:

  ```
  cd "C:\Users\you\Downloads\3DHeat-Ext-Forza"
  ```

## 4. Installa lo strumento {#install-the-tool}

```
python -m pip install -e .
```

Così si installa il comando `heat3d-forza-maps` e ciò che gli serve:
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) (la libreria su cui
si basano i lettori), numpy, lz4 e Pillow. Dovresti vedere righe che finiscono con
`Successfully installed ...`.

Hai già una copia di GameFiles e non vuoi installarla di nuovo? Imposta
`HEAT3D_GAMEFILES` sulla sua cartella; anche una cartella GameFiles chiamata
`3DHeat-GameFiles` accanto a questa viene trovata da sola.

## 5. Controlla che funzioni {#check-that-it-works}

```
heat3d-forza-maps --help
```

Dovresti vedere `usage: heat3d-forza-maps [-h]` e un elenco di comandi (`identify`,
`list`, `extract`, `course`, ...). Questo significa che è andata: lo strumento è pronto.

## 6. Un primo percorso {#a-first-course}

Se registri i giri con FH Companion, dai a `course` il nome di un percorso così
come lo mostra la libreria:

```
heat3d-forza-maps course "Example Circuit"
```

Oppure dagli un file di giro (una qualsiasi delle forme in
[Input dei giri](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

```
heat3d-forza-maps course lap.json -o example.glb
```

Dice quale tracciato e quale gara ha trovato, di che cosa è fatto il terreno, che
cosa ci ha collocato sopra, e termina con `wrote example.glb (... bytes)`. Vedi
[Esportazione del percorso](course-export.md).

## Leggere gli esempi {#reading-the-examples}

- `<qualcosa>` è un **segnaposto**: scrivi invece il tuo valore, senza le parentesi
  angolari. `<lap file>` diventa, per esempio, `laps\my_lap.json`.
- `[--option]` tra parentesi quadre è **facoltativo**: omettilo se non ti serve.
- Un percorso con spazi richiede le **virgolette doppie**: `"C:\My Games\lap.json"`.

## Quando qualcosa va storto {#when-something-goes-wrong}

| Vedi | Cosa fare |
|---|---|
| `'python' is not recognized` | Python non è installato, oppure non era spuntato "Add to PATH". Esegui di nuovo il programma di installazione e spunta l'opzione, poi apri un nuovo terminale. |
| `'heat3d-forza-maps' is not recognized` | Il passo 4 è stato saltato, oppure è stato eseguito con un altro Python. Eseguilo di nuovo; `python -m heat3d_ext_forza --help` funziona comunque dalla cartella dello strumento. |
| `heat3d-forza-maps needs 3DHeat GameFiles: ...` | GameFiles non è installato. Esegui di nuovo il passo 4, oppure imposta `HEAT3D_GAMEFILES` su una cartella GameFiles. |
| `heat3d-forza-maps needs Pillow: ...` (o lz4, numpy) | Esegui il `pip install` indicato nella riga. |
| `no installed Forza track found` | Il gioco non è in una libreria Steam né in `C:\XboxGames`. Passa la cartella del suo tracciato con `--track` ([Come nasce un percorso Forza](course-forza-horizon.md#finding-the-installed-game)). |
| `none of the installed tracks (...) has terrain at x ..., z ...` | Il giro viene da un gioco o da una mappa che non è installata. |
| `can't open file` / `not found` con un percorso | Il percorso ha spazi senza virgolette, oppure c'è un errore di battitura. Mettilo tra virgolette doppie. |

Altri messaggi e le loro soluzioni:
[Risoluzione dei problemi](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html)
sul sito di GameFiles.
