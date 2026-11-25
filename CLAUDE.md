# CLAUDE.md

Working rules for this repository. Follow these (in addition to the usual conventions) whether you are Claude or anyone automating contributions.

## The project

ScriptSDK has two components versioned together (same version number in `package.json` and `pyproject.toml`):
- **JavaScript/TypeScript SDK** (`lib/`): compiled to JS via `npm run build` (output in `dist/lib/`).
- **Endstone plugin** (`src/endstone_scriptsdk/`): Python package, packaged as a wheel via `npm run buildp` (output in `dist/*.whl`).

## Branches and validation

- Always work on a dedicated branch (feature/fix), never directly on `develop` or `main`.
- A branch ends with a Pull Request. **No merge happens without explicit validation from louis.charneux.**
- Once validated, the PR is merged into `develop` as a **squash merge** (a single clean commit on `develop`).

## Shipping to production

When `develop` is ready to ship:

1. Merge `develop` into `main` as a **fast-forward** if possible (no merge commit). If a fast-forward isn't possible, flag it before doing anything else.
2. Bump the version number (semver) in `package.json`, `pyproject.toml`, and the version badge in `README.md`, keeping all three consistent.
3. Create an annotated tag `vX.Y.Z` on `main` (matching the version in the files above) and push it.

Pushing the tag automatically triggers the `.github/workflows/release.yml` workflow, which:
- compiles the JS SDK and produces a zip of the compiled contents of `lib/`,
- builds the Python wheel (`.whl`),
- creates a **draft GitHub release** named `vX.Y.Z`, with both files attached and a description pre-filled from `.github/release_template.md`.

The release description is then **filled in manually** (it's a template, not an auto-generated changelog) before publishing it from the GitHub UI.

## Flow summary

```
personal branch -> PR -> validation (louis.charneux) -> squash merge -> develop
develop -> fast-forward -> main -> tag vX.Y.Z -> push
                                        |
                                        v
                        release.yml workflow (build JS + wheel,
                        draft release with template to fill in)
```
