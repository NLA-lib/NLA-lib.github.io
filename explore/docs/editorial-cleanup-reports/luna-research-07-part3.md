# Luna research cohort 07 · part 3

Baseline revisions and citation associations were checked against `/tmp/nlalib-release-explorer/api/v1`; the Lanczos, block Golub–Kahan, and refinement definitions were inspected in the pinned Lean source. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `22bf30ab-6185-5d8f-8b97-3a1ef452ff55` (`nlalib-krylov-golubkahan-band-isexactstoredrun-mul-conjtranspose-mul-conjtranspose-eq-rbki`) | `4bf5c7e897504277b763bbc86f352bed7bad7a2ed0305ec0325b83d53139b398` | `proposed` |
| `161639a0-5d37-530b-9f3f-52b80780a847` (`nlalib-krylov-lanczos-runs-solve`) | `f2782cf17ba90ea557688c0416cd1c18445dac5b4b091f4796fadcf0f86f2854` | `proposed` |
| `3318f77c-2fb6-5ae5-a52e-c7239d83ab69` (`nlalib-krylov-lanczos-stmtcost-solve`) | `4ec8fab265919deb4bf3a51f0d4c6e6533fc55a6a8fb634c714f9dd005d012e9` | `already-consistent` |
| `ca6ffb21-49a0-54fc-81a5-dae0dd103639` (`nlalib-krylov-lanczos-stmtpeak-solve-le`) | `b1fe3aac396d936f798f1aaa7aee2963cb967e527fa36932e5e7dc93b3287e93` | `already-consistent` |
| `4665c197-4b8f-5074-bbc4-261137cc421b` (`nlalib-linearsystems-refinement-certification-algorithm-checked`) | `7d56322500ba75be23800ef661c9283908deefcf3fef5a1442c8af78ee590dd1` | `needs-mathematical-review` |

## Edits and links

- In `nlalib-krylov-golubkahan-band-isexactstoredrun-mul-conjtranspose-mul-conjtranspose-eq-rbki`, changed the matrix start block from `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing “exact run” phrase to the [Block Golub–Kahan process definition](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/). The definition is generic over real or complex scalars; this result specializes to real matrices.
- In `nlalib-krylov-lanczos-runs-solve`, linked the existing “call” and “scratch bounds” references to the [operation budget](/explore/statements/3318f77c-2fb6-5ae5-a52e-c7239d83ab69/) and [scratch bound](/explore/statements/ca6ffb21-49a0-54fc-81a5-dae0dd103639/), respectively. Linked “Hermitian Lanczos” to the [Lanczos process definition](/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/) under its stated symmetry condition; this target is specifically Hermitian. Linked the existing output-convention phrase to the [guarded three-term Lanczos definition](/explore/statements/8a730a7c-e552-5641-bd95-fa635dcebc98/), which covers zero input, zero cap, and early breakdown.
- The operation-budget and scratch statements were already consistent and were left unchanged. The scratch/workspace symbols are scalars or resource counts; no bolding applies.
- The refinement theorem's vectors remain bold and all scalar error and contraction parameters remain unbolded. No notation change was needed.
- No formulas, assumptions, titles, IDs, result bindings, or delimiter segmentation were changed. Links preserve original labels and wording.

Actual inherited citations from each linked declaration's `record.references` (the authored `object.references` arrays are empty):

- `NLAlib.Krylov.GolubKahan.Band.IsExactStoredRun.mul_conjTranspose_mul_conjTranspose_eq_rbki` — none.
- `NLAlib.Krylov.Lanczos.runs_solve` — none.
- `NLAlib.Krylov.Lanczos.stmtCost_solve` — none.
- `NLAlib.Krylov.Lanczos.stmtPeak_solve_le` — none.
- `NLAlib.LinearSystems.Refinement.Certification.algorithm_checked` — `CarsonHigham2018`, Corollary 3.3.

## Unresolved issue

`nlalib-linearsystems-refinement-certification-algorithm-checked.md` says “every interpretation satisfying the three contracts” without identifying those contracts in the shared statement. The Lean source `NLAlib/LinearSystems/Refinement/Certification.lean` describes an update contract and residual/correction-solve contracts and notes that a reader must check they are intended. This may materially affect how the guarantee applies to concrete operations. The report leaves this as `needs-mathematical-review`; no contract was inferred or added.

## Registry proposals

No new symbol-role mappings are needed in this group. The global notation registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. Definition targets and citation records were inspected; no rendered browser preview was available.
