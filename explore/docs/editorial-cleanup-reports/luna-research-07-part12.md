# Luna research cohort 07, part 12

Scope: manifest `research[11]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements reviewed. This is an editorial review, not a mathematical or formalization validation.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- |
| `188aac98-6bd6-511d-a625-99a6935d7b28` | `explore/content/statements/rbki-any-block-gapless-error.md` | `26b9e9612e7a07196763bafbbd7c5f864d052e0f9b7d5d4df443e5c1eca5d5d3` | `needs-mathematical-review` | No source edits. | None on object |
| `0bd6d1ef-ab85-5de8-85b7-6872fc39dae0` | `explore/content/statements/rbki-block-monotonicity.md` | `7a82422b44d04465ffae14de4047ed1615747e99eeace8dc20bb065fd1a3bd0e` | `proposed` | Replaced unbraced `\\mathbf\\Omega` and `\\mathbf\\Omega'` with explicit `\\boldsymbol{\\Omega}` and `\\boldsymbol{\\Omega}'` notation. | None on object |
| `49c904f7-6031-57df-9638-f96650269510` | `explore/content/statements/rbki-gapless-error.md` | `8e3030489445e93d7927dac5dd2734da6ac03b6a481efbd379c1637693a69299` | `needs-mathematical-review` | No source edits. | None on object |
| `6cec8318-a6a3-5186-a4c8-1928457d0cc8` | `explore/content/statements/rbki-gapped-error.md` | `37a07281b55147538d7f93a250ecedb599e3ab22db7ea862a7e88805db70e022` | `needs-mathematical-review` | No source edits. | None on object |
| `2715e07f-95d2-5b31-863a-8adcfb6d65d4` | `explore/content/statements/rbki-multiplicity-lower-bound.md` | `f5bf920e91c4d094fa7961d2dbb7443fc584245a98d8883d3843956c280ed4b5` | `proposed` | Replaced unbraced/braced `\\mathbf\\Omega` forms with `\\boldsymbol{\\Omega}` notation throughout. | None on object |

## Evidence and unresolved issues

- Each editor object's `object.references` list is empty. No citation associations were added. The source docstrings for the expectation and probability bounds contain literature citations, but those comments do not establish that the references are inherited by these statement objects; they were not copied into front matter.
- `rbki-any-block-gapless-error` describes a real matrix in its source docstring, but the readable statement leaves the field of `\\mathbf{A}` unspecified. The pinned source is `NLAlib/LowRank/Gaussian/SmallBlock.lean`, docstring at line 1114 and theorem beginning at 1132. Clarify the intended field before editing.
- `rbki-gapless-error` and `rbki-gapped-error` omit the source's standard Gaussian law for `\\mathbf{X}` and the declaration's real-matrix domain. The pinned source declarations take `A : Matrix m n ℝ` and `hX : HasLaw X (gaussianMatrix n l) μ` (`BlockKrylovGapless.lean` around lines 682–685; `BlockKrylov.lean` around lines 437–441). These are mathematical conditions, so they were not inferred into the statements.
- `rbki-block-monotonicity` has no verified direct definition target for the RBKI procedure; no link was guessed. The multiplicity statement's explanation mentions the exact projection but no scope-compatible existing definition page was verified.
- No formulas, delimiter segmentation, assumptions, titles, bindings, IDs or metadata changed. No symbol-role registry additions proposed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed ID, front-matter, kind, binding, title and target-ID checks. It reports 80 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is in this batch. The two edited statements are not flagged.
- Preview/rendering was not run in this local source-only review.
## Authoritative inherited citation record audit

This audit resolves each entry through the pinned editor object’s `evidence.declaration` and the corresponding declaration `record.references`. It supersedes any earlier statement that treated an empty authored `object.references` array as proof of no inherited references. The pairs below are already attached through the declaration and were not duplicated in front matter.

| UUID | Linked declaration | Inherited key/locator pairs |
| --- | --- | --- |
| `188aac98-6bd6-511d-a625-99a6935d7b28` | `NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_one_add_sq_mul_le_of_hasLaw_gaussianMatrix` | `MeyerMuscoMusco2023`, Theorem 1; `MeyerMuscoMusco2023`, Theorem 11 |
| `0bd6d1ef-ab85-5de8-85b7-6872fc39dae0` | `NLAlib.singularValues_sub_rbki_le_of_range_le` | None in declaration record |
| `49c904f7-6031-57df-9638-f96650269510` | `NLAlib.integral_specNorm_sub_rbki_sq_le_mul_exp_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, Theorem 9.1 (RBKI) |
| `6cec8318-a6a3-5186-a4c8-1928457d0cc8` | `NLAlib.integral_specNorm_sub_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, Theorem 9.2 (RBKI) |
| `2715e07f-95d2-5b31-863a-8adcfb6d65d4` | `NLAlib.singularValues_le_singularValues_sub_rbki_of_singularValues_eq` | None in declaration record |
