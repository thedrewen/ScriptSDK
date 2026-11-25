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
2. Bump the version number (semver) in `package.json`, `package-lock.json`, `pyproject.toml`, and the version badge in `README.md`, keeping all consistent.
3. The tag `vX.Y.Z` (matching the version in the files above) must be created by a human, not pushed by an automated agent: tag protection rules on `v*` reject pushes from Claude's GitHub App. So Claude (or whoever automates this) stops here and:
   - asks louis.charneux to create and push the tag themselves — simplest via GitHub's "Draft a new release" UI (tag `vX.Y.Z` targeting `main`, then **Publish**, since the tag is only created/pushed on publish, not on save-as-draft),
   - hands them a filled-in release description, written to the structure of `.github/release_template.md` but with the sections actually filled from the real changes since the previous tag (not left as placeholders).

Pushing the tag automatically triggers the `.github/workflows/release.yml` workflow, which:
- compiles the JS SDK and produces a zip of the compiled contents of `lib/`,
- builds the Python wheel (`.whl`),
- creates/updates a **draft GitHub release** named `vX.Y.Z`, with both files attached and the description reset to the raw `.github/release_template.md` placeholders (it always overwrites the body).

So the filled description Claude prepared is pasted in manually, replacing the placeholders, before publishing the release from the GitHub UI.

## Flow summary

```
personal branch -> PR -> validation (louis.charneux) -> squash merge -> develop
develop -> fast-forward -> main -> bump version -> louis.charneux creates & pushes tag vX.Y.Z
                                                                |
                                                                v
                                        release.yml workflow (build JS + wheel,
                                        draft release, body reset to template)
                                                                |
                                                                v
                                picks up Claude's filled description -> publish
```
