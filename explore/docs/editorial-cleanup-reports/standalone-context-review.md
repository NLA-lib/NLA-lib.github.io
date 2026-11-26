# Standalone statements and commentary follow-up

The earlier cleanup was merged through PR #26 and was visible on the public
Chebyshev convergence page. It preserved irrelevant implementation prose and
left the solution and CG iterate implicit. This follow-up corrects that example
and tightens the editorial workflow across all 778 research-facing scope entries.
Raw Lean helper descriptions remain outside this scope.

## Behavior and content

- The mathematical box contains the claim, its hypotheses and notation definitions.
- A terminal Markdown paragraph beginning `Note:` stays in the same editable source
  and revision history, but renders below the box on the individual page. List cards
  and definition previews show the claim. Library reference pages and local revision
  previews use the same separation. No new content schema or AWS deployment is needed.
- Irrelevant navigation/filler text is removed; substantive explanations, proof
  sketches and source comparisons are retained as commentary.
- The Chebyshev result states Hermitian A, Ax*=b, arbitrary x0, kth exact-arithmetic
  CG iterate, nonnegative iteration index and energy norm. CG has a semantic link
  to its algorithm page. Its displayed inequality is unchanged.
- Other source-explicit context fixes cover CG, GMRES, block Golub–Kahan, sketching,
  matrix approximation, matrix functions and polynomial bounds.

The [inventory](standalone-inventory.csv) has 778 unique UUIDs with a body-screen
outcome and independent edited/materialized flags. **204 source entries change**,
including **29 previously generated entries** now given Markdown with the same
identity. Edits can coexist with a held context issue; a commentary move does not
resolve an unrelated missing assumption. Per-agent reports distinguish body screening
from formal-source checks. The final inventory supersedes their earlier file-presence
classifications. “Screened-clear” is not a mathematical certification.

## Source checks and coordinator corrections

The comparison baseline is site `bb7545d`, library
`e207eefa3d0c91354b42affc0bfcd982a3b05807`. Front matter, UUIDs, titles, formal
bindings, references and proof fields are unchanged from the prior source or exact
generated template. All **155 pre-existing displayed equations** in edited files
remain verbatim. The [source audit](standalone-source-audit.json) checks these
properties, proper note delimiters and semantic link targets.

New context and intentional inline reformulations are justified against linked
signatures/docstrings in the batch reports. In particular, GMRES replaces a formal
iterate call with a locally defined mathematical iterate and explicit Euclidean norm;
CG termination expresses the same equality in prose; tuple notation is expanded
into compatible matrix dimensions. These are reviewed reformulations, not claims
that every inline TeX fragment is byte-identical.

Coordinator checks corrected unsafe moves before publication:

- Kept event E's probability bound and the perturbed-matrix tangent definition in
  their claims. Kept Radau/Lobatto small-support conventions with their definitions.
- Retained the CGS2 threshold, buffer layout and algorithm steps in its definition.
- Restored the Haar proof identity and real/complementary-frame scope. Its real
  matrix dimensions match `NLAlib/RandomMatrix/Haar/Blocks.lean:513–607`.
- Restored generalized Nyström sketch-width scaling and exact-certificate scope
  in the stored block-Krylov identity.
- Defined RSI gap parameters and truncation using `BlockKrylov.lean:436–445,586–596`
  and the singular-gap definition, including its zero/zero convention.
- Put the exact Laplace-transform theorem's nonempty dimension and trace-integrability
  assumptions in the claim (`Probability/MatrixConcentration/Laplace.lean:87–120`),
  with the largest-eigenvalue and functional-calculus notation defined there.
- Preserved the Rademacher fourth-moment identity in commentary; retained the empty
  sketch convention. Gaussian zero-row cases follow the linked source's total-division
  convention, stated explicitly without adding an unsupported nonempty hypothesis.

## Remaining author review

The per-UUID held outcomes identify unresolved mathematical/formulation issues.
Fifteen entries still explicitly depend on surrounding machine/stream/model contracts
(“as above”, “same hypotheses”, or similar). They are marked held, including the dense
Schur unitary corollary caught in the coordinator scan. Do not interpret an edited
flag or a successful renderer as resolving those contracts. Existing alias, empty-prose
and declaration-kind questions remain separate; no identities or discussions are merged.

## Validation

The Explorer suite passes: 151 tests, 11 optional skips. All **7,061 authored
equations** pass KaTeX with zero errors. The complete build succeeds with 164 authored pages, 19,711 library records and
17,925 collaboration objects. All 29 materialized entries retain their exported
UUID/path and complete linked formal evidence in the built editor API. Chromium
checks confirm the corrected CG statement, commentary below the polynomial-bound
box and absent from its list card, commentary retained in editable Markdown, and
the formerly generated Beta identity. Math and styled discussions render without
JavaScript errors. The local preview was refreshed while retaining its session.
