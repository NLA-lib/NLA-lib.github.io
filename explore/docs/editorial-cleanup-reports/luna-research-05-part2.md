# Luna research cohort 05 · part 2

Baseline revisions and source evidence were checked against the pinned release snapshot at `/tmp/nlalib-release-explorer/api/v1`. The five assigned statement files were reviewed against their linked Lean declarations and declaration records. This report describes an editorial proposal only; no proposal was submitted.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `a5e449d4-fd34-5212-96fa-75ce7fa2feaf` (`matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-singulargapratio-of-haslaw-gaussianmatrix`) | `4aa8d1abd8c23cd0778a9427c981ccd9c0a7e894578c0f6cad3a245222fed8a8` | `proposed` |
| `e59d814f-e0b1-56c7-af02-203f32b258da` (`matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-singulargapratio-of-haslaw-gaussianmatrix`) | `e110b36661aee6d8a0ff34bb57e545b61012ecf6f3a3546e9c1407154e014e49` | `proposed` |
| `79ce5973-651d-563f-9f9a-68c47fe92daf` (`nlalib-ae-charpoly-separable-of-haslaw-complexgaussianmatrix`) | `488eecde13e5f600d866d344609bb191c47da5a69cac6cd07c3f64d1d7bf4cf7` | `already-consistent` |
| `9e96e2c6-478a-5eef-8072-3b65a72a0b33` (`nlalib-blockkrylov-storedoutput-eq-rbki`) | `4af32bee684ee4ce3617b25af7430d28ef2820b607b79159d537fde94538b902` | `already-consistent` |
| `8c857b38-dcb9-5698-b8b0-0f647fe28c56` (`nlalib-cgs2-cgs2extendroutine-meets-exact`) | `67e5b55f7ec5b7d6ed680863e13f11899c4f6daaf68d758d62e1071fbb939df0` | `proposed` |

## Edits, references, and links

- The first two entries had unbraced `\mathbb E` in their displayed expectations; changed only to `\mathbb{E}`. All formulas and display segmentation remain intact. Their declaration signatures use positive-semidefinite real matrices and Gaussian matrix inputs; matrix `A` and `X` remain bold, and scalar indices, spectral values, and polynomial iteration counts remain unbolded.
- The two gapped nuclear-norm results share the title and block id `gapped-nuclear`, but state separate bounds for NysSI and NysBKI with distinct formulas and iteration parameters. They are related results with distinct Lean declarations and UUIDs; no IDs or statements were merged.
- In `nlalib-cgs2-cgs2extendroutine-meets-exact`, linked the existing phrase “exact extension contract” to the exact-extension definition [NLAlib.IsBasisExtension](/explore/statements/12a7ec72-6c64-59e6-b7de-7aff8d055ba2/). The target defines exact extension for `RCLike` scalar fields, matching the generic extension context. It is a direct definition, not a related algorithm result.
- `nlalib-ae-charpoly-separable-of-haslaw-complexgaussianmatrix` and `nlalib-blockkrylov-storedoutput-eq-rbki` were already consistent in vector/matrix fonts and transpose notation. No direct, scope-matching definition target was found for “simple spectrum” or “characteristic polynomial”; no link was added. No formula or wording changes were made to these entries.

Actual inherited citation pairs from declaration record `record.references`:

- `Matrix.PosSemidef.integral_nuclearNorm_sub_truncatedSVD_nystrom_pow_mul_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `Matrix.PosSemidef.integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `NLAlib.ae_charpoly_separable_of_hasLaw_complexGaussianMatrix` — none.
- `NLAlib.BlockKrylov.storedOutput_eq_rbki` — none.
- `NLAlib.CGS2.cgs2ExtendRoutine_meets_exact` — none.

The `object.references` fields are authored associations and empty here; the two Tropp–Webber references are inherited and already rendered. No front-matter citation was added. No citations were borrowed from related declarations.

## Unresolved issues and registry proposals

No missing hypotheses or source discrepancy was established in this batch. The expectation bounds have similar framing but describe distinct algorithms as noted above. A possible notation registry proposal for later review is Greek matrix roles `\Omega`/`\Psi` on neighboring Nystrom algorithm entries; none of the five assigned statements required such an edit, and the global registry was not changed.

## Validation and limits

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks cover parsing and whitespace, not mathematical correctness. The definition target and declaration citation records were inspected in the pinned snapshot; no rendered browser preview was available.
