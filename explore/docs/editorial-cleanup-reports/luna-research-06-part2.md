# Luna research cohort 06 · part 2

Baseline revisions and declaration references were checked against `/tmp/nlalib-release-explorer/api/v1`; the linked declarations were located in the pinned Lean source. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `25803ed2-ec86-5406-bad1-718ee3c6f0bf` (`nlalib-frobnorm-sub-truncatedsvd-rsvd-sq`) | `1f8f9e93e03faaaa165a7043e699eaef7438f178aab229982f39af6eed1ca4a6` | `proposed` |
| `c895cc03-43bf-5ab0-831d-8720e5af74b6` (`nlalib-integral-frobnorm-sub-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `900a72661c642c1cbc4d8caf3279e9cde27be07851833cfcb7626b3e303ac841` | `needs-mathematical-review` |
| `bca995a9-a2a8-5034-b4bb-565f08cbb95b` (`nlalib-integral-frobnorm-sub-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `057b820a8cefd1866d16e3e055d025ba67804589c78c65e98cd009369bed464d` | `needs-mathematical-review` |
| `1266e5b2-8402-52e9-b859-115a81dc709f` (`nlalib-integral-frobnorm-sub-truncatedsvd-generalizednystrom-sq-le-one-add-of-haslaw-gaussianmatrix-of-truncatedgeneralizednystromrangedim-le`) | `a144275c2917de0d25e04538d4dcfc8ed1b49ceb402c693613ad5aff28c28549` | `proposed` |
| `93310fa9-d261-5f3c-b56f-f8a9bf1d8124` (`nlalib-integral-frobnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `d11bd06b135243d07518c227de9b4812bd707836bd24a5f99798d73cef0c6671` | `needs-mathematical-review` |

## Edits and references

- `nlalib-frobnorm-sub-truncatedsvd-rsvd-sq`: changed the sketch symbol to `\boldsymbol{\Omega}` and linked the existing wording “truncating within that range” to the [singular-value-decomposition definition](/explore/statements/d5bca832-63a1-5043-ab6e-03b8402a2a55/), which defines retaining leading singular components as a rank truncation.
- `nlalib-integral-frobnorm-sub-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix`, `nlalib-integral-frobnorm-sub-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix`, and `nlalib-integral-frobnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix`: braced `\mathbb{E}` only. Their bodies say “Under the same hypotheses” but do not locally define the positive gap ratio `\gamma` used in the formula. The source declaration encodes `singularGapRatio H h t`, but the readable entries leave the intended definition and cross-reference context unstated. No definition was inferred or inserted.
- `nlalib-integral-frobnorm-sub-truncatedsvd-generalizednystrom-sq-le-one-add-of-haslaw-gaussianmatrix-of-truncatedgeneralizednystromrangedim-le`: braced `\mathbb{E}` and changed the Greek test matrices to `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}`. The input is explicitly real; the sketch roles are matrices.
- The two RBKI Frobenius statements are related but distinct: one bounds the error of `\mathsf{rbki}(...)` itself and the other bounds its rank-`r` truncated output. Their formulas and formal declarations remain separate; no IDs were merged.
- No formulas, hypotheses, norms, constants, titles, IDs, result bindings, or delimiter segmentation were changed. No prose was added to create links.

Actual inherited citation pairs were read from declaration record `record.references`. The authored `object.references` arrays are empty; no references were added to front matter.

- `NLAlib.frobNorm_sub_truncatedSVD_rsvd_sq` — `Woodruff2014`, Lemma 44.
- `NLAlib.integral_frobNorm_sub_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, Theorem 9.2 (RBKI).
- `NLAlib.integral_frobNorm_sub_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, Theorem 9.2 (RSI).
- `NLAlib.integral_frobNorm_sub_truncatedSVD_generalizedNystrom_sq_le_one_add_of_hasLaw_gaussianMatrix_of_truncatedGeneralizedNystromRangeDim_le` — none.
- `NLAlib.integral_frobNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.

## Registry proposals

The two Greek test matrices in the generalized Nyström result use `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}`. Suggest a Greek-matrix role mapping for those symbols for later registry review; the global registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. This does not establish theorem correctness or formal/readable equivalence. The SVD target and inherited citation records were inspected; no rendered browser preview was available.
