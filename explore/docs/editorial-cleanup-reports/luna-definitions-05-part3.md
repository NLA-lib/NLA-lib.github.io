# Luna matrix definitions cohort 05, part 3

This report covers only the final five assigned definitions. Baseline revisions and editor evidence were read from the pinned Explorer objects; actual declaration `record.references` were checked for each bound definition. Each editor object's authored `object.references` is empty and `reference_links` is null.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `469e6e39-a086-5aba-9b14-ee0d2e5df1f0` | `explore/content/statements/nlalib-polarschulziterate-469e6e39.md` | `4f181fd2699996d5a251c510d958f5b89f2e07a0a4f1acd10eb21975023b2308` | `already-consistent` |
| `ce25720b-6102-5bb3-a0e2-a679814dd9d8` | `explore/content/statements/nlalib-rbki-ce25720b.md` | `ab1635a3a7940ba16d68b38244babf81d7e9413d23654f6025c6272f207206d6` | `proposed` |
| `c07e970e-5e57-5ffc-95c4-0a61ec4b2f4d` | `explore/content/statements/nlalib-refinementrun-c07e970e.md` | `13d60f000cfd7801b6bcb77451b0bdf0d04809442540775b813afbe01c3fdb99` | `already-consistent` |
| `90192996-6dc6-5054-aca9-ae0e5756c82c` | `explore/content/statements/nlalib-schur-denseschuralgorithm-90192996.md` | `2ae64d6d00dac14a57ce45fdd1f6c688ba60a83727ff57c5b3607161edf3bdab` | `already-consistent` |
| `cbea4e58-b0f0-50f9-8290-46f3da3fd35f` | `explore/content/statements/nlalib-schur-verifiedschuralgorithm-cbea4e58.md` | `4c09e3bcfd3c7e14c4f0a541c7b3ddf44ab4b8897ec631e111e108ac548d4fed` | `already-consistent` |

## Changes and citation associations

- **Newton–Schulz polar iteration**: already consistent for the assigned scope. Its rectangular update and convergence-hypothesis statement are unchanged. No standalone polar-decomposition definition target was found; no related iteration link was substituted.
- **Randomized block Krylov iteration**: corrected the Greek start-block matrix from `\mathbf\Omega` to `\boldsymbol{\Omega}` throughout the prose and both formulas. No other part of the iteration, range expression, field statement, or rank behavior changed. No direct semantic link target was identified in the existing body terms.
- **Refinement run**: already consistent for this scope. Its formula, norms, nonnegative parameters, unrestricted start, and lack of smallness assumptions are unchanged.
- **Dense Schur certificate**: already consistent for this scope. The unit-cost model description, instruction budget, work/span formula, and cost-accounting text remain unchanged.
- **Verified Schur certificate**: already consistent for this scope. Its fixed program, every-tape flag-conditional claim, dimensions, and work/span formula are unchanged.

Inherited declaration references from the pinned source records:

- `NLAlib.polarSchulzIterate`: `Higham2008`, §8.3.
- `NLAlib.rbki`: `TroppWebber2023`, Algorithms 5.4 and 5.5; `MuscoMusco2015`, Algorithm 2.
- `NLAlib.RefinementRun`: `CarsonHigham2018`, Algorithm 1.1.
- `NLAlib.Schur.denseSchurAlgorithm`: none.
- `NLAlib.Schur.verifiedSchurAlgorithm`: none.

No inline bibliographic strings occur in these bodies. No citation associations were added or copied. Formula segmentation, field conditions, assumptions, operation steps, titles, IDs, UUIDs, formal bindings, and review metadata were preserved. No raw helper content was expanded.

## Validation and unresolved items

No direct polar-decomposition definition was found for the two polar-iteration definitions in the cohort; that remains an unlinked concept. No additional field, pivot, stability, or convergence assumptions were inferred.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

The RBKI source identifies `\Omega` as a matrix; consider a reviewed role declaration for this symbol if registry coverage is expanded. No global registry change was made.
