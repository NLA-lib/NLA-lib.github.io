# Luna generated results 04 — part 3

This report covers the final five named results assigned in `/tmp/nla-luna-cohort-04.json`.
The authored-binding alias check found no existing file with any assigned result key.
Exact exported templates were materialized at their supplied paths; UUIDs, IDs,
kinds, titles, formal bindings, mathematical expressions and math delimiter
segmentation are retained.

The editor snapshots have empty authored `object.references` lists. I checked
`reference_links.inherited` and list those associations below. No citation was
borrowed from a related declaration.

## Per-UUID results

### `d3e99f30-f02a-5df8-ad99-70eb3a91c3fa` — `basis-extension-gram-defect`

- Baseline revision: `009c699a5d17fe5b270360c6e22b644b2219f5bd50ba3a0f6067d7647157b4d9`.
- Source: `explore/content/statements/entry-d3e99f30-f02a-5df8-ad99-70eb3a91c3fa.md`; declaration `NLAlib.IsBasisExtensionErr.frobNorm_gramDefect_fromCols_sq_le` in `NLAlib/Matrix/Perturbation/BasisExtension.lean`.
- Outcome: `proposed`.
- Added an exact link on “Gram defect” to [Rounded extension of a basis by a block](/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/). The target defines the same support Gram defect formula for real matrices, matching this declaration’s real basis. Matrix notation and transpose style were already appropriate. The source body explicitly says “No printed source”; no citation was added.
- Unresolved: none identified for this editorial pass.

### `85b63a3d-6e69-5f62-b799-d61a036c63b6` — `bauer-fike`

- Baseline revision: `36ee7f47534b8dad512dbd1a9acd56d56caec32523ba91b5d3caf8b0e3f35a23`.
- Source: `explore/content/statements/entry-85b63a3d-6e69-5f62-b799-d61a036c63b6.md`; declaration `NLAlib.exists_norm_sub_le_pseudoConditionNumber_mul_specNorm` in `NLAlib/Matrix/Perturbation/Residual.lean`.
- Outcome: `proposed`.
- Removed inline citations to `GolubVanLoan2013` Theorem 7.2.2 and `HornJohnson2013` Theorem 6.3.2. Both exact inherited associations remain attached to the result. Matrix and eigenvalue-vector notation was already object-aware. No definition link added.
- Unresolved: none identified for this editorial pass.

### `095830f7-f116-5956-8031-a82709c77dd3` — `bernstein-ellipse-approx`

- Baseline revision: `bc435425aa815d99c756f699041a0afae0ca6660dd675cbae601704817025899`.
- Source: `explore/content/statements/entry-095830f7-f116-5956-8031-a82709c77dd3.md`; declaration `NLAlib.exists_degree_le_isUniformApproxOn_Icc_of_differentiableOn` in `NLAlib/Polynomial/Approximation/AnalyticApproximation.lean`.
- Outcome: `proposed`.
- Removed `[Trefethen2019, Theorem 8.2]`; the inherited `Trefethen2019`, Theorem 8.2 association remains. Added a link on “open Bernstein ellipse” to the exact formal definition [`NLAlib.openBernsteinEllipse`](/explore/library/declarations/NLAlib.openBernsteinEllipse/), which defines the foci and the parameterized ellipse used here. No formula or delimiter changes.
- Needs mathematical review: the linked declaration signature requires `1 < \rho`, but the readable body does not state this hypothesis. The link does not supply it as a theorem condition; review the prose separately rather than inferring or adding it in this pass.

### `1351eb09-b212-5c2c-b227-91317234b040` — `bernstein-inequality`

- Baseline revision: `5ab55ad2fec734912c0a19328373fc81bd347158e9f3583d0cc41116ad3aa816`.
- Source: `explore/content/statements/entry-1351eb09-b212-5c2c-b227-91317234b040.md`; declaration `NLAlib.HasSubexponentialMGF.measureReal_sum_ge_le_of_iIndepFun` in `NLAlib/Probability/SubExponential/Tail.lean`.
- Outcome: `proposed`.
- Removed `[Wainwright2019, §2.1.3]`; the exact inherited association remains. Linked the first “sub-exponential” occurrence to the formal definition [`NLAlib.HasSubexponentialMGF`](/explore/library/declarations/NLAlib.HasSubexponentialMGF/). The target defines the real-valued random-variable condition and variance/scale parameters used by this theorem. Removed duplicate sentence punctuation at the citation boundary; math was not changed.
- Unresolved: none identified for this editorial pass.

### `e402bfcb-bd27-537c-92fa-126246113c4e` — `best-approximant-interpolates`

- Baseline revision: `894a15a62b7ede46c0756b7496a8137cbf0854abfceb35c2fae00c767cf435a2`.
- Source: `explore/content/statements/entry-e402bfcb-bd27-537c-92fa-126246113c4e.md`; declaration `NLAlib.exists_eval_eq_of_isUniformApproxOn_minimaxError` in `NLAlib/Polynomial/Approximation/Equioscillation.lean`.
- Outcome: `proposed`.
- Removed inline `[Trefethen2019, Ch. 10]`; the inherited `Trefethen2019`, Ch. 10 association remains. Kept the source qualifier that the locator needs checking and that the referenced formulation is on `[-1,1]`. Added a link on “best approximation of degree at most $n$” to [Best uniform polynomial error](/explore/statements/89ab2263-0730-583c-89db-9695bea9604d/), whose definition uses the same continuous-function, compact-set and degree-at-most-$n$ setting. No math expression or delimiter segmentation was changed.
- Needs mathematical review: the inherited Ch. 10 locator is explicitly flagged by the source note for checking, and the cited formulation is described as being on `[-1,1]` while this result is stated on `[a,b]`. The source note is retained; the locator has not been independently corrected.

## References and checks

Inherited source associations are `GolubVanLoan2013` Theorem 7.2.2; `HornJohnson2013` Theorem 6.3.2; `Trefethen2019` Theorem 8.2; `Wainwright2019` §2.1.3; and `Trefethen2019` Ch. 10. No new citations were added. No global symbol-role changes proposed. `node explore/tests/check_notation.cjs` passed: 2,429 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 260 sources; all five UUIDs, generated IDs and result bindings matched, and source-to-output comparison confirmed original math expressions and delimiter segmentation are unchanged. Both inherited statement-reference targets and both library-declaration targets exist; all inherited bibliography keys have frontend `.bib` entries. `git diff --check` passed. No rendered preview or full content build was run.
