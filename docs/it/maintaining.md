---
title: Manutenzione della documentazione
nav_order: 91
lang: "it"
source: maintaining.md
source_hash: "5a5a685c8282"
nav_exclude: true
search_exclude: true
---
# Manutenzione di questa documentazione {#maintaining-these-docs}

Una lista di controllo per ogni rilascio, perché le pagine non restino mai indietro rispetto al codice.

1. **Rigenera il riferimento.** `python tools/gen_docs_reference.py` riscrive il
   [Riferimento dei comandi](../cli-reference.md) a partire dal `--help` del programma e dai nomi
   delle parti. `python tools/gen_docs_reference.py --check` esce con 1 quando la pagina
   committata è vecchia.
2. **Ridisegna le immagini del terminale** quando cambia un output:
   `python tools/terminal_pictures.py` esegue `cars --help` e `course` sul tracciato inventato che
   costruiscono i test. Mai un tracciato vero o un giro vero.
3. **Elenca ciò che è cambiato.** `git log v<VERSION>..HEAD --oneline`, dove `<VERSION>` è l'ultima
   versione rilasciata (il file `VERSION` al rilascio). Dai a ogni nuova funzione, opzione e output
   un posto in una pagina, e una riga nella sezione **Docs** di
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/CHANGELOG.md).
4. **Revisione indipendente.** Qualcuno che non ha scritto le pagine legge il README e ogni pagina
   cambiata, immagini comprese, tre volte: come un principiante che non ha mai usato un terminale,
   come un bambino di 8 anni, e come un esperto che controlla ogni opzione rispetto a `--help`.
   Gli esempi usano solo nomi e numeri inventati.
5. **Correggi** tutto ciò che la revisione trova.
6. **Traduzioni.** Ogni pagina tradotta registra l'hash della pagina inglese da cui è stata fatta.
   Ritraduci le pagine la cui fonte inglese è cambiata, poi rivedi ogni lingua: testo chiaro,
   etichette dei diagrammi corrette, le stesse parole dell'interfaccia tradotta del visualizzatore.
7. **Esegui i test** (qui sotto).
8. **Pubblica** solo dopo il via libera del proprietario.

## Test {#tests}

```
python -m pip install -e .[test]
python -m pytest
```

Tutto gira su dati inventati: archivi, modelli, texture, file di posizionamento e intere cartelle
di tracciato sono scritti dai test stessi (`tests/forza_fixtures.py`), e `course` viene eseguito
dall'inizio alla fine su uno di essi, partendo solo da un giro, trovando il gioco inventato come
trova uno vero.

Alcuni test leggono anche un Forza installato, quando c'è, e saltano quando non c'è: ogni archivio di
modelli forma una catena di chunk chiusa, ogni auto sta sulle sue ruote, e i cordoli giacciono sul
suolo accanto alla linea guidata dei percorsi registrati più guidati della libreria di FH Companion.
`HEAT3D_COURSE=<cartella del percorso>` sceglie il percorso per quest'ultimo. Leggono il gioco; non
scrivono mai nel repository.

I test hanno bisogno di 3DHeat GameFiles: installato, oppure trovato nel modo in cui lo trova il
comando (`HEAT3D_GAMEFILES`, la cartella `gamefiles` di un checkout di 3DHeat, oppure una cartella
`3DHeat-GameFiles` accanto a questa).

## Traduzioni: i comandi {#translations-the-commands}

Il sito è tradotto nelle 40 lingue del visualizzatore 3DHeat: l'inglese in `docs/`, ogni altra lingua
in `docs/<lang>/` con gli stessi nomi di file. `tools/docs_i18n.py` tiene la contabilità:

```bash
python tools/docs_i18n.py hashes             # dopo ogni modifica all'inglese: registra l'hash di ogni pagina
python tools/docs_i18n.py svg-strings        # dopo ogni modifica alle immagini: le etichette da tradurre
python tools/docs_i18n.py status             # per lingua: pagine aggiornate, vecchie, mancanti
python tools/docs_i18n.py todo --lang de     # le pagine tedesche da (ri)tradurre
python tools/docs_i18n.py svg-build --lang de    # le immagini tedesche da docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # timbra le pagine tedesche con l'hash inglese
python tools/docs_i18n.py check              # esce con 1 quando hash o etichette sono vecchi
```

Traduci solo ciò che elenca `todo`: lascia intatti Markdown, link, codice, nomi di file e di colonne,
e traduci i titoli e le descrizioni delle immagini, usando le parole proprie del visualizzatore 3DHeat
per i suoi pulsanti e pannelli (la sua `src/i18n/locales/<lang>/`). Le pagine di riferimento generate
e le immagini del terminale restano in inglese. Sul sito, una traduzione non aggiornata lo dice e
rimanda alla pagina inglese; una traduzione mancante ricade sull'inglese. Il menu delle lingue
nell'intestazione e il reindirizzamento alla lingua del browser nella home arrivano da `docs/_includes/`.
