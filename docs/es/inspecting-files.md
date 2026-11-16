---
title: "Inspeccionar archivos de Forza"
nav_order: 7
lang: "es"
source: inspecting-files.md
source_hash: "e6cee3695640"
nav_exclude: true
search_exclude: true
---
# Inspeccionar archivos de Forza: `identify`, `list`, `extract` {#inspecting-forza-files-identify-list-extract}

**En pocas palabras:** un circuito de Forza se guarda en unos pocos archivos comprimidos muy
grandes. Estos tres comandos dicen qué es un archivo, muestran lo que contiene un archivo
comprimido y copian una cosa fuera de él. No los necesitas para exportar un circuito; sirven
para mirar dentro.

## identify {#identify}

```
heat3d-forza-maps identify <file>
```

1. **Encuentra un archivo.** Los archivos de un circuito están en
   `<game folder>\media\Tracks\<map>\`: `GeoChunk0.minizip` a `GeoChunk3.minizip`, cada uno con
   un `ChunkContentsMiniZip<n>.txt` al lado.
2. **Ejecútalo.** Ejemplo (cifras inventadas):

   ```
   > heat3d-forza-maps identify GeoChunk0.minizip
   GeoChunk0.minizip  (12,345,678,901 bytes)
     ForzaTech .minizip archive, version 101
       entries    98,304 in 192 segments
       names      ChunkContentsMiniZip0.txt
   ```

   El propio archivo no guarda nombres (mira [ForzaTech](reader-forzatech.md)). `names` indica
   qué lista los nombra; si no hay ninguna al lado, las entradas se identifican por número
   (`#0`, `#1`, ...), y una lista cuyo número de líneas no coincide con el de las entradas se
   informa como que no pertenecen juntas.
3. **Un modelo** extraído de un archivo (`.modelbin`) también se nombra: su versión, cuántos
   fragmentos tiene y las etiquetas de fragmento más comunes. El contenido de los fragmentos no
   se decodifica aquí.

Cualquier cosa que no sea ninguna de las dos dice `<file>: not a Forza file` en la salida de
error y sale con código 2. El formato lo deciden los bytes, nunca la extensión.

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

Cada línea muestra el tamaño descomprimido, la compresión (`lz4`, `deflate` o `stored`) y la
ruta tal como la escribe la lista de nombres, sin el prefijo de la máquina que construyó el
juego, y con las barras invertidas del juego. `--filter` busca cualquier parte de la ruta, sin
distinguir mayúsculas; `--limit` (por defecto 50) limita las líneas, no el recuento.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

```
> heat3d-forza-maps extract GeoChunk0.minizip "scene\tbheightfield\autoterrain_x0_z0_cluster000.i.modelbin"
65,536 bytes -> autoterrain_x0_z0_cluster000.i.modelbin
```

La entrada es la ruta exactamente como la imprime `list`, o `#<number>`. Sin `--out` se escribe
en la carpeta actual con su propio nombre de archivo. Una entrada que no está en el archivo sale
con código 1 (`not in the archive: ...`).

Lo que sacas de los archivos del juego es contenido del juego: para tu propio análisis, no para
pasarlo a otros ([Términos y licencia](terms.md)).
