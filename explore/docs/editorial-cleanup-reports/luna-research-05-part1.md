# Luna research cohort 05 · part 1

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
formal evidence were checked against `/tmp/nlalib-release-explorer/api/v1/editor/objects/`;
inherited references were checked through the linked declaration records. No proposal
was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `e14bcce7-62ce-54e6-998e-40ef966c42bb` (`hutchpp-unbiased`) | `2944219c8cc3d22513a22e5d83afa9470edee89314911a72e229c737f8fc85e4` | `explore/content/statements/hutchpp-unbiased.md` | `proposed` |
| `e1a72f9d-aab8-55c4-b50b-40b1279609fc` (`iterative-refinement-forward-error`) | `5e79479c7bb2fdee21fc58f4e9f11ec1f107ef7b525b5ce4014df0c2d9fac0aa` | `explore/content/statements/iterative-refinement-forward-error.md` | `proposed`; run assumptions are implicit |
| `ba9a80b1-12cc-5be5-b98c-0834104cd8f5` (`lanczos-fa-uniform-bound`) | `3cc06fa7570ee05d09486a0d81fbb0e56810e7c70b4c09b98271679c28dc53f6` | `explore/content/statements/lanczos-fa-uniform-bound.md` | `proposed` |
| `0b4b1b6d-b0a4-52dc-90e9-53494f3cbdf4` (`lanczos-tridiagonal`) | `ecff62da45028447b2de5e70683feca94e99c4182815f7721e45ba2cd4fe4263` | `explore/content/statements/lanczos-tridiagonal.md` | `proposed` |
| `6cf5cbfe-3caa-5917-b1b9-e00daab48ffa` (`markov-inequality`) | `4881b8c952de96ac3b03b3947f8a5b33878cce59cce1e660127216a8d4cee65c` | `explore/content/statements/markov-inequality.md` | `proposed` |

## Changes and inherited references

- `hutchpp-unbiased`: braced `\mathbb{E}`. No definition link was added because the
  only occurrence of `\mathsf{hutch++}` is inside display math; no prose term names
  the estimator separately.
- `iterative-refinement-forward-error`: linked the existing word “run” to the
  `RefinementRun` definition at `/explore/statements/c07e970e-5e57-5ffc-95c4-0a61ec4b2f4d/`.
- `lanczos-fa-uniform-bound`: linked “Lanczos steps” to the exact Lanczos process
  definition at `/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/`, whose
  Hermitian-matrix scope matches the statement.
- `lanczos-tridiagonal`: linked “graded Krylov basis” to the same process definition,
  which defines the graded orthonormal basis for Hermitian matrices.
- `markov-inequality`: changed `\Pr` to the braced probability font `\mathbb{P}`
  and braced `\mathbb{E}`. The event, variable, threshold and inequality are unchanged.
- Actual inherited citation pairs from linked declaration records:
  `hutchpp-unbiased` — `MeyerMuscoMuscoWoodruff2021`, Theorem 10 and Lemma 14;
  `EpperlyTroppWebber2024`, Proposition 5.2.
  `iterative-refinement-forward-error` — `CarsonHigham2018`, Corollary 3.3.
  `lanczos-fa-uniform-bound` — `ChenPersson2026`, (2); `Saad1992`, §3.
  `lanczos-tridiagonal` — `Saad2003`, §6.6.
  `markov-inequality` — `Vershynin2018`, Proposition 1.2.4.
  `reference_links.inherited` is absent in this snapshot; linked declaration records
  were inspected directly. No citation was duplicated or moved inline.
- All IDs, UUIDs, theorem kinds, result bindings, formulas, hypotheses and metadata
  were retained.

## Symbol-role registry proposals

No registry changes were made. For a future role review, the matrix/vector roles are:

- `hutchpp-unbiased.md`: matrix `A`.
- `iterative-refinement-forward-error.md`: matrix `A`; vectors `x`, `b`.
- `lanczos-fa-uniform-bound.md`: matrix `A`; vector `b`.
- `lanczos-tridiagonal.md`: matrices `A`, `Q`.
- `markov-inequality.md`: no matrix/vector roles; `X` is a scalar random variable.

## Unresolved issues

- `iterative-refinement-forward-error.md:8–13` says “a run” without repeating the
  `RefinementRun` assumptions. The linked definition requires invertible `A` and
  describes the residual, correction and update conditions. Confirm that the direct
  definition link is sufficient for the theorem's intended scope; do not add those
  assumptions without review.
- No duplicate, citation mismatch, or missing proof URL was found in this batch.
  All five linked declarations report `admission_reported: false`.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after
editing. The notation check validates math parsing and registered notation roles,
not the mathematical claims. Both definition links were checked against their
Markdown definitions and formal domains. No rendered browser or repeated-placement
preview was available.
