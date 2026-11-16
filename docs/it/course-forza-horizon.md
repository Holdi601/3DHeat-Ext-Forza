---
title: Come nasce un percorso Forza
nav_order: 1
lang: "it"
source: course-forza-horizon.md
source_hash: "ce7adab4b167"
nav_exclude: true
search_exclude: true
---
# Come nasce un percorso Forza {#how-a-forza-course-is-made}

L'esportazione di Forza legge il tracciato direttamente dagli archivi ForzaTech del
gioco: il terreno con strada, banchina ed erba distinti tra loro, una texture del suolo
cotta dalle mappe del suolo del gioco stesso, e ogni modello collocato con la propria
texture (cordoli, guardrail, muri di pneumatici, cartelli, oggetti di scena, edifici).
Trova anche quale delle gare del gioco è stata guidata sul giro, e aggiunge ciò che il
gioco mette in campo per quella gara soltanto (il suo layer di evento: barriere, tende,
portali, tribune, bandiere), e il suolo di qualsiasi location che la guida attraversa,
come il pavimento di uno stadio.

```
heat3d-forza-maps course "Example Circuit"
heat3d-forza-maps course lap.json -o course.glb --season winter
heat3d-forza-maps courses -o courses
heat3d-forza-maps terrain "<gioco>\media\Tracks\<map>" --route lap.json -o map.glb
```

