# Luna research cohort 04 · part 3 (corrected coverage)

This report corrects the intended cohort04 part3 coverage to the five assigned UUIDs below. The historical `luna-research-04-part3.md` names a different set of entries and is not credited as coverage for this group. Baseline revisions and inherited citations were checked against `/tmp/nlalib-release-explorer/api/v1`; each linked definition was read before adding a link. This is an editorial proposal, not a mathematical or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `35e54249-105c-5da3-980b-30e3d93943b4` (`eckart-young-frobenius`) | `6d26550a6c00b09b47309cc0328ab26fc3f958b8f618eb87854a22f94194b3d4` | `proposed` |
| `d059f2c5-9a30-5050-9e0c-bfddc9d221d7` (`etgn`) | `6d89443305799b6b8880267f739f5fa2458b5c72a3886f874324c2dee5649c8b` | `proposed` |
| `07a22a07-cf1a-5eab-9c15-e691321845a2` (`generalized-nystrom-expected-error`) | `d6e2d61b90af4ec06c590c4746886700e29b8d4e30e0dd7a94c90ceef8b07b2f` | `proposed` |
| `5feae0f6-b290-5ff9-8c2e-4103573b92b7` (`girard-hutchinson-unbiased`) | `7d74f32595d04cadda1643080021032b3e8f2a65c0e1123541ce2a46702397b4` | `proposed` |
| `ab283d6b-fe5a-5ca9-bae6-317a3a172f42` (`gmres-optimality`) | `51e76389c4438528d0eab71078da00524ee4bb701a5fdf93ca15ab03c5c8097f` | `proposed` |

## Edits and definition links

- `eckart-young-frobenius`: linked the existing phrase “leading singular components” to the [singular-value-decomposition definition](/explore/statements/d5bca832-63a1-5043-ab6e-03b8402a2a55/), which directly defines retaining those components as a rank-at-most-$k$ truncation.
- `etgn`: braced the expectation font as `\mathbb{E}` and linked the existing term “early-truncated output” to the [`NLAlib.earlyTruncatedGeneralizedNystrom` definition](/explore/statements/cdd691bb-6aef-5d59-b7e9-615785a98d27/). The assigned theorem is explicitly for a real input; the target is the same mathematical output formulation.
- `generalized-nystrom-expected-error`: braced `\mathbb{R}` and `\mathbb{E}`; changed the Greek matrix sketches to `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}`; linked the existing phrase “best rank-at-most-$k$ approximation” to the SVD definition above. All dimensions, inequalities, norms, and display delimiters were retained.
- `girard-hutchinson-unbiased`: braced `\mathbb{E}` and linked the original phrase “isotropic probes” to the [isotropic-probes definition](/explore/statements/cb5e0fa7-3425-5848-83bd-fd73b4aa314e/), which defines the second-moment condition.
- `gmres-optimality`: linked the existing phrase “GMRES iterate” to the [GMRES definition](/explore/statements/7d1681b7-7670-532a-98d3-4e7886e4adcc/), which defines the iterate by the same residual minimization over the Krylov search space.

No IDs, result bindings, theorem kinds, titles, assumptions, formulas, or delimiter segmentation were changed. No text was added to create link targets.

## Actual inherited citations

The authored `object.references` arrays are empty. Citations below were read from each linked declaration record's `record.references`; no duplicate front-matter references were added.

- `NLAlib.frobNorm_sub_truncatedSVD_le_of_rank_le` — `HornJohnson2013`, §7.4.9.
- `NLAlib.integral_frobNorm_sub_earlyTruncatedGeneralizedNystrom_sq_le_one_add_mul_of_hasLaw_gaussianMatrix` — `TroppYurtseverUdellCevher2017`, §7.3.1, (7.3).
- `NLAlib.integral_frobNorm_sub_generalizedNystrom_sq_le_of_hasLaw_gaussianMatrix` — `TroppYurtseverUdellCevher2017`, Theorem 4.3.
- `NLAlib.integral_girardHutchinson` — `Epperly2023`, Unbiasedness.
- `NLAlib.isMinOn_gmresIterate` — `SaadSchultz1986`, §3.1; `Saad2003`, §6.5.1 and Proposition 5.3.

## Duplicate and unresolved review notes

`eckart-young-frobenius.md` has a separate authored entry, `eckart-young-frobenius-044d6c37.md` (UUID `6b9702ff-31b4-53a0-a649-f5445c79ee30`), with the same `result:eckart-young-frobenius` binding and the same Frobenius comparison. The entries have distinct UUIDs and wording. This batch preserves both identities and does not merge them. Their possible alias relationship should be reviewed separately.

No unresolved mathematical ambiguity was established in the five assigned statements. The changes are limited to role-appropriate notation and links on existing terms. The global notation registry and all nonassigned source entries were left untouched in this corrected-coverage commit.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. This does not establish theorem correctness or validate the formal/readable correspondence. No browser-rendered preview was available.
