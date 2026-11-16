---
title: "Comandos"
nav_order: 3
lang: "es"
source: commands.md
source_hash: "32f5e35285be"
nav_exclude: true
search_exclude: true
---
# Comandos {#commands}

Cada comando se ejecuta como `heat3d-forza-maps <command> ...` (o, desde la carpeta de la
herramienta sin instalarla, `python -m heat3d_ext_forza <command> ...`).

| Comando | Recibe | Hace |
|---|---|---|
| [`course`](#course) | una vuelta | exporta el circuito que la rodea |
| [`courses`](#courses) | una biblioteca de vueltas grabadas | ejecuta `course` en cada circuito de ella |
| [`races`](#races) | un Forza instalado | lista cada carrera que define el juego: qué añade, qué oculta, los recintos y el estado de su exportación |
| [`terrain`](#terrain) | una carpeta de circuito de Forza | corta una región por coordenadas del mundo |
| [`cars`](#cars) | un Forza instalado | cada coche con poco detalle, en un solo archivo para la pestaña Análisis de carrera del visor |
| [`identify`](#identify) | un archivo | dice si es un `.minizip` de Forza o un modelo de ForzaTech, y qué contiene |
| [`list`](#list) | un `.minizip` | lista sus entradas |
| [`extract`](#extract) | un `.minizip` | escribe una entrada en el disco |

**Cómo leer los ejemplos:** `<x>` significa que lo sustituyas por tu propio valor, sin los
signos menor y mayor; `[...]` es opcional; pon entre "comillas dobles" una ruta con espacios,
por ejemplo `"C:\Games\My Game"`. ¿Es la primera vez? Mira [Antes de empezar](before-you-start.md).
La referencia completa de `--help` de cada comando está en la
[Referencia de comandos](../cli-reference.md).

[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) ejecuta esta herramienta con
tus argumentos sin cambios para sus propios `course`, `courses`, `races`, `cars` y `terrain`
sobre una vuelta o un circuito de Forza, y pide a sus `identify`, `list` y `extract` los
archivos de Forza que sus propios lectores no conocen. Por eso `course` también acepta `--level`
e `--install` de GameFiles, y `list` y `extract` aceptan `--key`: se admiten y no se usan.

Cada vez que arranca el programa, puede comprobar primero si hay una versión más nueva.
`HEAT3D_NO_UPDATE=1` desactiva esa comprobación.

Fuente: [`cli.py`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/heat3d_ext_forza/cli.py).

## Códigos de salida {#exit-codes}

| Código | Significado |
|---|---|
| 0 | hecho |
| 1 | el trabajo falló: una vuelta que no se puede leer, una vuelta sin conducción, ningún terreno bajo la conducción, un circuito de `courses` que falló, un `.minizip` que no se puede leer o cuya lista de nombres no le corresponde, una entrada que no está en el archivo |
| 2 | nada que leer, o argumentos incorrectos: ningún Forza instalado, ningún circuito bajo la conducción, ninguna biblioteca de vueltas, una vuelta de otro juego, un archivo que no es de Forza, una ruta que no existe, una dependencia que falta (GameFiles, numpy, lz4, Pillow), `terrain` con `--box` y `--route` a la vez o sin ninguno, un argumento que argparse rechaza |

Cada fallo son una o dos líneas en la salida de error estándar, que dicen qué hacer, no un
rastreo de Python.

---

## course {#course}

```
heat3d-forza-maps course <lap> [-o FILE] [options]
```

Esto exporta el circuito alrededor de una vuelta: el suelo en una banda a cada lado de la
conducción, y lo que hay sobre él, como un `.glb`. Calcula el resto por sí mismo: dónde está
instalado el juego, en cuál de sus circuitos se condujo la vuelta, y cuál de las carreras del
juego es. Mira [Exportación de circuito](course-export.md).

`<lap>` puede ser cualquiera de los siguientes (detalles en
[Entradas de vuelta](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

- un archivo de vuelta: JSON de ruta, JSON de vuelta de FH Companion, JSON `heat3d-lap`, `.npz`, o `.csv` con columnas x, y, z
- una carpeta de archivos de vuelta, buscada recursivamente (un circuito grabado completo)
- un **nombre** de circuito, buscado en la biblioteca de FH Companion en `%LOCALAPPDATA%\FHCompanion\laps`

### Opciones {#options}

| Opción | Por defecto | Significado |
|---|---|---|
| `-o`, `--out FILE` | `<course name>.glb` en la carpeta actual, o en `$HEAT3D_LEVELS/forza/courses/` si está definida | dónde escribir; el nombre se pasa a minúsculas, y las secuencias de otros caracteres se cambian por `_` |
| `--margin M` | 80 | metros de suelo que se conservan a cada lado de la conducción |
| `--texture-size {2048,1024,512}` | 2048 | píxeles de textura de suelo por cada loseta de 512 m (2048 = 25 cm por píxel) |
| `--no-textures` | desactivada | solo colores planos: un archivo mucho más pequeño. Esto también omite la división entre carretera y arcén |
| `--season {summer,autumn,winter,spring}` | summer | de qué temporada son los mapas de suelo y las texturas de los modelos |
| `--no-placed` | desactivada | solo terreno: sin bordillos, barreras, señales ni edificios |
| `--trees` | desactivada | coloca también árboles, arbustos y objetos rompibles |
| `--detail-budget N` | automático | un techo de triángulos para todo lo colocado; mira [Niveles de detalle y presupuesto](https://holdi601.github.io/3DHeat-GameFiles/detail-budget.html) |
| `--track DIR` | buscado | la carpeta del circuito (dentro de `media\Tracks`, con `GeoChunk0.minizip`) si no se debe buscar en el juego instalado |
| `--game {forza,beamng,acrally}` | lo que diga el archivo de vuelta, si no, `forza` | de qué juego es la vuelta (ver abajo) |
| `--level`, `--install` | | aceptadas para la línea de comandos de GameFiles, no se usan |

### Qué juego {#which-game}

El juego se toma de `--game`, luego del campo `game` de un archivo `heat3d-lap` (o de la línea
de descripción `# {...}` de un CSV), y si no, por defecto Forza. Una carpeta toma el juego que
nombren sus archivos, cuando nombran uno solo; un archivo que no nombra ninguno (una vuelta de
FH Companion, `course.json`, un CSV sin línea de descripción) no cuenta.

| Valor | Qué pasa |
|---|---|
| empieza por `forza` | la exportación de Forza |
| `beamng` | rechazado, código de salida 2: `export it with heat3d-beamng-maps course` |
| `assetto-corsa-rally` o `acrally` | rechazado, código de salida 2: `export it with heat3d-acrally-maps course` |
| `assetto-corsa-evo` | rechazado: "keeps all its content in one package obfuscated with a key, and this tool recovers none" |
| `iracing` | rechazado: "tracks ship in a protected format that is not a file-extraction target" |
| cualquier otro | rechazado: "there is no course reader for <game> yet" |

Los tres últimos también sugieren las alternativas: reconstruir el circuito a partir de la
conducción (3DHeat GameCapture), o analizar las vueltas sin circuito, porque la pestaña
Análisis de carrera del visor dibuja una carretera a partir de ellas.

### Ejemplos {#examples}

```
# A course from the FH Companion library, by name
heat3d-forza-maps course "Example Circuit"

# One lap file, a narrower band, a smaller file
heat3d-forza-maps course lap.json -o example.glb --margin 40 --texture-size 1024

# Winter textures, trees included
heat3d-forza-maps course "Example Circuit" --season winter --trees

# A hard ceiling of 500,000 placed triangles
heat3d-forza-maps course lap.json --detail-budget 500000

# A track folder given directly (game installed somewhere it is not searched)
heat3d-forza-maps course lap.json --track "D:\Games\<Forza>\media\Tracks\<map>"
```

Lo que imprime una ejecución, en un circuito inventado que construyen las pruebas (en un
circuito real las cifras llegan a cientos de miles de triángulos, y dice qué circuito y qué
carrera encontró):

![ejecución de course en un circuito inventado](../assets/img/course-run.svg)

## courses {#courses}

```
heat3d-forza-maps courses [-o FOLDER] [options]
```

Esto ejecuta `course` en cada carpeta de circuito de una biblioteca de vueltas grabadas,
escribiendo un `<name>.glb` por cada una.

| Opción | Por defecto | Significado |
|---|---|---|
| `-o`, `--out FOLDER` | `courses`, o `$HEAT3D_LEVELS/forza/courses` si está definida | la carpeta donde escribir (se crea si falta) |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la biblioteca de vueltas |
| `--only TEXT [TEXT ...]` | todos | solo los circuitos cuyos nombres de carpeta contengan uno de estos textos (sin distinguir mayúsculas) |
| `--force` | desactivada | exporta de nuevo lo que ya tiene un `.glb` |
| `--track DIR` | buscado | igual que en `course` |
| `--margin M` | 80 | igual que en `course` |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | igual que en `course` |

¿Qué cuenta como carpeta de circuito? Una subcarpeta directa de la biblioteca cuyo nombre
contiene ` (course_`, que es como FH Companion nombra los circuitos, por ejemplo
`Example Circuit (course_1200_3400_to_1175_3400)`. La parte desde ` (course_` en adelante se
quita del nombre.

Cómo se comporta una ejecución:

- Un circuito cuyo `.glb` ya existe se omite (`kept`) salvo que se dé `--force`, así que una ejecución interrumpida continúa donde se quedó.
- Un `.glb` escrito por una versión anterior, sin la capa propia de la carrera ni los recintos (su `asset.extras.course_format` falta o es menor que el actual), se exporta de nuevo, como si se hubiera dado `--force` solo para él.
- Dos carpetas de circuito con el mismo nombre antes de ` (course_` (un grabador que puso a un circuito nuevo el nombre de uno antiguo) no se pisan: la carpeta creada primero conserva `<name>.glb`, la otra se escribe como `<name>_<start>.glb`, siendo `<start>` el punto de inicio, con los signos menos como `m` (por ejemplo `example_circuit_m120_m340.glb`).
- Un circuito que falla (vueltas ilegibles, memoria agotada, sin terreno...) se informa como `FAILED`, y la ejecución sigue.
- Al final imprime una tabla con el estado, el tamaño en MB, los segundos empleados y el nombre, y luego `<n> of <total> courses in <folder>`.
- El código de salida es 1 si algún circuito falló, y 2 si no hay biblioteca de vueltas.

```
heat3d-forza-maps courses -o courses --only circuit sprint --texture-size 1024
```

## races {#races}

```
heat3d-forza-maps races [-o FOLDER] [--markdown FILE] [options]
```

Lista cada carrera que define un Forza instalado, a partir de sus definiciones de rutas (mira
[Cómo se hace un circuito de Forza](course-forza-horizon.md#which-race)), y comprueba las
exportaciones de una carpeta `courses` contra ellas. Lee el juego y la biblioteca de vueltas;
no escribe nada salvo la tabla opcional.

| Opción | Por defecto | Significado |
|---|---|---|
| `-o`, `--out FOLDER` | igual que en `courses` | la carpeta en la que escribe `courses`, cuyos archivos se comprueban |
| `--library DIR` | `%LOCALAPPDATA%\FHCompanion\laps` | la biblioteca de vueltas |
| `--track DIR` | buscado | la carpeta del circuito, si no es la del juego instalado |
| `--markdown FILE` | ninguna | escribe también la tabla ahí, en Markdown |

Una fila por carrera, y una por cada circuito grabado que se condujo en ella:

| Columna | Significado |
|---|---|
| route | el id de la ruta |
| course | el circuito grabado que le corresponde, si lo hay |
| own assets | copias que la carrera añade al mundo de conducción libre |
| drawn | de ellas, las copias cuyo modelo trae el circuito |
| kinds | las copias añadidas por tipo (barreras, props, calcomanías, infraestructura, ...) |
| not geometry | marcadores de espectadores y splines de colisión, contados |
| hidden | objetos de conducción libre que la carrera quita |
| venue | los modelos de suelo de recinto por los que pasa la línea de IA de la carrera a menos de 10 m |
| export | `current`, `older format` (se exporta de nuevo con `courses`), `not exported`, o vacía para una carrera sin circuito grabado |

Termina con un recuento: `<n> races: <a> with assets of their own, <v> through a venue, <d> driven in the lap library, <s> recorded courses to export again`.

```
heat3d-forza-maps races -o courses --markdown races.md
```

## terrain {#terrain}

```
heat3d-forza-maps terrain <track folder> -o FILE (--box X0 Z0 X1 Z1 | --route FILE) [options]
```

Este es el corte con todo especificado a mano: das la carpeta del circuito y una región, no una
vuelta. Es útil cuando la zona que quieres es una caja y no un recorrido.

| Opción | Por defecto | Significado |
|---|---|---|
| `<path>` | obligatorio | una carpeta de circuito de Forza bajo `media\Tracks` (con `GeoChunk*.minizip`) |
| `-o`, `--out FILE` | obligatorio | el `.glb` que se escribe |
| `--box X0 Z0 X1 Z1` | | la región, en metros del juego (x y z, como los reporta la telemetría); las esquinas en cualquier orden |
| `--route FILE` | | un JSON de ruta con `"bounds": {"min": [x, y, z], "max": [x, y, z]}`, como lo escriben `heat3d_capture route` y `heat3d_capture laps`; se lee como UTF-8, con o sin marca de orden de bytes |
| `--margin M` | **100** | metros que se añaden alrededor de los límites de una ruta, y ancho del corredor cuando la ruta tiene una línea |
| `--texture-size`, `--no-textures`, `--season`, `--no-placed`, `--trees`, `--detail-budget` | | igual que en `course` |

Indica exactamente uno de `--box` y `--route`; si no, el código de salida es 2. Con `--route`,
el corte son los `bounds` de la ruta (`min`/`max`, x y z) ampliados con el margen. Si el
archivo también tiene al menos 10 posiciones, el corte se estrecha a un corredor de `--margin`
metros alrededor de ellas, y los modelos colocados reciben su detalle según la distancia a esa
línea. Con `--box`, se conserva la caja entera, y el detalle va a lo que está más cerca del
centro de la caja.

La altura nunca forma parte del corte. Una caja fuera del mapa, o en el mar, da
`"no terrain there"` (código de salida 1), no un error sobre coordenadas.

```
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --box 0 0 512 512 -o piece.glb
heat3d-forza-maps terrain "<game>\media\Tracks\<map>" --route route.json -o map.glb
```

## cars {#cars}

```
heat3d-forza-maps cars [-o FILE] [--game FOLDER]
```

Cada coche de un Forza instalado, con el poco detalle propio del juego, en un solo archivo
para la pestaña Análisis de carrera del visor. Tarda segundos y escribe unos 5 MB. Mira
[Coches de Forza](forza-cars.md).

## identify {#identify}

```
heat3d-forza-maps identify <path>
```

Lee el archivo y dice qué es, por sus bytes, no por su extensión: un `.minizip` de ForzaTech
(la marca `PGZP`: versión, cantidades de entradas y de segmentos, y si la lista
`ChunkContentsMiniZip<n>.txt` que nombra sus entradas está al lado), o un modelo de ForzaTech,
`.modelbin` (versión, cantidad de fragmentos, las etiquetas de fragmento más comunes).
Cualquier otra cosa sale con código 2 y `<file>: not a Forza file` en la salida de error. Mira
[Inspeccionar archivos de Forza](inspecting-files.md).

## list {#list}

```
heat3d-forza-maps list <.minizip> [--filter TEXT] [--limit N]
```

| Opción | Por defecto | Significado |
|---|---|---|
| `<.minizip>` | obligatorio | un `.minizip` de ForzaTech, como el `GeoChunk0.minizip` de un circuito |
| `--filter TEXT` | ninguno | solo las rutas que contengan TEXT, sin distinguir mayúsculas |
| `--limit N` | 50 | muestra como máximo N entradas (el total siempre se imprime) |
| `--key HEX` | ninguno | aceptada, no se usa: un `.minizip` no está cifrado |

Cada línea muestra el tamaño sin comprimir, la compresión (`lz4`, `deflate` o `stored`) y la
ruta, tal como la escribe la lista de nombres junto al archivo.

## extract {#extract}

```
heat3d-forza-maps extract <.minizip> <entry> [--out FILE]
```

| Opción | Por defecto | Significado |
|---|---|---|
| `<entry>` | obligatorio | la ruta exactamente como la imprime `list`, o `#<number>` |
| `--out FILE` | el nombre del archivo de la entrada (después de la última `/` o `\`), en la carpeta actual | dónde escribir; las carpetas padre se crean |
| `--key HEX` | ninguno | aceptada, no se usa |

## Variables de entorno {#environment-variables}

| Variable | Efecto |
|---|---|
| `HEAT3D_LEVELS` | una carpeta para cada exportación hecha sin `-o`: circuitos en `<HEAT3D_LEVELS>/forza/courses/`, el paquete de coches en `<HEAT3D_LEVELS>/forza/`. Si no está definida, van a la carpeta actual |
| `HEAT3D_GAMEFILES` | una carpeta de 3DHeat GameFiles, cuando GameFiles no está instalado con pip |
| `HEAT3D_NO_UPDATE` | cualquier valor distinto de vacío, `0`, `false` o `no` desactiva la comprobación de actualizaciones |
| `LOCALAPPDATA` | donde se buscan la biblioteca de FH Companion y la caché de actualizaciones |
| `HEAT3D_COURSE` | solo pruebas: el circuito que usa la prueba con el juego instalado en los bordillos; mira [Mantener estas páginas](maintaining.md#tests) |
