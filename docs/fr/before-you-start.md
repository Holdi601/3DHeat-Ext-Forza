---
title: "Avant de commencer"
nav_order: 2
lang: "fr"
source: before-you-start.md
source_hash: "df38b4a84aaa"
nav_exclude: true
search_exclude: true
---
# Avant de commencer {#before-you-start}

Vous ne connaissez pas la ligne de commande ? Cette page vous mène de rien à un outil qui
marche, en une dizaine de minutes. Vous tapez des commandes dans une fenêtre appelée un
**terminal**, et l'outil répond par du texte.

## 1. Installer Python {#install-python}

1. Allez sur [python.org/downloads](https://www.python.org/downloads/) et téléchargez
   **Python 3.10 ou plus récent**.
2. Lancez l'installateur. Sur son premier écran, cochez **« Add python.exe to PATH »**,
   puis cliquez sur **Install Now**.

Il faut aussi avoir Forza installé, par Steam ou le Microsoft Store (application Xbox).
L'outil le trouve tout seul.

## 2. Récupérer l'outil {#get-the-tool}

- **Avec git :** `git clone https://github.com/Holdi601/3DHeat-Ext-Forza.git`
- **Sans git :** sur la [page GitHub](https://github.com/Holdi601/3DHeat-Ext-Forza),
  cliquez sur le bouton vert **Code**, puis sur **Download ZIP**, et décompressez le fichier.

## 3. Ouvrir un terminal dans le dossier de l'outil {#open-a-terminal-in-the-tools-folder}

- Dans l'Explorateur de fichiers, ouvrez le dossier qui contient `README.md`. Cliquez sur
  la barre d'adresse, tapez `cmd` et appuyez sur Entrée. Une fenêtre noire s'ouvre, déjà
  dans ce dossier.
- Ou ouvrez **Windows Terminal** et allez-y avec `cd` :

  ```
  cd "C:\Users\you\Downloads\3DHeat-Ext-Forza"
  ```

## 4. Installer l'outil {#install-the-tool}

```
python -m pip install -e .
```

Cela installe la commande `heat3d-forza-maps` et ce dont elle a besoin :
[3DHeat GameFiles](https://holdi601.github.io/3DHeat-GameFiles/) (la bibliothèque sur
laquelle s'appuient les lecteurs), numpy, lz4 et Pillow. Vous devez voir des lignes qui
finissent par `Successfully installed ...`.

Vous avez déjà une copie de GameFiles et vous ne voulez pas l'installer une nouvelle fois ?
Réglez `HEAT3D_GAMEFILES` sur son dossier ; un dossier GameFiles nommé `3DHeat-GameFiles`
à côté de celui-ci est trouvé tout seul.

## 5. Vérifier que cela marche {#check-that-it-works}

```
heat3d-forza-maps --help
```

Vous devez voir `usage: heat3d-forza-maps [-h]` et une liste de commandes (`identify`,
`list`, `extract`, `course`, ...). C'est la réussite : l'outil est prêt.

## 6. Un premier parcours {#a-first-course}

Si vous enregistrez vos tours avec FH Companion, donnez à `course` le nom d'un parcours
tel que la bibliothèque le montre :

```
heat3d-forza-maps course "Example Circuit"
```

Ou donnez-lui un fichier de tour (l'une des formes décrites dans
[Entrées de tour](https://holdi601.github.io/3DHeat-GameFiles/lap-inputs.html)) :

```
heat3d-forza-maps course lap.json -o example.glb
```

Il indique quelle piste et quelle course il a trouvées, de quoi est fait le sol, ce qu'il
y a posé dessus, et il se termine par `wrote example.glb (... bytes)`. Voir
[Export de parcours](course-export.md).

## Lire les exemples {#reading-the-examples}

- `<quelque chose>` est un **espace réservé** : tapez à la place votre propre valeur, sans
  les chevrons. `<lap file>` devient, par exemple, `laps\mon_tour.json`.
- `[--option]` entre crochets est **facultatif** : omettez-le si vous n'en avez pas besoin.
- Un chemin contenant des espaces a besoin de **guillemets doubles** :
  `"C:\My Games\lap.json"`.

## Quand quelque chose ne va pas {#when-something-goes-wrong}

| Vous voyez | Que faire |
|---|---|
| `'python' is not recognized` | Python n'est pas installé, ou « Add to PATH » n'était pas coché. Relancez l'installateur, cochez-le, puis ouvrez un nouveau terminal. |
| `'heat3d-forza-maps' is not recognized` | L'étape 4 a été sautée, ou elle a tourné avec un autre Python. Relancez-la ; `python -m heat3d_ext_forza --help` marche de toute façon depuis le dossier de l'outil. |
| `heat3d-forza-maps needs 3DHeat GameFiles: ...` | GameFiles n'est pas installé. Relancez l'étape 4, ou réglez `HEAT3D_GAMEFILES` sur un dossier GameFiles. |
| `heat3d-forza-maps needs Pillow: ...` (ou lz4, numpy) | Lancez le `pip install` que la ligne indique. |
| `no installed Forza track found` | Le jeu n'est pas dans une bibliothèque Steam ni dans `C:\XboxGames`. Donnez son dossier de piste avec `--track` ([Comment un parcours Forza est fait](course-forza-horizon.md#finding-the-installed-game)). |
| `none of the installed tracks (...) has terrain at x ..., z ...` | Le tour vient d'un jeu ou d'une carte qui n'est pas installé. |
| `can't open file` / `not found` avec un chemin | Le chemin contient des espaces sans guillemets, ou une faute de frappe. Mettez-le entre guillemets doubles. |

D'autres messages et leurs solutions : [Dépannage](https://holdi601.github.io/3DHeat-GameFiles/troubleshooting.html)
sur le site de GameFiles.
