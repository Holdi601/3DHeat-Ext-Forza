---
title: "Maintenance de ces documents"
nav_order: 91
lang: "fr"
source: maintaining.md
source_hash: "5a5a685c8282"
nav_exclude: true
search_exclude: true
---
# Maintenance de ces documents {#maintaining-these-docs}

Une liste de contrôle à chaque version, pour que les pages ne retardent jamais sur le code.

1. **Régénérer la référence.** `python tools/gen_docs_reference.py` réécrit la
   [Référence des commandes](../cli-reference.md) à partir du `--help` du programme et des noms
   de parties. `python tools/gen_docs_reference.py --check` sort avec le code 1 quand la page
   committée n'est plus à jour.
2. **Refaire les images du terminal** quand une sortie change :
   `python tools/terminal_pictures.py` lance `cars --help` et `course` sur la piste fictive que
   construisent les tests. Jamais une vraie piste ni un vrai tour.
3. **Lister ce qui a changé.** `git log v<VERSION>..HEAD --oneline`, où `<VERSION>` est la dernière
   version publiée (le fichier `VERSION` au moment de la publication). Donnez à chaque nouvelle
   fonctionnalité, option et sortie une place dans une page, et une ligne dans la section **Docs**
   de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Forza/blob/main/CHANGELOG.md).
4. **Relecture indépendante.** Quelqu'un qui n'a pas écrit les pages lit le README et chaque page
   modifiée, les images comprises, trois fois : en débutant qui n'a jamais utilisé de terminal, en
   enfant de huit ans, et en expert qui vérifie chaque option contre `--help`. Les exemples
   n'utilisent que des noms et des chiffres inventés.
5. **Corriger** tout ce que la relecture trouve.
6. **Traductions.** Chaque page traduite enregistre le hachage de la page anglaise dont elle est
   issue. Retraduisez les pages dont la source anglaise a changé, puis relisez chaque langue :
   texte clair, libellés de schémas corrects, et mêmes mots que l'interface traduite du
   visualiseur.
7. **Lancer les tests** (ci-dessous).
8. **Pousser** seulement après le feu vert du propriétaire.

## Tests {#tests}

```
python -m pip install -e .[test]
python -m pytest
```

Tout tourne sur des données inventées : les archives, modèles, textures, fichiers de placement et
dossiers de piste entiers sont écrits par les tests eux-mêmes (`tests/forza_fixtures.py`), et
`course` est lancé de bout en bout sur l'un d'eux, à partir d'un seul tour, en trouvant le jeu
fictif comme il trouverait un vrai.

Quelques tests lisent aussi un Forza installé, s'il y en a un, et sont sautés sinon : chaque
archive de modèles forme une chaîne de morceaux fermée, chaque voiture repose sur ses roues, et les
bordures reposent sur le sol à côté de la conduite des circuits les plus parcourus de la
bibliothèque FH Companion. `HEAT3D_COURSE=<course folder>` choisit le parcours pour ce dernier test.
Ils lisent le jeu ; ils n'écrivent jamais dans le dépôt.

Les tests ont besoin de 3DHeat GameFiles : installé, ou trouvé comme le fait la commande
(`HEAT3D_GAMEFILES`, le dossier `gamefiles` d'un dépôt 3DHeat, ou un dossier `3DHeat-GameFiles` à
côté de celui-ci).

## Traductions : les commandes {#translations-the-commands}

Le site est traduit dans les 40 langues du visualiseur 3DHeat : l'anglais dans `docs/`, chaque
autre langue dans `docs/<lang>/`, avec les mêmes noms de fichiers. `tools/docs_i18n.py` tient les
comptes :

```bash
python tools/docs_i18n.py hashes             # après tout changement en anglais : enregistrer le hachage de chaque page
python tools/docs_i18n.py svg-strings        # après tout changement d'image : les libellés à traduire
python tools/docs_i18n.py status             # par langue : pages à jour, périmées ou absentes
python tools/docs_i18n.py todo --lang de     # les pages allemandes à (re)traduire
python tools/docs_i18n.py svg-build --lang de    # les images allemandes, à partir de docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marquer les pages allemandes avec leur hachage anglais
python tools/docs_i18n.py check              # sort avec le code 1 quand les hachages ou libellés sont périmés
```

Ne traduisez que ce que `todo` liste : gardez le Markdown, les liens, le code, les noms de fichiers
et de colonnes tels quels ; traduisez les titres et les descriptions d'images, et utilisez les mots
propres au visualiseur 3DHeat pour ses boutons et panneaux (son `src/i18n/locales/<lang>/`). Les
pages de référence générées et les images du terminal restent en anglais. Sur le site, une
traduction périmée l'indique et renvoie à la page anglaise ; une traduction absente se rabat sur
l'anglais. Le menu de langue de l'en-tête et la redirection de la page d'accueil selon la langue du
navigateur viennent de `docs/_includes/`.
