# Third-party licences

This tool is MIT licensed ([`LICENSE`](LICENSE)). What it uses, and under which
licence; each package's own source is what counts, not this file.

| Software | Licence | How it is used |
|---|---|---|
| 3DHeat GameFiles | MIT | a dependency, installed by pip: the glTF writer, lap files, the corridor, ground kinds, the detail budget, Steam libraries |
| numpy | BSD-3-Clause | a dependency: mesh decoding |
| lz4 | BSD-3-Clause | a dependency: the `.minizip` archives' LZ4 blocks |
| Pillow | MIT-CMU (HPND) | a dependency: block-compressed textures, JPEG output |
| pytest | MIT | development only: the tests |

No reader here is derived from another project's source. ForzaTech's formats are
undocumented; every offset was measured on the files (see
[ForzaTech](https://holdi601.github.io/3DHeat-Ext-Forza/reader-forzatech.html)).

## The game's files

Forza Horizon and Forza Motorsport belong to Microsoft (Playground Games and
Turn 10 Studios). This repository holds no file of the games and no course,
car or texture made from one; the tool reads the copy the user installed, on
the user's machine, and what it writes stays there. See
[Terms and licence](https://holdi601.github.io/3DHeat-Ext-Forza/terms.html).
