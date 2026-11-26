# Coordinator review of Luna pilot

Current publication status: GitHub PR #24 merged checkpoint `b2bd09d` into main
at `8ba81cac`. Later batches remain on this review branch. Earlier sections below
record the status when each checkpoint was reviewed, not current publication
status. `reviewed-inventory.csv` marks whether each current source version and its
inspection record are present in the observed main revision.

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

## Cohort 03 checkpoint

The reviewed inventory now contains 72 distinct UUIDs: 43 proposed source changes
and 29 inspected entries without a retained edit. Nine bounded five-file batches
cover rounding, Krylov and randomized definitions/results. Their original reports
are retained. The coordinator additionally preserved the initial capitalization of
Standard Gaussian, bolded the Ritz vector component consistently, narrowed an
embedding link label, and linked truncated-SVD notation to its precise definition.

A source audit validates unchanged front matter (apart from explicit references),
kinds, formal bindings, titles and all definition-target IDs. Original mathematical
fragments are unchanged modulo font/bracing conventions for existing entries,
except the previously reviewed singular-value clarification. The three generated
CG files have separately reviewed layout/citation relocations. These checks are
editorial safeguards and do not certify theorem truth or complete missing hypotheses.
All cleanup proposals remain off main. See `reviewed-inventory.csv` for UUID-level
coverage; the remaining research inventory and possible aliases are still pending.

## Cohorts 04 and definitions 05

The coordinator retained the assigned definitions and research-theorem typography
and direct concept links after reading each diff. The research04 part3 source
changes were outside that agent's assignment and duplicated the separately assigned
definitions04 work. Its report reviewed the wrong five files and receives no additional coverage credit;
the intended files have been reassigned. Its source edits were
not cherry-picked. The broad rank-k-subspace link was rejected in favor of the
precise singular-values link from the definition batch. The original scalar
`r_{cc}` was restored: a formatting pass does not authorize renaming it to R.

Fourteen additional named results were materialized with stable original UUIDs and
bindings. The citation-only Arnoldi-Hessenberg record is inspected but not
materialized as an empty theorem. A Gram-defect link was moved to the actual
rounded-extension phrase defined by its target. Unconfirmed citations, field-scope
questions and incomplete standalone hypotheses remain explicitly flagged in the
generated-batch reports; no mathematical certification is implied.

## Research-facing scope checkpoint

The corrected research04 part3 report now covers its intended files. Reviewed
coverage is 162 distinct UUIDs, including 96 retained source proposals and one
citation-only record left unmaterialized. The remaining entries are explicitly
pending in `research-scope-inventory.csv`; raw Lean helper descriptions are outside
this pass. Definition batches04–07 are reviewed, and research05 parts1–2 are
reviewed. All authored-definition assignments are now complete.

The Markov statement uses the conventional probability font `\mathbb{P}` instead
of `\Pr`, alongside braced expectation notation. This is a reviewed notation
alias; its event and bound are unchanged. The source audit's other mathematical-
fragment exceptions are the initial generated-CG citation/layout changes and
the previously recorded singular-value clarification.

Validation at this checkpoint: 139 Explorer tests passed (8 optional skips),
2,430 equations rendered by KaTeX without errors, and the full pinned library
build completed. Three representative generated/shared entries were checked in
Chromium with math, styled discussion and direct definition previews. Later
source batches remain proposals until individually reviewed and recorded.

## Subsequent bounded-batch review

Generated matrix08 parts1–2 and research06 part1 have been inspected. Source math
and identities pass the comparison audit. Citation removal in physical-energy
convergence retains the exact-model qualification; the coordinator repaired its
sentence transition and normalized bracing/capitalization in physical-energy
quadrature. Generated-title escape normalization retains the same parsed title.
A separate 68-row possible-authored-alias queue records identity questions without
merging pages; two additional named-result aliases are recorded in
`root-generated-aliases.md`. The full pending/reviewed scope remains explicit.

## Citation and parser review through matrix08 part7

Research06 and research07 part1, generated05, and matrix08 parts1–7 are now
reviewed. Coverage is 239 UUIDs with 162 retained source proposals. The source
audit still reports only the five explicitly reviewed exceptions described above.
The coordinator corrected citation sentence transitions, kept the difference
between the cited qualitative tiny-interval formulation and the explicit physical-
energy bounds, and capitalized initial prose without changing math.

A malformed closing directive in matrix08 part3 was corrected before build
validation. The agent playbook now requires statement-source parsing and a staged
whitespace check as well as KaTeX, and emphasizes preserving source qualifications
after citation removal. Agent reports retain uncertainty about citation locators
and missing standalone hypotheses; inspected is not mathematically certified.

## Mid-run evidence checkpoint

Coverage: 384 of 778 research-facing UUIDs, with 278 retained source proposals.
The remaining scope is explicit in the inventory. The citation audit checks all
known bibliography keys, retains 197 removed key/locator associations exactly,
and reports no missing association. `source-audit.json` contains the unchanged
identity/binding and formula comparison evidence, with only the five previously
reviewed layout/notation exceptions. These audits compare source associations and
presentation, not the truth of the claims or the adequacy of the cited proofs.

The coordinator held matrix08 part17 until its degree bound and eigenvector-weight
clause were restored exactly from the pinned template. The current source passes
the audit. Report07 part8 was corrected to its actual assigned UUIDs; its out-of-
order spectral-bisection font edit is recorded separately from coverage. All agents
now compare staged expressions and parsed titles to the pinned baseline and
validate report UUIDs and changed paths against the supplied manifest.

## Current-data compatibility checkpoint

The initial editorial scope remains the pinned 778 research-facing entries. All
242 authored entries have now been inspected; overall coverage is 572 UUIDs.
There are 420 retained source proposals and 376 removed key/locator associations
confirmed against the pinned records, with no missing association found.

Main concurrently merged PR #25, adding six BCW statements. They are preserved
byte for byte and separately documented in `concurrent-main-additions.md`. Their
new declarations require the newer rolling library data. The complete build
succeeds with data/source revision `e207eefa3d0c91354b42affc0bfcd982a3b05807`
(19,711 library records, 17,283 declarations, 611 result groups); comparison of
cleanup edits remains pinned to `83c32cc` rather than treating newer mathematics
as editorial changes. The refreshed loopback preview passes representative
Chromium math, discussion-style and definition-preview checks.

The coordinator retained the original factor provenance in the Higham/Carson
inner-product bounds, restored precise nonnumeric clause attribution, and kept
unverified sharpness locators as unresolved rather than asserting that source
checks were completed. Original reports with citation-record omissions are
superseded by their appended authoritative declaration-reference tables.

## Completed editorial scope

All 778 pinned research-facing UUIDs are inspected; no scope entry remains
pending. The final outcome table is in README.md, and each record retains its
original revision token. 606 citation key/locator associations are preserved in
both the original records and current build metadata. The six concurrent BCW
statements remain unchanged and outside this pinned count. Root-level source
polish preserves original source ownership and qualifications rather than
introducing stronger claims. The follow-up list separates missing formulations,
source-locator verification, aliases and field/domain questions.
