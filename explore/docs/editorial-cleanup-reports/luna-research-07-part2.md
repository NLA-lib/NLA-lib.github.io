# Luna research cohort 07 · part 2

Baseline revisions and references were checked against `/tmp/nlalib-release-explorer/api/v1`; process and certification definitions were read from the pinned snapshot. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `975091bf-ef10-570b-99f0-6e3b30609d5e` (`nlalib-isblockgolubkahan-mul-blockprefix-right-eq`) | `4155d395c25f20e3d2562205b311ee2aef5fe1672e98fd0721582c1ee684fcfc` | `proposed` |
| `c52e956e-6658-55db-a3ff-01104cb2ade8` (`nlalib-isblockgolubkahan-range-blockprefix-right`) | `e433950d8157a556fe810f287b22d6773d0c40bfe5704a036dc2175ef8c4e044` | `proposed` |
| `d8206024-5e81-58e5-ae97-3f5e3e459750` (`nlalib-krylov-golubkahan-band-certification-certifies`) | `4fbbe88941709ff3cd21a18c7e051da10abb77d64398ac27f7a958d7edba73c8` | `proposed` |
| `34337bed-f4b8-5514-b1d8-717d0f0e391b` (`nlalib-krylov-golubkahan-band-certification-original-staticbudget`) | `f4b9a780d2f78aa821a16c67f4ea8ded54268bd8b682cd96b850d8f5b6090727` | `already-consistent` |
| `5c5ad6bf-3fdc-55bd-a427-6489b7c4a18d` (`nlalib-krylov-golubkahan-band-certification-staticpeak-solveprogram-le-solvepeak`) | `4a3c24231ab31765de4db86dabe8a9a0a33bc0df89747e203711fcc214a7a143` | `already-consistent` |

## Edits and links

- In the first block relation and the Krylov-range statement, linked the existing phrase “exact run” to the [Block Golub–Kahan process definition](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/). It defines exact runs as outputs related to the input and supports both real and complex fields.
- In the right-range statement, changed the sketch symbol from `\mathbf\Omega` to `\boldsymbol{\Omega}` throughout. `\Omega` is the matrix start block; the powers and dimensions, including the displayed range and prose companions, are unchanged.
- In the band-certification statement, linked “exact contract” to the [exact basis-extension definition](/explore/statements/12a7ec72-6c64-59e6-b7de-7aff8d055ba2/) and “exact run” to the process definition above. Both targets match the real-matrix certification's concepts. The universal quantifiers and certification conclusions are unchanged.
- The primitive static-budget and static-peak statements were already consistent in notation and were left unchanged. No formulas, conditions, titles, IDs, or bindings were altered.

All five declaration records have no inherited citations; their authored `object.references` arrays are also empty. No citations were added.

## Registry proposals and unresolved issues

Suggest a Greek-matrix role for `\Omega` in the block Krylov range statement for later registry review. The global registry was not changed. No unresolved mathematical ambiguity was found. The range statement's “same result group, listed under Further results” is retained; it refers to several companion results without naming one target, so no single link was attached.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish mathematical correctness or formal/readable equivalence. The definition targets and inherited-reference records were inspected; no rendered browser preview was available.
