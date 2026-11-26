# Luna Krylov cohort 03, part 2

This report covers only the second five files in the assigned `krylov` cohort. Baseline revisions, evidence and reference associations were checked in `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`; linked declaration records were checked in the pinned declarations API. Every object has `object.references: []` and `reference_links: null`. Both linked declaration records have empty `record.references`; the other three entries are authored definitions without declarations. No inline bibliographic strings occur in these bodies, so no references were moved or added.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58` | `explore/content/statements/nlalib-isblockgolubkahan-4dfc5d02.md` | `cf6fe96f0d82d295479cd8e49950ee68af905b7423962c394784fa8314541039` | `proposed` |
| `593daa98-8a52-5a89-a792-f46844fd76d6` | `explore/content/statements/nlalib-isblockgolubkahanerr-593daa98.md` | `edc38a04a724511e691e083e5b11de4d0ff2f8ee469f2091bf470cb570997b58` | `proposed` |
| `d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239` | `explore/content/statements/lanczos-process-d9e8ae48.md` | `957571ad6668dcc5975d168dd9ad1013d9595ba5072d4a10f6e766e579d0800b` | `proposed` |
| `b7f38d6d-61b5-5315-97b5-ad37f607e474` | `explore/content/statements/minres-b7f38d6d.md` | `8d8393bd56fc4dffbd4c56010461e13cc130c740207312b862155c0d6cfaa657` | `proposed` |
| `c9704060-abeb-5a36-9da4-7c1c288ebce6` | `explore/content/statements/preconditioned-minres-c9704060.md` | `cbe6d2e058e4a33e785100d25cf5d75e0c4a549acc61120287cbd19a733a1d1e` | `proposed` |

## Changes, links, and scope

- **Block Golub–Kahan process**: changed the Greek matrix symbol `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing phrase “exact extension” to the exact basis-extension definition, UUID `12a7ec72-6c64-59e6-b7de-7aff8d055ba2`. Its declaration `NLAlib.IsBasisExtension` supports `[RCLike 𝕜]`, matching the process declaration's real-or-complex field. All formulas, shapes, and relation conditions remain unchanged.
- **Rounded block Golub–Kahan process**: changed `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked “rounded extension” to the definition of rounded basis extension, UUID `fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393`. Its pinned signature is real-valued, matching the source process declaration's `Matrix ... ℝ`; the source's `\mathsf{T}` transpose is therefore retained. No inequalities or norms changed.
- **Lanczos process**: linked “Hermitian matrix” to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`. The target begins with the Hermitian condition and does not impose a real-only field. The recurrence, compression and breakdown description are unchanged.
- **MINRES**: linked the existing phrase “Lanczos-based short recurrence” to the Lanczos process definition, UUID `d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239`. Its Hermitian-matrix context includes the source's real-symmetric case. The real-only Krylov-space definition was inspected and is compatible, but no link was added inside or around the existing mathematical expression, preserving its math-environment segmentation. No positive-definiteness, solvability, or termination hypothesis was added.
- **Preconditioned MINRES**: linked “Hermitian” to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`; the target has no real-only field restriction. No link was made to the standalone MINRES definition, whose scope is specifically real symmetric, because this source allows general Hermitian matrices. The transformed system, residual norm, and spectrum wording are unchanged.

## Citation evidence and validation

All five pinned editor objects have empty authored `object.references`; each has `reference_links: null`. The exact and rounded block Golub–Kahan declarations (`NLAlib.IsBlockGolubKahan`, `NLAlib.IsBlockGolubKahanErr`) both have no inherited declaration references (`record.references: []`). The Lanczos process, MINRES, and preconditioned MINRES entries are authored definitions with no declaration binding. No bibliography text occurred in the five bodies. No citations were transferred from neighboring or related declarations.

Verified the exact target sources and UUIDs. The exact process and exact extension support real/complex scalars; the rounded run and rounded extension are real-valued; the MINRES Krylov target is real-only and was not inserted into math; Hermitian targets use adjoint notation without a real-only restriction. `node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run. These checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

No relocations, duplicates, proof sources, or global notation changes were proposed. IDs, UUIDs, formal bindings, conditions, matrix dimensions, matrix/vector notation apart from the Greek matrix font correction, provenance and review metadata were preserved.
