# Luna research cohort 07 · part 1

Baseline revisions and inherited citation records were checked against `/tmp/nlalib-release-explorer/api/v1`; source declarations and the linked block Golub–Kahan definition were inspected in the pinned snapshot. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `61e06e3d-bf47-552c-9e75-a9af204ad122` (`nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `470d43200742f7bf59298091d09d52f2b52e0d9694b2bbbd4b48ca6f7fb1fabd` | `proposed` |
| `8e47438a-9c8e-5414-ab32-1d0cdeb3e198` (`nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix`) | `e0d4b5daa721e76a80fc67a6f7f6785c08ee53eed78eeb75829caa16d896d902` | `proposed` |
| `ce90654e-db13-5ef8-bd4d-3c665dd98c60` (`nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `f3d6d77d2cb021724805a4719cb4cb5ab9c4b4a3f9d10a0c1347981210166bea` | `proposed` |
| `07503cd9-ef53-5b6f-94ec-3b3203ebf50b` (`nlalib-isblockgolubkahan-conjtranspose-mul-left-eq`) | `1de1dca0c949d105cc0655be7872ef58881341c5781d0829ff8dcdaf0d394286` | `proposed` |
| `e16ffb73-7768-5557-9cc1-029af7b0a416` (`nlalib-isblockgolubkahan-gramdefect-right-eq-zero`) | `cd20b4c1acb08e72522954d664fb2d7541574a4511208b011e17f94c8fa471bf` | `proposed` |

## Edits and links

- Braced `\mathbb{E}` in the three expected-error formulas. Their scalar singular values and gap ratio remain unbolded; matrix symbols retain bold font.
- In both block Golub–Kahan identities, linked the existing phrase “exact run” to the [Block Golub–Kahan process definition](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/). That definition describes an exact run as any output related to the input and explicitly covers real or complex scalars.
- The adjoint relation retains `\mathbf{A}^{\mathsf{H}}\mathbf{U}=\mathbf{V}\mathbf{S}`. The Gram identity retains `\mathbf{V}^{\mathsf{H}}\mathbf{V}=\operatorname{diag}(\mathbf{s})`; its `s_c` entries are scalar indicators. No formula or delimiter segmentation changed.
- The gapped RSI and RBKI bounds are distinct algorithm-specific results. No IDs or bindings were merged. No direct readable page for the companion left-basis orthonormality theorem was found, so no link was added for that final sentence.

Actual inherited citation pairs from each linked declaration's `record.references`; no references were added to front matter:

- `NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2; `Gu2015`, Theorem 3.4.
- `NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2 (RSI).
- `NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `NLAlib.IsBlockGolubKahan.conjTranspose_mul_left_eq` — none.
- `NLAlib.IsBlockGolubKahan.gramDefect_right_eq_zero` — none.

All authored `object.references` arrays are empty; citations shown are the actual inherited declaration associations.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish mathematical correctness or formal/readable equivalence. The exact-run target and inherited reference records were inspected; no rendered browser preview was available.
## Authoritative inherited citation record audit

This audit resolves each entry through the pinned editor object’s `evidence.declaration` and the corresponding declaration `record.references`. It supersedes any earlier statement that treated an empty authored `object.references` array as proof of no inherited references. The pairs below are already attached through the declaration and were not duplicated in front matter.

| UUID | Linked declaration | Inherited key/locator pairs |
| --- | --- | --- |
| `61e06e3d-bf47-552c-9e75-a9af204ad122` | `NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, §9.1, remark after Theorem 9.2; `Gu2015`, Theorem 3.4 |
| `8e47438a-9c8e-5414-ab32-1d0cdeb3e198` | `NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix` | `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2 (RSI) |
| `ce90654e-db13-5ef8-bd4d-3c665dd98c60` | `NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, §9.1, remark after Theorem 9.2 |
| `07503cd9-ef53-5b6f-94ec-3b3203ebf50b` | `NLAlib.IsBlockGolubKahan.conjTranspose_mul_left_eq` | None in declaration record |
| `e16ffb73-7768-5557-9cc1-029af7b0a416` | `NLAlib.IsBlockGolubKahan.gramDefect_right_eq_zero` | None in declaration record |
