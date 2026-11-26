# Luna matrix definitions cohort 05, part 2

This report covers only the second five assigned definitions. Baseline revisions and editor evidence were checked in the pinned release Explorer objects. All five objects have empty authored `object.references` and `reference_links: null`; inherited citations below were read from each bound declaration's `record.references`.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `6d8b12f4-2783-5f4b-8c76-53d3c62f914f` | `explore/content/statements/nlalib-lanczosquadrature-6d8b12f4.md` | `665ef9b65e54f837698391169b40bb1d0e0a7118575aa6890a4d960ff6648282` | `proposed` |
| `8f827d72-be63-547b-b653-014c1f9c9eeb` | `explore/content/statements/nlalib-mgs-factorprogram-8f827d72.md` | `0d1bb352514d1dcf26432591f54258764ea8848802e396a594ca7d79b7ab30d2` | `already-consistent` |
| `8647f4e3-cefb-5ae0-9fac-51da15589631` | `explore/content/statements/nlalib-nystrombki-8647f4e3.md` | `dbcb46bf508b089ebab1bd88c30110815cd6598311f5f6aa2a0c484eae46502b` | `proposed` |
| `062e6bec-6230-5042-9571-8edf07f8ae3c` | `explore/content/statements/nlalib-oddmatrixiterate-062e6bec.md` | `46c11c67b64797d0203ef4d440cf5604c3b84d89564c4b27d894dc203214a325` | `proposed` |
| `27bc7cdd-514e-5fd6-8349-3561c58491be` | `explore/content/statements/nlalib-polarnewtoniterate-27bc7cdd.md` | `e28855953907632fafa202e388c424f0c6a748329f1476d42e0a38f1a113c152` | `already-consistent` |

## Edits and link verification

- **Lanczos quadrature**: linked the existing “Hermitian” term to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`, and “Lanczos compression” to the Lanczos process definition, UUID `d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239`. These definitions directly state the Hermitian condition and the Lanczos compression. The bound function has `[RCLike 𝕜]`; neither target imposes real-only scope. The formula, weights, and assumptions sentence remain unchanged.
- **In-place modified Gram–Schmidt**: already consistent for this scope. Procedure steps, Hermitian coefficient, stored matrix, and scratch-cell counts are unchanged. Its declaration has no inherited references.
- **Nyström block Krylov iteration**: changed the Greek matrix symbol `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked “Nyström construction” to the Nyström approximation definition, UUID `254f7f6f-1199-596d-9347-4d32f1eab873`. The target directly defines that construction for Hermitian positive-semidefinite matrices with the adjoint formula; the bound `NLAlib.nystromBKI` is `[RCLike 𝕜]`. The block powers, formula and explanatory sentence remain unchanged.
- **Polynomial polar iteration**: linked the existing “singular values” term to UUID `581c9098-24f3-55b6-bd36-a47af48b21ff`, whose definition covers singular values of general real/complex matrices. The Gram-form update and singular-vector statement are unchanged. No direct polar-factor definition target was found.
- **Newton polar iteration**: already consistent for this scope. The rectangular real-or-complex domain, pseudoinverse adjoint, iteration and partial-isometry claim are unchanged. No standalone polar-decomposition definition target was found; no related method link was substituted.

## Citation evidence

Declaration references checked at the pinned API records:

- `NLAlib.lanczosQuadrature`: `GolubMeurant2010`, Chapter 6.
- `NLAlib.MGS.factorProgram`: none.
- `NLAlib.nystromBKI`: `TroppWebber2023`, Algorithm 5.8.
- `NLAlib.oddMatrixIterate`: `AmselPerssonMuscoGower2026`, §2.
- `NLAlib.polarNewtonIterate`: `Higham2008`, §8.3.

No assigned body contains an inline bibliographic citation string. These actual declaration associations were already inherited and rendered; no citation was copied or added. Any references on cross-linked targets remain associated with those target entries; none were copied to these statements.

## Validation and unresolved items

Verified UUIDs and field scopes of all linked definition targets. The Nyström target and source support complex Hermitian positive-semidefinite matrices; the singular-values target is not real-only. The missing standalone polar decomposition/factor definition is the remaining link gap for the two polar-related definitions. No mathematical formula, field restriction, condition, identity, title, ID, binding, or metadata changed. The only source-level formula edit is the Greek matrix font correction; inline/display math segmentation is unchanged. No helper expansion was made.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

The Nyström correction identifies `\Omega` as a matrix. No global notation registry change was made.
