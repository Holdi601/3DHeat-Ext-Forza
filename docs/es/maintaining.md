---
title: "Mantener estas páginas"
nav_order: 91
lang: "es"
source: maintaining.md
source_hash: "5a5a685c8282"
nav_exclude: true
search_exclude: true
---
# Mantener estas páginas {#maintaining-these-docs}

Una lista de comprobación para cada versión, para que las páginas nunca se queden atrás del código.

1. **Regenera la referencia.** `python tools/gen_docs_reference.py` reescribe la
   [Referencia de comandos](../cli-reference.md) a partir del propio `--help` del programa y de
   los nombres de sus partes. `python tools/gen_docs_reference.py --check` sale con código 1
   cuando la página publicada está desactualizada.
2. **Vuelve a dibujar las imágenes de terminal** cuando cambie una salida:
   `python tools/terminal_pictures.py` ejecuta `cars --help` y `course` sobre el circuito
   inventado que construyen las pruebas. Nunca un circuito real ni una vuelta real.
3. **Enumera lo que cambió.** `git log v<VERSION>..HEAD --oneline`, donde `<VERSION>` es la
   última versión publicada (el archivo `VERSION` de esa publicación). Da a cada función nueva,
   opción y salida un lugar en una página, y una fila en la sección **Docs** de
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/CHANGELOG.md).
4. **Revisión independiente.** Alguien que no escribió las páginas lee el README y cada página
   cambiada, las imágenes incluidas, tres veces: como principiante que nunca ha usado una
   terminal, como un niño de 8 años, y como experto que comprueba cada opción contra `--help`.
   Los ejemplos usan solo nombres y números inventados.
5. **Corrige** todo lo que encuentre la revisión.
6. **Traducciones.** Cada página traducida registra el hash de la página en inglés de la que se
   hizo. Vuelve a traducir las páginas cuyo origen en inglés cambió, y luego revisa cada idioma:
   texto claro, etiquetas de los diagramas correctas, y las mismas palabras que la interfaz
   traducida del visor.
7. **Ejecuta las pruebas** (abajo).
8. **Publica** solo con el visto bueno del propietario.

## Pruebas {#tests}

```
python -m pip install -e .[test]
python -m pytest
```

Todo corre con datos inventados: archivos, modelos, texturas, archivos de colocación y carpetas
de circuito completas los escriben las propias pruebas (`tests/forza_fixtures.py`), y `course`
se ejecuta de principio a fin sobre uno, a partir solo de una vuelta, encontrando el juego
inventado tal como encuentra uno real.

Algunas pruebas también leen un Forza instalado cuando lo hay, y se saltan cuando no: cada
archivo de modelos forma una cadena cerrada de fragmentos, cada coche se apoya sobre sus
ruedas, y los bordillos quedan junto a la línea conducida de los circuitos más conducidos de la
biblioteca de FH Companion. `HEAT3D_COURSE=<course folder>` elige el circuito para esta última.
Leen el juego; nunca escriben en el repositorio.

Las pruebas necesitan 3DHeat GameFiles: instalado, o encontrado de la misma forma en que lo
encuentra el comando (`HEAT3D_GAMEFILES`, la carpeta `gamefiles` de una copia de 3DHeat, o una
carpeta `3DHeat-GameFiles` junto a esta).

## Traducciones: los comandos {#translations-the-commands}

El sitio está traducido a los 40 idiomas del visor de 3DHeat: el inglés en `docs/`, cada otro
idioma en `docs/<lang>/` con los mismos nombres de archivo. `tools/docs_i18n.py` lleva la
contabilidad:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Traduce solo lo que lista `todo`: mantén el Markdown, los enlaces, el código y los nombres de
archivos y columnas tal cual; traduce los títulos y las descripciones de las imágenes, y usa las
palabras propias del visor de 3DHeat para sus botones y paneles (su `src/i18n/locales/<lang>/`).
Las páginas de referencia generadas y las imágenes de terminal se quedan en inglés. En el sitio,
una traducción desactualizada lo dice y enlaza la página en inglés; una que falta cae en inglés.
El menú de idiomas del encabezado y la redirección por idioma del navegador en la página de
inicio salen de `docs/_includes/`.
