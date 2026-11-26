# Luna matrix definitions cohort 04, part 1

This report covers only the first five files in the assigned matrix cohort. Baseline revisions, evidence and reference associations were checked in the pinned release Explorer editor objects under `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`. All five objects have `object.references: []`, `reference_links: null`, and authored-definition evidence without a Lean declaration binding. There are no inherited declaration citations. No inline bibliographic strings were present, so no citation associations were moved or added.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `c3defe75-5c9e-5827-8089-7c905475120c` | `explore/content/statements/inverse-iteration-c3defe75.md` | `87ea1ab38dc6b82ee2593c7dc5e336bda39e25fcd5181496764361bd01f4ddef` | `already-consistent` |
| `acb8b8c2-271a-594d-9431-e0d4447ee5a0` | `explore/content/statements/iterative-refinement-acb8b8c2.md` | `d028d979dda4215dd00f16e16bd3de2c772d36725d1ce4ed79c1cde3e608b0a7` | `already-consistent` |
| `4d02220c-4aa0-5cd0-8df1-afff8a1279ba` | `explore/content/statements/iterative-sketching-4d02220c.md` | `bdd207f0c0d17b54a2759935b21a6fb73c17cedcef5600fdf65cb6edef4056eb` | `already-consistent` |
| `9daaad7c-093e-59a8-a0a5-b86b31c81bc3` | `explore/content/statements/jacobi-eigenvalue-method-9daaad7c.md` | `d1f7c66e9c97a95d5bcee7ff78959b8aba2e0b6b7242e9c7ddfefc865e9e4394` | `proposed` |
| `615008ca-f5db-5cff-ab6b-b07f178cbd05` | `explore/content/statements/krylov-space-and-grade-615008ca.md` | `5b5e290902db715929f56c11c7ee23d8435fa46e1cfe617719cfb680b81e6992` | `already-consistent` |

## Changes and scope

- **Inverse iteration**: already consistent for the assigned scope. The matrix/vector symbols are explicit, and the shift, invertibility condition, solve, and normalization remain unchanged. No dedicated Rayleigh-quotient definition target was found; no related algorithm link was substituted.
- **Iterative refinement**: already consistent for the assigned scope. Its exact-versus-computed steps and approximation signs are retained, including the existing display-math segmentation. No citation or compatible definition link was needed.
- **Iterative sketching**: already consistent for the assigned scope. Matrix/vector notation, adjoints, damping parameter and convergence caveat are explicit. No indirect sketching or embedding link was added.
- **Jacobi eigenvalue method**: linked the existing term “Hermitian” to the Hermitian spectral-decomposition definition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`. That target directly states the Hermitian condition and does not restrict the scalar field to real. No plane-rotation target was found; no related substitute or new clause was added. The method and pivot schedule text are unchanged.
- **Krylov space and grade**: already consistent with its explicitly real-only domain `$\mathbf{A}\in\mathbb R^{n\times n}$`, `$\mathbf{b}\in\mathbb R^n$`. That field restriction is preserved. It remains a real-only definition; this batch did not broaden it to cover complex matrices/vectors.

## References and validation

All five editor objects have empty authored `object.references`, `reference_links: null`, and no declaration evidence, so there are no inherited declaration references to check or reuse. No inline bibliographic citation strings occur in the bodies. No citation association was added from related declarations or statements. IDs, UUIDs, kinds, formulas, conditions, metadata, and math-environment segmentation were preserved; no helper content was expanded.

Verified the front matter and prose of the linked Hermitian spectral-decomposition target. Its matrix field is not restricted to real scalars. `node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

No notation registry additions were needed. No global registry change was made.
