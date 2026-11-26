# Luna randomized cleanup 03 — part 1

Scope is the first five assigned authored definitions in `/tmp/nla-luna-cohort-03.json`.
The baseline revision tokens are from the pinned editor-object snapshots under
`/tmp/nlalib-release-explorer/api/v1/editor/objects/`. All five objects are authored
statements without linked Lean declarations; their snapshots have no inherited
reference records. The bodies contain no bibliographic citation strings. No source
references were added or removed.

## Per-UUID results

### `36be1f8d-abc5-5dfd-b557-ff75ebe97822` — Filtered range-finder approximation

- Baseline revision: `2eb81ce8b402503a07b8562345467c4ed7b6e67c0c41fe0975a012dabebf257a`.
- Source: `explore/content/statements/filtered-range-finder-approximation-36be1f8d.md`.
- Outcome: `proposed`.
- Changed the Greek test matrix from `\mathbf\Omega` to `\boldsymbol{\Omega}` in the formula, matching its matrix role. Latin matrices remain bold; scalar filter/function/power variables remain unbolded. No citation strings or references; no definition link added.
- Unresolved: dimensions for the test matrix and spectral filter are not stated. The definition preserves the supplied scope rather than inferring dimensions or filter assumptions.

### `a0a6bea3-9bd3-5ab9-a4d3-c926d57d230b` — Randomized subspace extraction

- Baseline revision: `496efb5be6c7d5e3b1b5406cf0a8a0201758b9f2491577ed4c569a96c5406e65`.
- Source: `explore/content/statements/randomized-subspace-extraction-a0a6bea3.md`.
- Outcome: `already-consistent`.
- Matrix/vector notation is object-aware. No bibliographic citation strings or references; no link added.
- Unresolved: the sample-matrix dimensions are unstated. The existing QR definition requires an `m ≥ n` input for its thin factorization, so it is not a scope-safe target for this entry’s unspecified `G` dimensions. No link was added. Consider clarifying dimensions in a separate mathematical review.

### `90f9c5f5-2db3-5dde-afe2-c2d2f5bdd092` — Randomized subspace iteration

- Baseline revision: `7c9cd370c2293dab1a3dbc18956bb94e44e68dd862ce7a36a05a677369dd9c45`.
- Source: `explore/content/statements/randomized-subspace-iteration-90f9c5f5.md`.
- Outcome: `proposed`.
- Changed the Greek test matrix from `\mathbf\Omega` to `\boldsymbol{\Omega}`. Added verified concept links, preserving original wording: “orthogonal projector” to [Orthogonal projection](/explore/statements/2fa76a05-ce3c-5a1c-9aee-625c01bfd829/), “ordinary range-finder approximation” to [Range-finder approximation](/explore/statements/15e6c9dc-370c-5cb2-b684-46e5f33e39f2/), and “block Krylov iteration” to [Randomized block Krylov iteration](/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/). The targets were read: the projection definition uses orthonormal columns and works over complex matrices; the range-finder target defines the untruncated projected approximation; the block-Krylov target covers real or complex matrices and retains successive powers. No citations or references.
- Unresolved: matrix and test dimensions are implicit in the expression. No unsupported dimensions were added.

### `84f513cb-f346-53d2-a25c-d47827a8967b` — Gaussian sketches and Haar frames

- Baseline revision: `7656e31bb4abc75935c5de60a7d63d2cee07c19dee059717d6aaa134bf227dbe`.
- Source: `explore/content/statements/gaussian-sketches-and-haar-frames-84f513cb.md`.
- Outcome: `already-consistent`.
- No object-notation correction or verified concept link was needed. No citation strings or references.
- Unresolved: the final sentence points to a “relevant law” without identifying a specific law. It is retained as supplied; no source or scaling was invented.

### `cb5e0fa7-3425-5848-83bd-fd73b4aa314e` — Isotropic probes

- Baseline revision: `f5274b6ba115b02083305855f0b27b07cd764ed48ef28d7d10232ba569bef6c3`.
- Source: `explore/content/statements/isotropic-probes-cb5e0fa7.md`.
- Outcome: `proposed`.
- Added a verified link on “standard real Gaussian” to [Gaussian sketches and Haar frames](/explore/statements/84f513cb-f346-53d2-a25c-d47827a8967b/), whose definition gives the independent `N(0,1)` entry law. The target’s matrix law applies to a vector as a one-column matrix. Kept `\mathbf{g}` and `\mathbf{I}` bold and expectation in `\mathbb{E}`. No citation strings or references.
- Unresolved: none identified for this editorial pass.

## Registry, preview and checks

No global symbol-role additions are proposed. `\boldsymbol{\Omega}` is a Greek sketch matrix; the changes are local to the two files where the original bare Greek bold command was malformed for the documented convention. No preview or full content build was run. `node explore/tests/check_notation.cjs` passed: 2,303 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 245 sources; all five batch IDs and all four linked target UUIDs were present. `git diff --check` passed. These checks do not establish mathematical correctness.
