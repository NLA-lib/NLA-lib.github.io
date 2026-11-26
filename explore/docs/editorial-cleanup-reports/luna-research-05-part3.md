# Luna research cohort 05 · part 3

Baseline revisions and declaration evidence were checked against `/tmp/nlalib-release-explorer/api/v1`. The five assigned statements were reviewed against their Lean source. This is an editorial proposal only; no proposal was submitted.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `4e574a88-17af-5903-a933-df1cef419a4e` (`nlalib-cgs2-cgs2extendroutine-meets`) | `9ed1170fa0b77816252e33f20b5faf3b6452cf98bf9c1484a3de857ae250ed00` | `proposed` |
| `5b8c8de4-ac54-5a02-a6ea-5cf2c96cee62` (`nlalib-computation-norm-inv-mulvec-sub-le-of-ischoltrace`) | `ea88d509ae1cccc5111b416867bab1b9575fa3da56161b1c393982d6dcb7e8d3` | `needs-mathematical-review` |
| `e9cd7afc-bec4-59b6-b5d9-8b006e4b1d5b` (`nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix`) | `7fa16fe17eeeea3790b40b4f1fa05a12352bb1ab75b534bdee158256fc22d7ee` | `proposed` |
| `84d02c77-a2fc-5e91-9252-6a5c17632cf4` (`nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix`) | `2910db568f6cc5625f869628f82d4acb0487f9184dfecefe070d35fe31a1522b` | `proposed` |
| `dcf428cb-b48d-5638-ac05-ad9f844a1630` (`nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rbki-sq-le-of-haslaw-gaussianmatrix`) | `e28b5d815aeba6aff69e27092146ebedd64e59bef0b0d3dfcde55e2bf6027f82` | `proposed` |

## Edits, references, and relationships

- `nlalib-cgs2-cgs2extendroutine-meets`: linked the existing “rounded extension” term to the [`NLAlib.IsBasisExtensionErr` definition](/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/), whose contract uses the same window and parameters. The statement's scalar error quantities remain unbolded; it contains no vector or matrix symbols requiring font changes.
- `nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix`, `nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix`, and `nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rbki-sq-le-of-haslaw-gaussianmatrix`: braced `\mathbb{E}` in each displayed expectation. Scalar spectral values, gap ratio, epsilon, and iteration/depth parameters remain unbolded; `\mathbf{A}` and `\mathbf{X}` remain matrix-font symbols.
- The two nuclear-norm entries state related sufficient complexity bounds for distinct algorithms: NysSI uses power steps with dependence `1/\gamma`; NysBKI uses depth with dependence `1/\sqrt{\gamma}`. Their UUIDs, declarations, conditions, formulas, and names are distinct; they were not merged.
- The RBKI statement's final sentence points to companion gapped spectral- and Frobenius-norm forms, but does not name their individual identities. No link was attached to a generic phrase that could not unambiguously point to both companions. This cross-reference wording is retained as authored.
- `nlalib-computation-norm-inv-mulvec-sub-le-of-ischoltrace` has consistent notation and was not edited. Its “computed Cholesky factor as above” phrase depends on context not present in this standalone body. The linked formal declaration `NLAlib.Computation.norm_inv_mulVec_sub_le_of_isCholTrace` requires a positive-definite matrix, an `IsCholTrace` hypothesis, an entrywise factor-error bound, and input/substitution trace conditions; those are not stated explicitly here. The Lean docstring refers to the preceding `IsCholTrace.pos_and_specNorm_sub_le` result. This needs editorial review to determine whether the cross-entry context is intended; no hypotheses were inferred or added. The exact Cholesky-factorization definition alone would not establish these computed-factor assumptions, so no link was added.

Actual inherited citations, read from each linked declaration's `record.references` (the authored `object.references` arrays are empty). No citation front matter was added:

- `NLAlib.CGS2.cgs2ExtendRoutine_meets` — none.
- `NLAlib.Computation.norm_inv_mulVec_sub_le_of_isCholTrace` — `CarsonHigham2018`, (2.3).
- `NLAlib.exists_forall_integral_nuclearNorm_sub_truncatedSVD_nystrom_pow_mul_le_of_singularGapRatio_pos_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `NLAlib.exists_forall_integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_of_singularGapRatio_pos_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rbki_sq_le_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10; `MartinssonTropp2020`, Theorem 11.11.

## Registry proposals

No global registry change was made. These assigned statements did not require new role mappings; the audited matrix and scalar roles already follow the notation guide.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. This checks parsing and whitespace, not theorem correctness or formal/readable equivalence. The exact-extension definition and all inherited citation pairs were inspected in the pinned snapshot; no rendered browser preview was available.
