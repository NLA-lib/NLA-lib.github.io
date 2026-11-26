# Luna matrix definitions cohort 06, part 3

This report covers only the final five assigned definitions. Baseline revisions and editor metadata were checked in the pinned release Explorer objects. All five objects are authored definitions with empty `object.references`, `reference_links: null`, and no linked declarations; consequently none has inherited declaration citations.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `a2eae5c1-9838-5481-bd1e-23c8c937297c` | `explore/content/statements/nystr-m-subspace-iteration-a2eae5c1.md` | `173ce92c0efd7336816f922b2f5386d0791dc4501540b343a21160e4138a8c98` | `proposed` |
| `7ba672b5-064e-59ab-a9bf-4618f6a93878` | `explore/content/statements/pivoted-cholesky-7ba672b5.md` | `6ede922b2f6ee9779392079e84874e2c7fbc547776ce1eb7e38411ab127d497f` | `proposed` |
| `9eae1af0-188b-5813-b0b9-54626065edae` | `explore/content/statements/power-iteration-9eae1af0.md` | `69a4e3ac3ee34252dedb6a37fb74e0bb0fd332c416621f73a43ce9b9bcb00ec2` | `already-consistent` |
| `b414dcaf-295f-5cf2-b402-53aed405eae8` | `explore/content/statements/probe-spectral-estimation-b414dcaf.md` | `657693378b665737a5f4c17d2682325565af6d3b8ff9f6f7715f7163f7609a78` | `proposed` |
| `76e7063b-9c06-5517-9953-ba9b8e5adf49` | `explore/content/statements/randomized-kaczmarz-76e7063b.md` | `6cd15584477a9e1dc81b04a27873c846dc9dc05f0f0c387acf91de680ed6c7d6` | `already-consistent` |

## Edits and direct definition links

- **Nyström subspace iteration**: corrected the Greek matrix sketch symbol from `\mathbf\Omega` to `\boldsymbol{\Omega}` throughout. Linked the existing “Nyström approximation” term to UUID `254f7f6f-1199-596d-9347-4d32f1eab873` and “block Krylov variant” to UUID `8647f4e3-cefb-5ae0-9fac-51da15589631`. Both definitions match the stated PSD Nyström methods and support real or complex scalar fields. The linked Nyström approximation definition outside this batch still writes its Greek matrix as `\mathbf\Omega`; it is flagged here for a future assigned cleanup, not edited.
- **Pivoted Cholesky**: linked the existing phrase “unpivoted positive-definite Cholesky” to Cholesky factorization, UUID `d00946c1-7d12-50e4-a6da-635456a9fca7`. That target directly defines the unpivoted factorization for Hermitian positive-definite matrices. The distinction from the semidefinite rank-revealing pivoted construction is unchanged.
- **Power iteration**: already consistent. The Rayleigh-quotient term has no direct matching definition target in the assigned scope; no related target was substituted.
- **Probe spectral estimation**: linked “Hermitian” to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`; “isotropic probes” to UUID `cb5e0fa7-3425-5848-83bd-fd73b4aa314e`; and “Lanczos quadrature” to UUID `6d8b12f4-2783-5f4b-8c76-53d3c62f914f`. These directly define the named concepts and have no conflicting real-only restriction. No normalization or expectation statement changed.
- **Randomized Kaczmarz**: already consistent. It remains explicitly real-valued, with the row sampling, projection update, zero-row case and guarantee distinction unchanged. No direct definition target for its affine row projection was identified.

## Citation associations

All five assigned entries are authored definitions with no Lean declaration evidence, no inline citation strings, and no inherited declaration references. No citations were moved or added. No citation metadata was copied from linked or neighboring definitions.

## Validation and limitations

Verified the exact target definition sources and UUIDs, including their field/domain scopes. The Nyström approximation target outside the assigned paths needs future notation cleanup (`\mathbf\Omega` is Greek matrix notation); that file was not changed. No formulas, hypotheses, IDs, titles, or metadata changed. The Nyström source changes only matrix-font notation; inline/display math segmentation is unchanged.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.
