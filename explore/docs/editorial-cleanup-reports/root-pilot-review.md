# Coordinator review of Luna pilot

Release baseline: `a1d2898`. Pinned library extraction:
`83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Three Luna agents inspected
12 canonical shared statement files in separate worktrees. Their reports and
corrective commits are retained here; this coordinator review records the final
decisions rather than rewriting those histories. Nothing in this review branch
has been published to main.

## Accepted editorial changes

- CG polynomial and Chebyshev bounds: bold the existing matrix/vector symbols.
- CG finite termination: bold the existing solution/iterate vectors.
- Arnoldi relation: link the existing canonical Krylov-basis phrase to its generic
  Arnoldi-process definition, which shares the formal real/complex scope.
- Matrix norms: explicitly identify the existing sigma notation and link it to
  the dedicated singular-values definition rather than the less specific SVD page.
- Residuals: use `\boldsymbol{\Lambda}` for the Greek matrix symbol.
- Polynomial-on-a-matrix: link the Hermitian functional-calculus concept.

Seven source files have proposed changes. Five assigned files finish unchanged;
unchanged does not mean that all mathematical-scope questions are resolved.

## Corrections and deferred issues

- Removed duplicate authored references that were already inherited from linked
  declaration records. `object.references: []` is not evidence of absent citations.
  The snapshot exporter now exposes inherited and editorial associations separately,
  with a regression test. The playbook explicitly documents the fallback lookup for
  older snapshots.
- Removed real-only Krylov-definition links from the generic real/complex CG and
  Arnoldi/poly contexts. Their formal declarations use `RCLike` or their readable
  scope is unspecified. The target definition needs a separate scope review.
- Did not add Saad2003 equation (6.128) to the interval Chebyshev statement merely
  because it appears on a related condition-number declaration. Its existing
  primary-source citations remain intact; the extra locator is a review candidate.
- Kept the original scalar-polynomial explanatory wording and the positive-spectral-
  interval explanation instead of rewriting either to make room for a link.
- Missing standalone CG assumptions, polynomial domains, quadrature hypotheses and
  intended spectral-separation claims remain flagged in the agent reports. No
  missing hypotheses or proofs were invented.

The original pilot reports describe intermediate proposals; this coordinator
report and the final source diff define which edits were retained. The inventory
contains 16,448 canonical entries, 15,433 with readable prose. This pilot covers 12
entries, not the entire library. The remaining inventory is tracked separately by
UUID; blank prose and mathematical questions must retain explicit outcomes.

## Follow-on review checkpoint

The next rounding, spectral-definition, factorization and generated-CG batches
bring the inspected set to 27 UUIDs. Their individual reports retain baselines,
source associations and unresolved questions. The following additional changes
were retained for local review:

- Braced real-field/zero-vector notation and standard-rounding concept links.
- Correct Greek matrix fonts in SVD and Hermitian spectral/functional definitions.
- Direct singular-values/SVD and Hermitian-definition links on existing terms.
- A Gram–Schmidt definition link in QR; the indirect orthonormal-columns-to-QR
  link was removed because it was not an exact concept definition.
- Three generated CG entries were materialized with their original UUIDs and
  formal bindings, and inline source citations moved into the already inherited
  references or a verified Hestenes–Stiefel locator with its real-case qualifier.
  The Galerkin explanation retains its original `L=K` projection convention.

The user confirmed research-facing statements and named results as the first
scope. At the pinned release this gives 242 authored records and 536 additional
named-result candidates; 68 possible generated/authored aliases are a separate
review queue. Raw Lean helper descriptions are deferred. A further cohort of
45 authored entries is assigned in nine nonoverlapping five-file batches.
Nothing in the cleanup review branch has been merged into main.
