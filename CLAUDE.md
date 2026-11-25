# CLAUDE.md

Règles de travail pour ce dépôt. À respecter par Claude (et quiconque automatise des contributions) en plus des conventions habituelles.

## Le projet

ScriptSDK a deux composants versionnés ensemble (même numéro de version dans `package.json` et `pyproject.toml`) :
- **SDK JavaScript/TypeScript** (`lib/`) : compilé en JS via `npm run build` (sortie dans `dist/lib/`).
- **Plugin Endstone** (`src/endstone_scriptsdk/`) : package Python, packagé en wheel via `npm run buildp` (sortie dans `dist/*.whl`).

## Branches et validation

- Toujours travailler sur une branche dédiée (feature/fix), jamais directement sur `develop` ou `main`.
- Une branche se termine par une Pull Request. **Aucun merge n'est fait sans validation explicite de louis.charneux.**
- Une fois validée, la PR est fusionnée dans `develop` en **merge squash** (un seul commit propre sur `develop`).

## Mise en production

Quand `develop` est prêt à partir en production :

1. Fusionner `develop` dans `main` en **fast-forward** si possible (pas de merge commit). Si un fast-forward n'est pas possible, le signaler avant de faire autrement.
2. Mettre à jour le numéro de version (semver) dans `package.json`, `pyproject.toml` et le badge de version du `README.md`, de façon cohérente entre les trois.
3. Créer un tag annoté `vX.Y.Z` sur `main` (même version que les fichiers ci-dessus) et le pousser.

Le push du tag déclenche automatiquement le workflow `.github/workflows/release.yml`, qui :
- compile le SDK JS et produit un zip du contenu compilé de `lib/`,
- construit le wheel Python (`.whl`),
- crée une **release GitHub en brouillon (draft)** nommée `vX.Y.Z`, avec les deux fichiers en pièces jointes et une description pré-remplie à partir de `.github/release_template.md`.

La description de la release est ensuite **complétée manuellement** (c'est un template, pas une génération automatique) avant de la publier depuis l'interface GitHub.

## Résumé du flux

```
branche perso -> PR -> validation (louis.charneux) -> squash merge -> develop
develop -> fast-forward -> main -> tag vX.Y.Z -> push
                                        |
                                        v
                        workflow release.yml (build JS + wheel,
                        draft release avec template à remplir)
```
