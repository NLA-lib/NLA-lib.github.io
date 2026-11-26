# Luna research cohort 07 · part 5

Baseline revisions and inherited citation associations were checked against `/tmp/nlalib-release-explorer/api/v1`; linked declarations were inspected in the pinned Lean snapshot. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `2a591816-ee5e-5295-99ac-adfaafad0e31` (`nlalib-measurereal-singularvalues-add-smul-le-le-pow-four-of-haslaw-complexgaussianmatrix`) | `ca14ba5a8177516fabddd1d9d741a76e5e1744e0d36027d4fdaf0a6d572dd2b6` | `proposed` |
| `a5d91c5d-df40-55e9-ac3f-92bb1c0dbf85` (`nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianmatrix`) | `72b1efb84935d82ca4e114bae7286ea296674b61bbf5d97066ac39102768b439` | `proposed` |
| `b6e3068d-bde4-5d5c-aafe-f3918ea961e1` (`nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianvector`) | `7c58e2023469be371c95aa4efa0c2ae6317a65832811b71fc52a47b7fb209369` | `proposed` |
| `830039af-0d41-5fa5-886e-01b1c11815c0` (`nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianmatrix`) | `4cec2cb245dae7d75ea7c10ef575570693c4bc44245975ee84d6d9e6ad1bbfef` | `proposed` |
| `b89d095b-73c0-59e2-a3f9-173e6d19b29c` (`nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianvector`) | `85e010f15bc5abd34c03638872a14573042aff9cffc0e93c190feb582ffcc599` | `proposed` |

## Edits and links

- Braced `\mathbb{P}` in all five probability statements and `\mathbb{R}` in the two real-vector statements. No vector, matrix, or scalar roles changed.
- In the any-block RBKI tail statement, linked the existing “single-vector bound” phrase to the [single-start-vector RBKI result](/explore/statements/b6e3068d-bde4-5d5c-aafe-f3918ea961e1/). The target has the same tail expression for the single-column start block, so this is a direct companion-result link.
- The single-vector and any-block results are related but distinct cases; likewise, the truncated and untruncated RBKI results concern different outputs. No IDs or formulas were merged.
- The two vector statements mention additional forms “listed under Further results.” Those phrases refer to groups of companion entries rather than one unambiguous target in this assigned batch, so no link was added. Their original wording remains unchanged.
- No formulas, conditions, constants, titles, IDs, bindings, or display segmentation changed. No explanatory prose was added.

Actual inherited citations from declaration record `record.references`; no references were added to front matter. The authored `object.references` fields are empty.

- `NLAlib.measureReal_singularValues_add_smul_le_le_pow_four_of_hasLaw_complexGaussianMatrix` — none.
- `NLAlib.measureReal_specNorm_sub_rbki_sq_gt_le_of_hasLaw_gaussianMatrix` — `MeyerMuscoMusco2023`, Theorem 6.
- `NLAlib.measureReal_specNorm_sub_rbki_sq_gt_le_of_hasLaw_gaussianVector` — `MeyerMuscoMusco2023`, Theorem 6.
- `NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianMatrix` — `MeyerMuscoMusco2023`, Theorem 6.
- `NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianVector` — `MeyerMuscoMusco2023`, Theorem 6.

## Registry proposals

No registry additions are proposed. The global registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. The related vector theorem and inherited citation records were inspected; no rendered browser preview was available.
