---
title: "Antes de empezar"
nav_order: 2
lang: "es"
source: before-you-start.md
source_hash: "df38b4a84aaa"
nav_exclude: true
search_exclude: true
---
# Antes de empezar {#before-you-start}

¿Nunca has usado la línea de comandos? Esta página te lleva de cero a una herramienta
funcionando en unos diez minutos. Escribes órdenes en una ventana llamada **terminal**, y la
herramienta responde con texto.

## 1. Instala Python {#install-python}

1. Ve a [python.org/downloads](https://www.python.org/downloads/) y descarga
   **Python 3.10 o posterior**.
2. Ejecuta el instalador. En su primera pantalla, marca **"Add python.exe to PATH"**,
   y luego haz clic en **Install Now**.

También necesitas un Forza instalado, por Steam o por la Microsoft Store (aplicación Xbox).
La herramienta lo encuentra sola.

## 2. Consigue la herramienta {#get-the-tool}

- **Con git:** `git clone https://github.com/Holdi601/3DHeat-Ext-Forza.git`
- **Sin git:** en la [página de GitHub](https://github.com/Holdi601/3DHeat-Ext-Forza),
  haz clic en el botón verde **Code** y luego en **Download ZIP**, y descomprímelo.

## 3. Abre una terminal en la carpeta de la herramienta {#open-a-terminal-in-the-tools-folder}

- En el Explorador de archivos, abre la carpeta que contiene `README.md`. Haz clic en la barra
  de direcciones, escribe `cmd` y pulsa Intro. Se abre una ventana negra, ya en esa carpeta.
- O abre **Windows Terminal** y ve allí con `cd`:

  ```
  cd "C:\Users\you\Downloads\3DHeat-Ext-Forza"
  ```

## 4. Instala la herramienta {#install-the-tool}

```
python -m pip install -e .
```

Esto instala el comando `heat3d-forza-maps` y lo que necesita:
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) (la biblioteca sobre la que
se apoyan los lectores), numpy, lz4 y Pillow. Deberías ver líneas que terminan en
`Successfully installed ...`.

¿Ya tienes una copia de GameFiles y no quieres instalarla otra vez? Indica su carpeta en
`HEAT3D_GAMEFILES`; una carpeta de GameFiles llamada `3DHeat-GameFiles` junto a esta también
se encuentra sola.

## 5. Comprueba que funciona {#check-that-it-works}

```
heat3d-forza-maps --help
```

Deberías ver `usage: heat3d-forza-maps [-h]` y una lista de comandos (`identify`, `list`,
`extract`, `course`, ...). Eso es señal de éxito: la herramienta está lista.

## 6. Un primer circuito {#a-first-course}

Si grabas vueltas con FH Companion, da a `course` el nombre de un circuito tal como lo muestra
la biblioteca:

```
heat3d-forza-maps course "Example Circuit"
```

O dale un archivo de vuelta (cualquiera de las formas de
[Entradas de vuelta](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)):

```
heat3d-forza-maps course lap.json -o example.glb
```

Dice qué circuito y qué carrera encontró, de qué está hecho el suelo y qué colocó sobre él, y
termina con `wrote example.glb (... bytes)`. Mira [Exportación de circuito](course-export.md).

## Cómo leer los ejemplos {#reading-the-examples}

- `<algo>` es un **marcador de posición**: escribe tu propio valor en su lugar, sin los
  signos menor y mayor. `<lap file>` se convierte, por ejemplo, en `laps\my_lap.json`.
- `[--option]` entre corchetes es **opcional**: omítelo si no lo necesitas.
- Una ruta con espacios necesita **comillas dobles**: `"C:\My Games\lap.json"`.

## Cuando algo sale mal {#when-something-goes-wrong}

| Ves | Qué hacer |
|---|---|
| `'python' is not recognized` | Python no está instalado, o no se marcó "Add to PATH". Ejecuta el instalador otra vez y marca la casilla, luego abre una terminal nueva. |
| `'heat3d-forza-maps' is not recognized` | Se saltó el paso 4, o se ejecutó con otro Python. Vuelve a ejecutarlo; `python -m heat3d_ext_forza --help` funciona desde la carpeta de la herramienta en cualquier caso. |
| `heat3d-forza-maps needs 3DHeat GameFiles: ...` | GameFiles no está instalado. Repite el paso 4, o indica `HEAT3D_GAMEFILES` con una carpeta de GameFiles. |
| `heat3d-forza-maps needs Pillow: ...` (o lz4, numpy) | Ejecuta el `pip install` que nombra la línea. |
| `no installed Forza track found` | El juego no está en una biblioteca de Steam ni en `C:\XboxGames`. Pasa su carpeta de circuito con `--track` ([Cómo se hace un circuito de Forza](course-forza-horizon.md#finding-the-installed-game)). |
| `none of the installed tracks (...) has terrain at x ..., z ...` | La vuelta es de un juego o de un mapa que no está instalado. |
| `can't open file` / `not found` con una ruta | La ruta tiene espacios sin comillas, o una errata. Ponla entre comillas dobles. |

Más mensajes y sus soluciones:
[Solución de problemas](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html)
en el sitio de GameFiles.
