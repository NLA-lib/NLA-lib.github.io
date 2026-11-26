# Luna research cohort 06 · part 3

Baseline revisions and declaration reference associations were checked against `/tmp/nlalib-release-explorer/api/v1`; linked declarations were located in the pinned Lean source. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `09cd1af3-5651-547a-a481-b16bf9a1dcba` (`nlalib-integral-frobnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix`) | `a614ee170f2273fd723cbfd85c0e1b383c8e3e1b77abf112440975c97f7abd3f` | `needs-mathematical-review` |
| `1e71ef0b-3edf-5d7b-9a7b-f202eb006a97` (`nlalib-integral-specnorm-sub-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix`) | `4603b097959aec11248845a4bd55f20c422c6b58ebe89f8b143ec7c1ae759747` | `needs-mathematical-review` |
| `8f2f113d-fe93-5cfc-8e86-00d35dd428ff` (`nlalib-integral-specnorm-sub-rsvd-aeval-sq-le-of-haslaw-gaussianmatrix`) | `536af4fc8d7977a9c624c6326a08e787c0bd9eb5bb99f52cb89146cf27e8de30` | `needs-mathematical-review` |
| `c9146d75-6940-51e0-b74c-ae8dc5904fac` (`nlalib-integral-specnorm-sub-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix`) | `955573da203a3c00bab40b382448ad2b7b39a123b5c4c3ba561ae0709febc40b` | `needs-mathematical-review` |
| `ab58d6c1-feba-55f1-928f-db09057451b9` (`nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix`) | `55d7ca374db5dafeef53edabd017b9a54d89c07a6dfdc07d38cb8624f893e65b` | `proposed` |

## Edits and contextual issues

- Braced `\mathbb{E}` in all five expectation formulas. No formula, assumption, norm, constant, display segmentation, title, UUID, or binding changed.
- The first statement also says “Under the same hypotheses” without defining `\gamma` locally; its formula uses the positive gap ratio. The declaration source encodes this through `singularGapRatio`, but the readable statement depends on prior context.
- The RBKI gapless relative statement and the RSI gapless relative statement each end by calling themselves alternatives to “the preceding one.” The standalone entries do not identify that preceding result. The RBKI truncated gapless statement has no such cross-reference and was left with only the expectation font change.
- The polynomial-filter RSVD result says the deterministic bound, Frobenius form, and unitarily invariant norm form “are listed below,” but its standalone source body contains none of those items. Its label `a`/`c` condition and real-polynomial domain were left intact; the contextual claim was not reconstructed.
- The two RBKI gapless statements are related but distinct: one bounds the full RBKI output and the other its rank-`r` truncated output. Neither was merged.
- No safe direct concept definition was needed or verified on the original prose in these entries, so no links were added.

Actual inherited citation pairs from each linked declaration's `record.references` (all authored `object.references` arrays are empty). No citations were added or moved:

- `NLAlib.integral_frobNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, §9.1, remark after Theorem 9.2.
- `NLAlib.integral_specNorm_sub_rbki_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2.
- `NLAlib.integral_specNorm_sub_rsvd_aeval_sq_le_of_hasLaw_gaussianMatrix` — `TroppWebber2023`, Lemma 9.5.
- `NLAlib.integral_specNorm_sub_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2 (RSI).
- `NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix` — `MuscoMusco2015`, Theorem 10 (proof); `TroppWebber2023`, Theorem 9.2.

## Registry proposals

No role registry additions are proposed for this batch. The global notation registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. Inherited citations were checked in declaration records; no rendered browser preview was available.
