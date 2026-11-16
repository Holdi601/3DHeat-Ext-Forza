---
title: "Términos y licencia"
nav_order: 12
lang: "es"
source: terms.md
source_hash: "6c61ae2ba60f"
nav_exclude: true
search_exclude: true
---
# Términos y licencia {#terms-and-licence}

Esta página es un registro de lo que dicen las licencias, no asesoramiento legal.

## El juego es de Microsoft {#the-game-is-microsofts}

Forza Horizon y Forza Motorsport, sus circuitos, coches y texturas pertenecen a Microsoft
(Playground Games y Turn 10 Studios), que no respalda este proyecto. Este repositorio **no
contiene ningún archivo de los juegos**, ni ningún circuito, coche o textura hecho a partir de
uno, y la herramienta **nunca descarga contenido del juego**: lee la copia **instalada en tu
equipo**.

Lo que le indiques sigue siendo tu responsabilidad. Los juegos tienen sus propias condiciones de
licencia, y los contratos de usuario (EULA) suelen prohibir la ingeniería inversa. Son contratos
exigibles, y la obligación recae en quien ejecuta la herramienta. Ninguna decisión de diseño de
aquí la libera.

## Sin claves: ninguna incluida, ninguna recuperada {#no-keys-none-shipped-none-recovered}

**Lee contenedores.** Leer un formato de archivo contenedor es manejo de archivos corriente. Los
archivos `.minizip` de ForzaTech y sus modelos, texturas y archivos de colocación no están
cifrados, y la herramienta no contiene ninguna clave, no recupera ninguna clave, no lee la
memoria de otro proceso y no inyecta nada en el juego. Las vueltas vienen de la telemetría que el
propio juego publica.

## La salida no es para redistribuir {#output-is-not-for-redistribution}

Lo que sale es geometría para **contexto espacial**: el suelo, la carretera y lo que hay junto a
ella, reducido a un presupuesto, para que las vueltas se puedan analizar en su lugar. Es lo menos
valioso de lo que contienen los archivos, y sigue siendo contenido del editor.

- Guarda los circuitos `.glb` exportados, el archivo de coches (`.h3dcars`) y las texturas que contienen para tu propio análisis, en la máquina en la que se hicieron.
- No publiques, compartas ni vendas circuitos, coches, modelos ni texturas exportados.
- El `.gitignore` del repositorio mantiene fuera del control de versiones los archivos del juego, las exportaciones, las vueltas y las grabaciones, por tipo de archivo (`*.glb`, `*.h3dcars`, `*.minizip`, `*.modelbin`, `*.pb`, `*.csv`, `*.lap.json` y más).

## Los formatos {#the-formats}

Los formatos de ForzaTech no están documentados. Leerlos es ingeniería inversa de un contenedor.
Ninguno de los lectores de aquí se deriva del código fuente de otro proyecto: cada desplazamiento
se midió en los archivos, y cómo se decidió cada uno está anotado en
[ForzaTech](reader-forzatech.md).

## Por qué es una herramienta aparte {#why-this-is-a-separate-tool}

Los lectores de los juegos de cada empresa viven en su propio repositorio, así que una pregunta
de licencia o una solicitud de retirada sobre un juego llega solo a la herramienta de ese juego.
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) mantiene los lectores genéricos
de formatos de motor y la base común; esta herramienta mantiene los de Forza. Si este
repositorio tuviera que desaparecer, no se iría nada más con él.

## La licencia de esta herramienta {#this-tools-licence}

Todo lo escrito para este repositorio está bajo la **licencia MIT**
([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSE)): úsalo, cámbialo,
distribúyelo, comercialmente o no.

Paquetes de terceros, todos permisivos
([`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/LICENSES.md)):

| Paquete | Licencia | Para qué se usa |
|---|---|---|
| 3DHeat GameFiles | MIT | el escritor glTF, los archivos de vuelta, el corredor, los tipos de suelo, el presupuesto de detalle, las bibliotecas de Steam |
| numpy | BSD-3-Clause | decodificación de mallas |
| lz4 | BSD-3-Clause | los bloques LZ4 de los archivos `.minizip` |
| Pillow | MIT-CMU (HPND) | texturas comprimidas por bloques, salida JPEG |
| pytest | MIT | solo desarrollo |

Las licencias se leyeron de los metadatos de los paquetes en septiembre de 2026. Si las
condiciones de un componente cambiaron después, cuenta la fuente.