Fonti: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py) (`export_course`, `_write_course`),
[`forzainstall.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzainstall.py),
[`forzaterrain.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaterrain.py),
[`forzatexture.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzatexture.py),
[`courseexport.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/courseexport.py),
[`forzaplacement.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaplacement.py),
[`forzamaterial.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzamaterial.py),
[`forzaroute.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/forzaroute.py).
I formati dei contenitori stessi sono su [ForzaTech](reader-forzatech.md).

## Trovare il gioco installato {#finding-the-installed-game}

Nessuno dovrebbe dover digitare un percorso come
`D:\Games\steamapps\common\<Forza>\media\Tracks\<map>`, quindi il percorso viene ricavato da solo:

1. **Librerie Steam.** Il file `config\libraryfolders.vdf` di Steam viene letto da
   `C:\Program Files (x86)\Steam` o `C:\Program Files\Steam`, e ogni voce `"path"` al suo
   interno è una libreria. In `steamapps\common` di ogni libreria si cerca.
2. **Microsoft Store.** Si cerca in `C:\XboxGames`, se esiste. Lì il gioco sta un livello più
   in basso, in `<gioco>\Content`.
3. Una **cartella di gioco** è qualsiasi figlio di queste cartelle che abbia una cartella
   `media\Tracks`, comunque si chiami.
4. Una **cartella di tracciato** è qualsiasi cartella sotto `media\Tracks` che contenga un
   `GeoChunk0.minizip`. Conta in base al suo contenuto, non al nome, quindi un tracciato con
   un nome che nessuno ha mai visto viene comunque trovato.

Se il gioco si trova altrove, passa la cartella del tracciato con `--track`; vedi
[Risoluzione dei problemi](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html#finding-the-game)
("no installed Forza track found").

`--track <cartella>` salta tutto questo.

Una cartella di tracciato contiene ciò che l'esportazione legge:

| File | Cos'è |
|---|---|
| `GeoChunk0.minizip` ... `GeoChunk3.minizip` | gli archivi: ogni modello, texture e file di posizionamento, senza nomi al loro interno |
| `ChunkContentsMiniZip0.txt` ... `3.txt` | una riga per voce d'archivio, nell'ordine delle voci: l'unica fonte dei nomi |
| `AssetManifest.xml` | ogni texture che il tracciato contiene, con l'hash con cui i materiali la richiamano |

## Quale tracciato {#which-track}

Un gioco contiene più di una cartella di tracciato (la mappa open world, un garage o due).
Quella giusta viene scelta per **coordinate, non per nome**:

- La domanda è il riquadro di delimitazione del giro, allargato da `--margin`.
- Per ogni cartella di tracciato vengono letti come testo, senza aprire alcun archivio, i
  quattro manifesti `ChunkContentsMiniZip*.txt`. Ogni nome di tassello del terreno
  (`autoterrain_x<X>_z<Z>..._cluster<N>.i.modelbin`) porta la sua posizione nella griglia.
  Lo strumento conta quanti tasselli distinti cadono dentro il riquadro.
- Vince il tracciato con più tasselli. Se nessun tracciato ne ha, l'esportazione si ferma con
  "none of the installed tracks (...) has terrain at x ..., z .... Those are the game's own
  metres, as its telemetry reports them."

Un tracciato intero risponde in meno di un secondo. Una corrispondenza per nome potrebbe
scegliere la mappa sbagliata, e una mappa sbagliata sembra plausibile quanto quella giusta.

La console scrive `on <tracciato>, in <cartella del gioco>`.

## Quale gara {#which-race}

Il gioco distribuisce ciascuna delle sue gare come un percorso con un numero, il suo
**id del percorso**. Ogni percorso è legato a due file:

| File | Cosa contiene |
|---|---|
| `media\OpenWorld\<map>\AITracks\Route<id>.owt` | la linea di guida AI della gara: un nodo di 56 byte a partire dal byte `0x60`, il numero di nodi a `0x24`, ogni nodo inizia con la sua posizione (x, y, z) in metri del gioco |
| `media\Stripped\gs\<map>\routedefinitions.zip` | un `route<id>_<map>.rtd` per gara: XML semplice che elenca ciò che la gara aggiunge al mondo e ciò che toglie (vedi [Il layer della gara](#the-races-own-layer)) |

Il giro viene abbinato a un percorso confrontandolo con ogni linea AI il cui riquadro si
sovrappone a quello del giro:

- Da ogni campione del giro, la distanza dal punto più vicino della linea; e da ogni punto
  della linea, la distanza dal campione del giro più vicino.
- Le due mediane vengono sommate. Vince il percorso con la somma più piccola, se la somma è
  sotto **30 m** (`MATCH`).
- Servono entrambe le direzioni: uno sprint breve giace lungo un percorso lungo che usa la
  stessa strada, e un giro lungo copre un percorso corto.

La console scrive `the game's route <id> (driven line within <n> m of it)`, oppure che nessun
percorso corrisponde. Senza corrispondenza viene collocato solo il mondo a percorrenza libera.

## Terreno {#terrain}

Come viene trovato il terreno (in `forzaterrain.py`):

- I manifesti indicano il terreno come un indice spaziale:
  `scene\tbheightfield\autoterrain_x-2046_z1023_cluster012.i.modelbin`.
- I due numeri sono coordinate di griglia che **avanzano di 1023**, e ogni passo della griglia
  è un tassello di **512 m**. Il tassello `x-2046` è `-2046 / 1023 = -2`, che inizia a
  `-2 * 512 = -1024` m. Se si leggono i nomi come metri, ogni ricerca sbaglia di un fattore
  due e restituisce comunque terreno, preso da un'altra parte della mappa.
- Un tassello può comparire tre volte: normale, `_cb` e `_ul`. Tutti e tre coprono lo stesso
  suolo. Se ne prende uno per tassello, in quell'ordine di preferenza, perché unirli
  triplicherebbe la geometria in superfici coincidenti.
- Un tassello viene letto solo se tocca il riquadro del giro **e** il corridoio. Un tassello
  che il corridoio non tocca non viene mai decompresso.
- Ogni `.modelbin` di un tassello scelto viene decodificato al **livello di dettaglio 0
  soltanto**. Un tassello contiene quattro livelli sullo stesso suolo, ed esportarli tutti
  metterebbe lo stesso metro quadrato quattro volte nel file.
- Ogni mesh porta con sé la propria scala e il proprio bias nel mondo, quindi un tassello
  finisce dove lo mette il gioco, senza alcuna trasformazione dell'istanza. Vengono tenuti i
  triangoli la cui impronta si sovrappone al riquadro, poi solo quelli che arrivano nel corridoio.
- Una mesh in un formato che il lettore rifiuta viene saltata e contata
  (`N meshes could not be read`), così un risultato scarso spiega il motivo.

Il riepilogo del terreno stampa il numero di vertici, di triangoli, di mesh e di tasselli, e
l'estensione x/y/z.

### Strada, banchina, terreno, segnaletica, acqua {#road-verge-terrain-markings-water}

I nomi dei materiali non dicono dove sia la strada. Intorno a un circuito, il 94% del suolo
usa un materiale con shader stradale, perché il terreno vicino alla strada viene disegnato
con esso, e lo shader decide asfalto o erba pixel per pixel. Quindi:

| Tipo | Deciso da |
|---|---|
| striscia di strada | il **layout dei vertici**: le strisce di strada sono l'unico suolo con un secondo set di UV (canale 1); un triangolo i cui tre vertici li hanno tutti è strada |
| asfalto o banchina | dentro una striscia di strada, la **maschera di asfalto** del tassello nel baricentro del triangolo: 0,5 o più è `road`, meno è `verge` |
| segnaletica | nome del materiale che corrisponde a `whiteline`, `yellowline` o `decal` |
| segni di pneumatici | nome del materiale che corrisponde a `tyremark` o `skid` (controllato prima della segnaletica, perché i segni di pneumatici sono chiamati `tyremark_decal_*`) |
| acqua | nome del materiale che corrisponde a `water`, `lake`, `river`, `paddy`, `ocean` o `sea` |
| terreno | tutto il resto |

Misurato sui giri registrati sul circuito di prova, quasi tutti i campioni cadono su
triangoli di striscia di strada, e la grande maggioranza sulla parte di asfalto una volta che
la maschera ha separato la banchina.

La maschera di asfalto esiste solo quando le texture del suolo vengono cotte. Con
`--no-textures`, o per un tassello le cui mappe mancano, le strisce di strada restano intere
come `road` e non si separa alcuna banchina. Le mappe mancanti costano dettaglio, mai geometria.

### Le superfici dipinte vengono sollevate {#painted-layers-are-lifted}

La segnaletica e i segni di pneumatici sono distribuiti come propri triangoli che giacciono
esattamente sulla strada. Il gioco li disegna con un offset di profondità. Disegnati così
come sono, strada e vernice si contendono ogni pixel. L'esportazione dà a ogni parte di
segnaletica e di segni di pneumatici una propria copia dei vertici, sollevata di **5 cm**
(`DECAL_LIFT`) lungo la normale della superficie, così la strada sotto non viene sollevata con loro.

### Normali {#normals}

Le normali del terreno vengono dall'archivio. La componente x della normale è memorizzata come
quarto short della posizione, e y e z nell'attributo `NORMAL` (vedi [ForzaTech](reader-forzatech.md)).
Se anche un solo vertice dell'estrazione non ha una normale, le normali di tutto il suolo
vengono calcolate dai triangoli.

## La texture del suolo {#the-ground-texture}

Ogni tassello del terreno distribuisce tre mappe che coprono il suo quadrato di 512 m, in
cinque risoluzioni (da `_quality1` a `_quality5`, la più grande da 2048 px, cioè 25 cm per pixel):

| Mappa | Schema del nome del file | Cosa contiene (come misurato) |
|---|---|---|
| principale | `mainmap_x<X>_z<Z>_x<season>x_diff` | R, G: normale di dettaglio (x, z). A: più bassa sull'asfalto e sul terreno accidentato |
| secondaria | `submap_x<X>_z<Z>_x<season>x_diff` | pesi degli strati. B: alta sull'asfalto (239 sulla linea guidata, 165 accanto) |
| lucentezza | `autoglossf0_x<X>_z<Z>_x<season>x_glos` | G: bassa sull'asfalto (147 contro 215). B: sale nei boschi |

Nessuna di queste è una fotografia a colori. Sono gli ingressi con cui lo shader del terreno
del gioco miscela i suoi strati di materiale, e quegli strati non vengono decodificati. Quindi
la texture cotta è **una interpretazione, non una copia dell'aspetto del gioco**. Mantiene
*dove* sta ciascun tipo di suolo, a 25 cm, e lo dipinge con colori fissi:

| Suolo | RGB lineare | Peso |
|---|---|---|
| erba (corta, vicino alla pista) | 0.30, 0.44, 0.18 | la base |
| terreno accidentato (più lontano) | 0.40, 0.42, 0.22 | `smoothstep(88 -> 72, main.A) * (1 - asphalt)` |
| bosco | 0.13, 0.23, 0.10 | `smoothstep(4 -> 24, gloss.B)` |
| asfalto | 0.20, 0.20, 0.21 | `smoothstep(188 -> 228, sub.B) * smoothstep(200 -> 168, gloss.G)` |

Per l'asfalto devono concordare entrambe le mappe. Da sola, una delle due lascia un'aria
grigia macchiata nell'erba dove la compressione a blocchi fa anelli. Il risultato viene
ombreggiato dalla normale di dettaglio della mappa principale contro una luce fissa
(`0.55 + 0.6 * lambert`), così i bordi dei cordoli, le scarpate e i solchi si leggono come
rilievo, e viene scritto come sRGB a 8 bit.

Orientamento: la riga 0 dei pixel è il bordo **nord** del tassello (z più grande), la colonna
0 il suo bordo **ovest** (x più piccolo). Lo si è trovato proiettando i giri registrati sulla
maschera dell'asfalto in tutti gli otto modi in cui un quadrato può essere ribaltato o ruotato.
Esattamente uno dei modi li mette sull'asfalto. Le UV ne derivano: `u = (x - x0) / 512`,
`v = 1 - (z - z0) / 512`.

Le mappe vengono lette alla migliore risoluzione disponibile fino alla qualità 5 e
ricampionate alla dimensione della mappa principale. Se l'immagine a colori è più grande di
`--texture-size`, viene poi ridotta a quella dimensione con filtro Lanczos. La maschera
dell'asfalto resta sempre a piena risoluzione, perché decide la geometria. `--season` sceglie
le mappe `x<season>x`. Un tassello senza mappe per quella stagione viene disegnato a colori
piatti, e la console segnala `N without maps`.

## Modelli collocati {#placed-models}

Il terreno porta con sé la sua posizione nel mondo. Nient'altro la porta. Dove si trova ogni
copia di un modello è registrato nei file di posizionamento `.pgeo`, uno per categoria per
cella spaziale: `scene\proc\cellsize\<size>\<x>_<z>\c<size>_<category>_....pgeo`. La struttura
dei record è descritta in [ForzaTech](reader-forzatech.md#placement-files-pgeo).

### Cosa viene letto {#what-is-read}

- I file di posizionamento vengono filtrati **per nome**: la dimensione della cella e la sua
  posizione nel percorso danno il quadrato della cella (da `x * size` a `(x + 1) * size`), e
  vengono aperte solo le celle che si sovrappongono al riquadro del giro e che appartengono a
  una categoria richiesta.
- Categorie predefinite: `barriers`, `props`, `signs`, `buildings`, `infrastructure`,
  `bridges`, `rocks`, `evolving`. `--trees` aggiunge `trees`, `bushes` e `smashables`. Queste
  non vengono mai lette: `grasstemplate`, `crowdtemplate` e `cwdspline` (erba e spettatori: il
  gioco le disegna come sprite animati, non hanno geometria).
- Ogni file appartiene a un **layer**, letto dal suo nome dopo `c<size>_<category>_`. Una
  parola di livello di dettaglio (`do`, `so`, `ulc`, `ulp`, `cwd`) e un eventuale numero di
  sezione indicano il mondo a percorrenza libera. Qualsiasi altra cosa è un layer che il gioco
  attiva: un layer di runtime (`rt_0`), un'attività (`_tag_<name>_`), un oggetto collezionabile,
  qualsiasi cosa archiviata sotto `evolving`. Un layer che nomina dei percorsi (`rt_x<id>`, per
  esempio `rt_x1023_x2201`) appartiene solo a quelle gare, e viene letto solo quando il giro ha
  abbinato una di esse. Vedi [Layer attivati](#switched-on-layers).
- Una copia viene tenuta se la sua posizione sta dentro il riquadro e dentro il corridoio.
  Le ripetizioni esatte (stessa posizione e orientamento al millimetro, elencate da due celle
  vicine) vengono unite.
- I **cordoli** sono oggetti di scena il cui nome di modello inizia con `road_gen_rum` (strisce
  vibranti). Vengono scritti come `ground:kerbs`, mai semplificati e mai lasciati fuori, perché
  un giro viene misurato proprio su di essi.

| Categoria | Parte | Colore di riserva (senza texture) |
|---|---|---|
| cordoli | `ground:kerbs` | 0.60, 0.12, 0.10 |
| barriere | `structure:barriers` | 0.50, 0.50, 0.50 |
| oggetti di scena | `structure:props` | 0.45, 0.35, 0.25 |
| cartelli | `structure:signs` | 0.70, 0.70, 0.70 |
| edifici | `structure:buildings` | 0.55, 0.52, 0.48 |
| infrastrutture | `structure:infrastructure` | 0.45, 0.45, 0.47 |
| ponti | `structure:bridges` | 0.45, 0.45, 0.45 |
| rocce | `structure:rocks` | 0.30, 0.28, 0.25 |
| oggetti frantumabili | `structure:smashables` | 0.12, 0.22, 0.06 |
| alberi, cespugli | `structure:trees` | 0.10, 0.20, 0.05 |

### La geometria del modello {#the-models-geometry}

Un nome collocato `<model>_3D` si riferisce ai file del modello `<model>_cluster###.i.modelbin`
(fino a una dozzina). Ogni triangolo porta una maschera dei livelli di dettaglio a cui appartiene:

- I livelli di un modello sono i suoi triangoli marcati esplicitamente per quel livello. I
  livelli vanno in sequenza da 0, il più fine per primo.
- I triangoli marcati `0xFFFF` (ogni livello) sono i pezzi che si rompono, come i pali di un
  guardrail o i singoli pneumatici di una pila. Coprono tutto il modello, e il gioco li disegna
  al suo posto quando è stato fatto a pezzi. Vengono usati solo per un modello senza un livello
  marcato esplicitamente.
- Le sotto-mesh il cui shader di materiale è un **decal** proiettato vengono lasciate fuori.

Ogni copia viene collocata con la sua posizione, i suoi assi x e y dal record (z = x cross y),
e la sua scala. Le normali vengono trasformate con l'inversa della scala.

### Quale texture {#which-texture}

Un materiale non nomina le sue texture. Le elenca come hash, e l'`AssetManifest.xml` del
tracciato associa ogni hash (`SourceHash`) a un nome di texture. Viene letta solo la sezione
`<Textures>`, e la lettura si ferma a `</Textures>` in un file che può arrivare a decine di
megabyte. Poi:

1. Lo slot `0x88B483AA` è il colore di base nello shader ambientale standard (ogni materiale
   campionato). Se il materiale vi lega una texture, quella viene usata.
2. Altrimenti decide il tipo della texture stessa, cioè la parola prima del suo GUID:
   `_bclr_`, poi `_diff_`, poi `_colour_`.
3. Le mappe del terreno (`mainmap`, `submap`, `autogloss`) e le palette di tinta (`tint`,
   `worldtint`) non colorano mai un modello.

Quindi un modello è colorato da ciò che il suo materiale lega, non da una texture chiamata
come il modello. Per esempio, `bar_rur_armco_crct_02_c` usa la texture di `..._02_a`.

La texture viene letta dagli archivi alla risoluzione più piccola che sia almeno **256 px** su
un lato (`MODEL_TEXTURE`), ridotta a 256 se più grande, e memorizzata come JPEG RGB nel `.glb`.
Il colore di un guardrail a 256 px per quattro metri è di 1,6 cm per pixel, e circa 80 di
queste texture entrano nell'atlante del visualizzatore accanto alle tessere del suolo.

**Stagioni.** `--season` sostituisce una texture con il suo gemello stagionale per nome,
ignorando il GUID (`..._xsummerx_bclr` diventa `..._xwinterx_bclr`, oppure `..._bclr` diventa
`..._winter_bclr`), quando il tracciato ne ha uno. Con `--season winter`, il materiale invernale
di una sotto-mesh viene usato anche dove la sua tabella di varianti lo indica.

**Varianti.** Il record di una sotto-mesh inizia con una tabella di materiali `(summer,
winter)`, uno per ogni aspetto che una copia può avere: cinque stampe per un cartellone, sei
colori di vernice per una pila di pneumatici. Ogni record di posizionamento indica quale
variante porta quella copia. Una sotto-mesh con meno varianti del modello ripete le sue.

**Il blocco segnaposto.** Gli atlanti condivisi degli edifici riservano un blocco RGB solido
(255, 64, 0) per le superfici che lo shader dell'edificio tinge con altre texture. Se più di un
ventesimo di una texture è entro 12 livelli da quel colore, il blocco viene ridipinto con il
colore medio della texture stessa. Altrimenti una città viene fuori arancione.

### Superfici trasparenti {#see-through-surfaces}

Le recinzioni a maglia e le reti sono singoli quad con buchi nel canale alfa della texture.
Disegnate piene, una recinzione diventa un muro che attraversa la vista del tracciato. Le
superfici il cui shader di materiale corrisponde a `alphatest`, `alphablend`, `transmissive`,
`anim_flag`, `impostor`, `branch`, `bush` o `tree` vengono verificate:

- L'opacità della texture viene mediata su una griglia di 32 x 32.
- Per superficie (ogni triangolo ritagliato che condivide una texture), si campionano quattro
  punti per triangolo nello spazio UV, pesati dall'area UV del triangolo.
- Se l'opacità media è almeno 0.05 e sotto **0.5**, l'intera superficie viene lasciata fuori.
  Sotto 0.05 l'alfa significa chiaramente qualcos'altro per il suo shader (un segnale di
  avvertimento che campiona 0.01), e la superficie resta piena.
- Un modello in cui ogni superficie è stata lasciata fuori viene segnalato:
  `N models left out as see-through (mostly holes in their texture)`.

Lo strumento giudica l'intera superficie, non un triangolo alla volta. Giudicato per triangolo,
metà di ogni quad sopravviveva e le recinzioni uscivano come file di denti.

### Edifici disegnati interi {#buildings-drawn-whole}

Una città costruisce i suoi edifici da pezzi modulari: centinaia di migliaia intorno a un solo
circuito cittadino, decine di milioni di triangoli anche al loro livello più grossolano.
Lasciare fuori i pezzi uno alla volta lasciava in piedi lastre di muro isolate. Il gioco inoltre
distribuisce sagome intere per edificio in `scene\hlod_tier_1\`, una mesh per edificio (radice
`hlod_tier_1_*`), già in coordinate del mondo come il terreno:

- Il riquadro mondiale di ogni sagoma viene letto dal riquadro di posizione della sua mesh
  (una lettura dell'intestazione, non una decodifica). Per una mappa intera richiede secondi.
- Vengono usate le sagome che toccano il riquadro del giro e il corridoio.
- Ogni pezzo `buildings` la cui posizione cade dentro l'impronta di una sagoma (più 0,5 m) viene
  eliminato, e al suo posto si disegna la sagoma. La sua distanza dalla guida si misura fino allo
  spigolo più vicino dell'edificio.
- Il riepilogo scrive `N buildings drawn whole from the game's own stand-ins (which replace M modular pieces)`.

### Layer attivati {#switched-on-layers}

Ciò che un layer attivato colloca viene esportato, ma separato dal mondo a percorrenza libera,
così il visualizzatore può mostrarlo o nasconderlo:

| Layer | Parte |
|---|---|
| il mondo a percorrenza libera | `structure:<category>` (come prima) |
| un layer che nomina il percorso della gara abbinata | `structure:event_<category>` |
| qualsiasi altro layer attivato | `structure:layer_<category>` |

Il riepilogo li conta: `switched-on layers: <n> copies in <m> (<layer names>)`.

### Modelli già in coordinate del mondo {#models-already-in-world-coordinates}

Alcuni tipi di modelli non sono in alcun file di posizionamento. Le loro mesh portano una
propria posizione nel mondo, come il terreno, quindi niente deve collocarli:

| Cartella sotto `scene\models\` | Cos'è | Parte |
|---|---|---|
| `plots` | il suolo proprio di una location: la pista e il campo interno di uno stadio, un sito di festival, una piazza | `ground:venue` |
| `plinths` (e qualsiasi modello chiamato `floor`, `ground` o `road`) | suolo con cui una strada è arredata: fioriere, gradini, la pavimentazione di un parco | `ground:plinths` |
| `hda_infrastructure` (ponti) | ponti costruiti proceduralmente | `structure:bridges` |

- Un modello viene considerato in coordinate del mondo quando il centro del suo riquadro sta a
  più di **300 m** (`WORLD_REACH`) dalla sua origine. I modelli collocati dai file di
  posizionamento stanno entro un paio di centinaia di metri dalla loro.
- Non vengono disegnati: gli occluder, i cavi tesi lungo le strade, il fondale del mare, i tetti
  e gli occluder degli edifici modulari (le sagome disegnano quegli edifici), i volumi di
  collisione e d'acqua.
- Ognuno viene letto dal riquadro delle sue mesh (una lettura dell'intestazione), pochi secondi
  per una mappa intera, una volta per esecuzione.
- Le parti di suolo non vengono mai disegnate più grossolane né lasciate fuori per rientrare nel
  budget, come i cordoli.

**Una location viene tagliata intera.** Quando la guida tocca il suolo proprio di una location
(`ground:venue`), il corridoio viene allargato all'intera impronta di quel suolo più `--margin`,
così arrivano anche le tribune, i muri e le barriere attorno a uno stadio, non solo la striscia
usata dai giri. La console scrive `through a venue (<model names>): cutting all of its ground, <n> km2`.
I basamenti non allargano il ritaglio.

### Dettaglio e budget {#detail-and-the-budget}

Le fasce di distanza, il budget e quali copie vengono tolte quando il budget è troppo piccolo
sono descritti in [Livelli di dettaglio e budget](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html).

### Riepilogo del posizionamento {#placement-summary}

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

## Il layer della gara {#the-races-own-layer}

Molte gare mettono in campo cose che nel mondo a percorrenza libera non ci sono: muri e
recinzioni di cemento che chiudono le strade laterali, pile di pneumatici, tende, un portale di
partenza, tribune, bandiere, striscioni. Ogni gara le elenca nella propria definizione di
percorso (`route<id>_<map>.rtd` in `routedefinitions.zip`, XML semplice in uno zip semplice):

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

- **Cosa viene aggiunto.** Ogni istanza viene collocata come una copia da file di
  posizionamento. I 16 numeri della trasformazione sono quattro righe: gli assi x, y e z del
  modello (ciascuno scalato) e la sua posizione in metri del gioco. La terza riga è il prodotto
  vettoriale delle prime due. `Material` è la variante che la copia indossa. La parte è
  `structure:event_<kind>`, dove `<kind>` è la cartella sotto `scene\models\` (barriers, props,
  infrastructure, signs; qualsiasi altra cosa conta come props), e il nodo porta gli extra glTF
  `{"layer": "event", "route": <id>}`.
- **Cosa viene tolto.** Una copia del mondo a percorrenza libera che sta entro **0,1 m** dalla
  posizione di un oggetto nascosto viene lasciata fuori. Un oggetto nascosto nell'origine è un
  modello in coordinate del mondo; il suo GUID di istanza viene cercato nell'`AssetManifest.xml`
  del tracciato (la lista `<Models>`: la sorgente di un modello, poi i GUID delle sue copie) per
  dargli un nome.
- **Il suolo che la gara nasconde viene mantenuto.** Una gara che nasconde il suolo proprio di una
  location vi stende una propria superficie. Quando quella superficie non è tra i modelli che il
  tracciato distribuisce, il suolo nascosto resta, come la cosa più vicina a ciò su cui si guida,
  e il riepilogo lo dice (`kept <model>: the race hides it for a surface of its own that the track does not ship`).
- **Non disegnato, ma contato.** I marcatori di spettatori (`crowd_proxies`: il gioco disegna la
  folla come sprite a partire da essi) e le spline di collisione (`.splinecol`). La console li
  elenca: `its own layer: <n> copies of <m> models, <k> free-roam objects hidden; not drawn: ...`.
- Gli asset della gara per cui il tracciato non distribuisce un modello (aloni di luce, alcuni
  cartelli, contenuti che il gioco carica in streaming) vengono nominati in `placed names have no
  model in the archives`.

Vengono collocate solo le copie dentro il corridoio, come per tutto il resto.

## Scrivere il file {#writing-the-file}

Le parti vengono scritte in quest'ordine: per tassello `terrain`, `verge`, `road` (ciascuna con
l'immagine del tassello), poi `water`, `tyre marks`, `markings` (piatte, le ultime due
sollevate), poi ogni parte collocata in ordine di nome. Le coordinate sono quelle del gioco
(metri, Y in alto). Vedi [Formato di output](https://holdi601.github.io/3DHeat-GameFiles/output-format.html).

Il file dice cosa contiene nel suo `asset.extras` di glTF:

| Campo | Significato |
|---|---|
| `course_format` | `2`: il layer della gara, le location e i modelli in coordinate del mondo sono inclusi. [`courses`](commands.md#courses) esporta di nuovo un file con un numero più basso (o senza) |
| `route` | l'id del percorso abbinato, oppure `null` |
| `event_copies`, `event_kinds` | quante copie del layer della gara sono state collocate, e i loro tipi |
| `hidden` | copie del mondo a percorrenza libera lasciate fuori perché la gara le rimuove |
| `venue` | i modelli di suolo di location che la guida attraversa |
| `layers` | i layer attivati collocati |

## Quanto costa {#what-it-costs}

Ordini di grandezza approssimativi:

| Percorso | Risultato |
|---|---|
| un circuito di campagna breve | qualche centinaio di migliaia di triangoli di terreno, oltre un milione di collocati; secondi, sotto 100 MB |
| una lunga sprint da punto a punto | il corridoio è una piccola frazione del riquadro intorno; circa un minuto, qualche centinaio di MB |
| un circuito cittadino | migliaia di barriere, oggetti di scena e cartelli, e interi edifici; con il budget automatico fino a diverse centinaia di MB |

Un chilometro quadrato di terreno open-world sono circa un milione di triangoli.

## Controlli alla base {#checks-behind-it}

Sono misurazioni fatte mentre il lettore veniva scritto, come dichiarato nel sorgente. Non
vengono rieseguite dai test, a meno che il gioco non sia installato.

- Sul circuito di prova, l'auto sta circa alla sua altezza di marcia sopra il suolo estratto
  (mediana sotto 0,2 m).
- Ogni tassello campionato cade dentro il quadrato di 512 m che il suo nome prevede.
- Posizionamenti consecutivi di guardrail distano esattamente 4 m, e la maggior parte delle
  estremità dei guardrail cade entro 5 cm dall'inizio del successivo.
- I cordoli si trovano pochi centimetri sopra il suolo estratto, con la faccia verso l'alto,
  entro 5 m dalla guida (anche un test sul gioco installato, vedi [Manutenzione](maintaining.md#tests)).

## Non disegnato {#not-drawn}

- Alberi e cespugli a meno di `--trees`. Erba e folle mai (il gioco le disegna come sprite).
- I modelli propri di una gara che il tracciato non distribuisce (vedi [Il layer della gara](#the-races-own-layer)).
- Materiali decal proiettati sui modelli.
- Le stampe dei cartelli fuse in alfa sul loro pannello vengono rese opache.
- Il colore del suolo è una ricostruzione di dove si trovano asfalto, erba e bosco, non i
  materiali del terreno propri del gioco.
