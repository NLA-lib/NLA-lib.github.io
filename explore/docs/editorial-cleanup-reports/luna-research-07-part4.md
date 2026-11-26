# Luna research cohort 07 · part 4

Baseline revisions and citation associations were checked against `/tmp/nlalib-release-explorer/api/v1`; the complex-Gaussian source declarations were inspected in the pinned Lean snapshot. This is an editorial proposal, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `f8e62433-bfdf-565e-bcc7-5fa20530c2d0` (`nlalib-measurereal-norm-mulvec-add-le-le-of-haslaw-complexgaussianvector`) | `855d00a9d837730e2669807e4ccda9dff3e3cc0fb5463b37e6fee9dddecc4d99` | `proposed` |
| `d12d207c-4b10-5d38-b3af-794f3ecfb298` (`nlalib-measurereal-not-exists-class-le-of-haslaw-complexgaussianmatrix`) | `f9106f9cba955b0a92bee1c83e71bd103d5ad96a4d70e7317add96f13f3c3c7b` | `proposed` |
| `d8fd5d15-a8e2-53c0-aaf5-f021e9b3cb9b` (`nlalib-measurereal-not-exists-iseigenvaluelisting-le-le-log-sq-of-haslaw-complexgaussianmatrix`) | `3da9548f7b619e23ea4f3d5b0ece8bddf0939322ded97beb38098c114c8876a2` | `proposed` |
| `33c3f20b-3401-544f-aaa4-a0644553f22e` (`nlalib-measurereal-not-exists-pseudoconditionnumber-le-le-log-sq-of-haslaw-complexgaussianmatrix`) | `76df2f6277e9de2323a124a936a580103c7a45de4fe0d58437d4b309111705f4` | `proposed` |
| `40802520-a357-5db5-9410-9d519ed8a063` (`nlalib-measurereal-singularvalues-add-smul-le-le-exp-one-mul-of-haslaw-complexgaussianmatrix`) | `d77f305bde8197d0cf49af189f113fca62bc482bc0f451b798dd4fbb890dd971` | `proposed` |

## Edits and links

- Braced `\mathbb{P}` in all five probability statements. Vector and matrix roles remain explicit: `\mathbf{g}`, `\mathbf{c}`, `\mathbf{P}`, `\mathbf{M}`, `\mathbf{G}`, `\mathbf{V}` and `\mathbf{d}` are vectors or matrices as written; scalar eigenvalues, thresholds, and scale parameters remain unbolded.
- In the combined diagonalization-class bound, linked the existing “gap tail” and “condition tail” phrases to the [gap-tail result](/explore/statements/d8fd5d15-a8e2-53c0-aaf5-f021e9b3cb9b/) and the [condition-tail result](/explore/statements/33c3f20b-3401-544f-aaa4-a0644553f22e/). Both source results concern the same complex Ginibre perturbation model and match the two component tails named in the class statement.
- The gap, condition-number, and combined-class results are related bounds with distinct conclusions and formulas. Their identities and citations remain separate; no entries were merged.
- No formulas, conditions, constants, titles, IDs, result bindings, or delimiter segmentation were changed. No prose was added to introduce links.

Actual inherited citations were checked through each linked declaration's `record.references`; the authored `object.references` fields are empty. No citations were added to front matter.

- `NLAlib.measureReal_norm_mulVec_add_le_le_of_hasLaw_complexGaussianVector` — none.
- `NLAlib.measureReal_not_exists_class_le_of_hasLaw_complexGaussianMatrix` — `BanksGarzaVargasSrivastava2025`, Lemma 6.5.
- `NLAlib.measureReal_not_exists_isEigenvalueListing_le_le_log_sq_of_hasLaw_complexGaussianMatrix` — `BanksGarzaVargasSrivastava2025`, Lemma B.1.
- `NLAlib.measureReal_not_exists_pseudoConditionNumber_le_le_log_sq_of_hasLaw_complexGaussianMatrix` — `BanksKulkarniMukherjeeSrivastava2021`, Theorem 1.5.
- `NLAlib.measureReal_singularValues_add_smul_le_le_exp_one_mul_of_hasLaw_complexGaussianMatrix` — `BanksKulkarniMukherjeeSrivastava2021`, Lemma 3.3; `SankarSpielmanTeng2006`, proof of Theorem 3.3.

## Registry proposals

No registry additions are proposed. Matrix and vector roles follow the current notation guide; the global registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish mathematical correctness or formal/readable equivalence. The two linked component results and citation records were inspected; no rendered browser preview was available.
