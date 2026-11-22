# Modèle du compte rendu de projet

Ce modèle est **obligatoire**. Ne modifiez ni la mise en page ni l'ordre des sections.

## Compiler

- **Overleaf** : importez le dossier en zip (New Project, puis Upload Project) et compilez avec pdfLaTeX.
- **En local** : `latexmk -pdf main.tex`

## Remplir

1. Renseignez les informations du projet en haut de `main.tex` (titre, équipe, membres, dépôt).
2. Répartissez les fichiers de `sections/` entre les membres : chacun rédige les siens et indique son nom dans `\redacteur{}`. Un fichier par personne limite les conflits Git.
3. Remplacez toutes les zones rouges `\acompleter`. Il ne doit en rester aucune.
4. Placez les figures dans `figures/` (le schéma d'architecture s'appelle `architecture.pdf` ou `.png`). Une figure absente s'affiche comme un cadre rouge.
5. Ajoutez vos sources dans `references.bib` et citez-les avec `\citet{}` ou `\citep{}`.
6. Pour la version rendue, remplacez `\consignestrue` par `\consignesfalse` dans `main.tex` : les encadrés bleus disparaissent.

## Contraintes

- 12 à 20 pages, hors page de garde, table des matières et annexes.
- Extraits de code de moins de 20 lignes ; le reste est dans le dépôt.
- Le PDF final est déposé dans `docs/rapport/rapport-final.pdf` et rattaché à l'étiquette Git de la version rendue.
