# Luna research cohort 06 · part 1

Baseline revisions and declaration references were checked against `/tmp/nlalib-release-explorer/api/v1`; the assigned declarations were also checked in the pinned Lean source. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `0ed7fc6a-e23a-5cc1-a1d8-2055f3edf2a8` (`nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-of-haslaw-gaussianmatrix`) | `c2242bc9c932b982b010e0cd19120d7dadaec49538415f142ab08ce326c8a21b` | `proposed` |
| `57ec5e8f-9d28-5793-b43a-fa7abfa993c3` (`nlalib-exists-iseigenvaluelisting-norm-sub-le-of-class`) | `18afee77e6cf5647684eca2faaca836f6f255b1f9095ac00c63061b10ebf5e51` | `proposed` |
| `f83d1bc1-e6b7-54ed-a19a-e944c02f33c6` (`nlalib-exists-iseigenvaluelisting-norm-sub-le-rpow`) | `62925de50114c90e0bb47dd9c39739b3c6515faad1d0bcb1ef9f7ff8ba9a5c42` | `already-consistent` |
| `2d946bb4-7f28-5df4-931c-7d4ce649fa18` (`nlalib-exists-mem-singularvalues-le-of-not-exists-iseigenvaluelisting`) | `088b990cd57f74249e9940de9a8dee0e41456ae6c4c24ad0f853dd19100e243e` | `already-consistent` |
| `0510eeec-6054-5ba1-8745-0037739c3d9a` (`nlalib-floatmachine-isaccurate-measurereal-not-isapproxdiagonalization-eigh-bisectiondepth-le-of-logb-le-of-haslaw-eighsamplelaw`) | `2bca4302d76e7f693d5cf8a3d73f94e30e40ade560e5f0edcf623b1a13cba644` | `proposed` |

## Edits and links

- The RSI sufficient-step result had an unbraced `\mathbb E`; changed only to `\mathbb{E}` in its existing display formula.
- In the diagonalizable-matrix perturbation result, braced the Greek listing font as `\boldsymbol{\lambda}` and linked the existing “Ostrowski–Elsner matching” phrase to the [Ostrowski–Elsner matching theorem](/explore/statements/f83d1bc1-e6b7-54ed-a19a-e944c02f33c6/). Both declarations concern complex matrices of order `n+1`; the linked result is the exact matching step named in the prose. No direct Bauer–Fike target was found, so that term remains unlinked.
- The standalone Ostrowski–Elsner result and the singular-value net statement already had role-appropriate notation and no linkable exact definition term; both were left unchanged.
- In the precision theorem, braced the field font `\mathbb{C}`. Scalar `\Omega` is a range parameter, so it remains unbolded. `\mathbf{U}` and `\mathbf{I}` are matrices, while `\mathbf{d}` is the eigenvalue list.
- No formulas, hypotheses, conclusions, titles, IDs, bindings, or display segmentation changed. No new explanatory prose was added.

## Actual inherited references

Each `object.references` array is empty. These pairs were checked in the linked declaration record's `record.references`; no references were added to front matter.

- `NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2 (RSI).
- `NLAlib.exists_isEigenvalueListing_norm_sub_le_of_class` — `BanksGarzaVargasSrivastava2025`, Corollary 1.3.
- `NLAlib.exists_isEigenvalueListing_norm_sub_le_rpow` — `BanksGarzaVargasSrivastava2025`, Lemma 1.2.
- `NLAlib.exists_mem_singularValues_le_of_not_exists_isEigenvalueListing` — none.
- `NLAlib.FloatMachine.IsAccurate.measureReal_not_isApproxDiagonalization_eigh_bisectionDepth_le_of_logb_le_of_hasLaw_eighSampleLaw` — `Shah2024`, Theorem 4.2.

## Unresolved issues

No mathematical ambiguity was established in the assigned statements. The diagonalizable-matrix theorem's “eigenvalues separated by $g$” condition is backed by the Lean source's pairwise condition `g ≤ ‖d i - d j‖` for distinct indices. The precision statement's sample-bit example and all arithmetic conditions were left intact. No role registry changes are proposed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish mathematical correctness or formal/readable equivalence. The Ostrowski–Elsner theorem target and inherited citation records were inspected; no rendered browser preview was available.
## Authoritative inherited citation record audit

This audit resolves each entry through the pinned editor object’s `evidence.declaration` and the corresponding declaration `record.references`. It supersedes any earlier statement that treated an empty authored `object.references` array as proof of no inherited references. The pairs below are already attached through the declaration and were not duplicated in front matter.

| UUID | Linked declaration | Inherited key/locator pairs |
| --- | --- | --- |
| `0ed7fc6a-e23a-5cc1-a1d8-2055f3edf2a8` | `NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_of_hasLaw_gaussianMatrix` | `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2 (RSI) |
| `57ec5e8f-9d28-5793-b43a-fa7abfa993c3` | `NLAlib.exists_isEigenvalueListing_norm_sub_le_of_class` | `BanksGarzaVargasSrivastava2025`, Corollary 1.3 |
| `f83d1bc1-e6b7-54ed-a19a-e944c02f33c6` | `NLAlib.exists_isEigenvalueListing_norm_sub_le_rpow` | `BanksGarzaVargasSrivastava2025`, Lemma 1.2 |
| `2d946bb4-7f28-5df4-931c-7d4ce649fa18` | `NLAlib.exists_mem_singularValues_le_of_not_exists_isEigenvalueListing` | None in declaration record |
| `0510eeec-6054-5ba1-8745-0037739c3d9a` | `NLAlib.FloatMachine.IsAccurate.measureReal_not_isApproxDiagonalization_eigh_bisectionDepth_le_of_logb_le_of_hasLaw_eighSampleLaw` | `Shah2024`, Theorem 4.2 |
