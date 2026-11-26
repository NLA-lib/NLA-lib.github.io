# Luna research cohort 07 · part 6

Baseline revisions and inherited citation records were checked against `/tmp/nlalib-release-explorer/api/v1`; the MGS definition was read from its shared Markdown source. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `75eae202-4e88-5a08-b9ed-7af0208f76ae` (`nlalib-mgs-factor-peak-le`) | `af8e948eaa596450541964904cfa59e316d90595ef1b626b19853c53b9be8dfa` | `already-consistent` |
| `60522b5b-99ce-5e10-9702-ddaea0dbe79a` (`nlalib-mgs-factorroutine-meets`) | `d6bb33c641418231c33a1a56fcf6cd3a353467b2b89d50d276ee083c7cf26644` | `proposed` |
| `ca9a7176-8d3f-5ea4-bb63-fc9416576e9b` (`nlalib-norm-inv-mulvec-sub-le-of-add-mulvec-eq`) | `9731f262ab64bc24dd257ede94d3ec35784f925eebf641ac9321d6cf397e0a99` | `already-consistent` |
| `81417ef6-1efe-5265-9d7a-7b1abb433e5b` (`nlalib-ofreal-sq-div-card-le-liminf-measure-inter-ball-of-not-exists`) | `7bf82cc51780fcb0980c8bf5eab71b41fd2a8bfed57ad1ad8c078971fbc49ddf` | `already-consistent` |
| `bb84de14-c932-5564-b420-591262284fdd` (`nlalib-ofreal-sum-sq-le-liminf-measure-inter-ball-of-mul-eq-mul-diagonal`) | `1a257b4d151abaeacf5cda4d5eaf87473e95171a6d6baa22f375346fbe65eb53` | `already-consistent` |

## Edits, references, and related results

- `nlalib-mgs-factorroutine-meets`: linked the existing inline identifier `gramSchmidtQ` to the [Gram–Schmidt orthogonalization definition](/explore/statements/47fa9a99-bf7f-54d6-ad4e-a307c2efa85a/). The target directly defines the mathematical column process and explicitly distinguishes classical from modified Gram–Schmidt.
- The other four entries already use appropriate matrix/scalar roles and transpose conventions; no notation edits were needed. No direct definition target was found for the MGS scratch bound, perturbation estimate, or pseudospectral area terms.
- The two pseudospectral area statements are related but distinct: one lower-bounds area from failure of a conditioned diagonalization, while the other upper-bounds a sum of eigenvalue condition numbers by the area limit. They have separate declarations and identities; no merge was made.
- No formula, hypothesis, title, ID, binding, or delimiter segmentation changed. No citations were moved or added.

Actual inherited citation pairs from declaration record `record.references` (authored `object.references` is empty for every entry):

- `NLAlib.MGS.factor_peak_le` — none.
- `NLAlib.MGS.factorRoutine_meets` — none.
- `NLAlib.norm_inv_mulVec_sub_le_of_add_mulVec_eq` — `CarsonHigham2018`, (2.3).
- `NLAlib.ofReal_sq_div_card_le_liminf_measure_inter_ball_of_not_exists` — `BanksKulkarniMukherjeeSrivastava2021`, Lemmas 3.1 and 3.2.
- `NLAlib.ofReal_sum_sq_le_liminf_measure_inter_ball_of_mul_eq_mul_diagonal` — `BanksKulkarniMukherjeeSrivastava2021`, Lemma 3.2.

## Registry proposals

No symbol-role additions are proposed. The global notation registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. The MGS target and inherited citation records were inspected; no rendered browser preview was available.
