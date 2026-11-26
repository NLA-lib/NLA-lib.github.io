# Luna spectral definitions cleanup 01

Batch scope: the four assigned authored definitions only. Baseline revision tokens and reference metadata were read from the pinned release Explorer snapshot at `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`. Each object has `object.references: []` and `reference_links: null`; each evidence record is `authored` without a Lean declaration binding, so no declaration-level inherited citations apply. No bibliography strings were present in the four bodies. No draft/proposal was submitted; this commit contains the bounded source edits and report for review.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `d5bca832-63a1-5043-ab6e-03b8402a2a55` | `explore/content/statements/singular-value-decomposition-d5bca832.md` | `b75091f9a36d8a3ad0558d02a6011bf922e4c82f3347511fe24d4246820a51f5` | `proposed` |
| `581c9098-24f3-55b6-bd36-a47af48b21ff` | `explore/content/statements/singular-values-581c9098.md` | `6409e33fce97eb06e022aa1dde88fc11a93ed4de45baaabbf9e2acc81d043d53` | `proposed` |
| `af61ef21-9f45-5d71-87c8-6d01c16be15e` | `explore/content/statements/hermitian-functional-calculus-af61ef21.md` | `471d1066f3f5fb381d1174b5c22bfc8a96bbd2054879619001895ef9bc2fae0f` | `proposed` |
| `49f5c3f6-f926-5bc6-b401-16993ec1e357` | `explore/content/statements/hermitian-spectral-decomposition-49f5c3f6.md` | `238d94f97ca8acba57749dd1dc53e6c9ca749977c2661a1fb0d25750ca6fce4a` | `proposed` |

## Changes and references

- **Singular-value decomposition**: changed matrix `\mathbf\Sigma` to `\boldsymbol{\Sigma}` and linked the existing term “singular values” to the specific singular-values definition, UUID `581c9098-24f3-55b6-bd36-a47af48b21ff`. The target defines singular values using `\mathbf{A}^{\mathsf{H}}\mathbf{A}` and imposes no real-only scope; it is compatible with the source's unitary and Hermitian-transpose notation. No hypotheses, dimensions, order, or truncation claim changed.
- **Singular values**: linked the existing phrase “singular-value decomposition” to UUID `d5bca832-63a1-5043-ab6e-03b8402a2a55`. Its target explicitly defines the diagonal singular values in nonincreasing order. No assertion about square roots, zero padding, perturbation, or truncation changed.
- **Hermitian functional calculus**: changed matrix `\mathbf\Lambda` to `\boldsymbol{\Lambda}` and linked the existing word “Hermitian” to the Hermitian spectral-decomposition definition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`. The target uses `\mathsf{H}` and describes a real diagonal matrix for Hermitian input; it does not impose a real-only field. The displayed formula, function domain condition, and independence-from-eigenbasis assertion are unchanged.
- **Hermitian spectral decomposition**: changed matrix `\mathbf\Lambda` to `\boldsymbol{\Lambda}` in both occurrences. No link was added: the page is itself the specific definition of Hermitian spectral decomposition, and the available functional-calculus definition uses this decomposition rather than defining a more specific matching concept. The claims about variational principles and interlacing remain unchanged.

All four are authored definitions with no linked Lean declaration and no associated declaration citations. Their editor objects have no authored reference associations; no inherited references were found because the evidence is authored, not declaration-bound. No bibliographic prose was removed, and no references were added or duplicated. No proof sources, relocations, or duplicate identities were proposed. IDs, UUIDs, kinds, and review metadata were preserved.

## Scope checks and validation

Read the linked target Markdown definitions and verified their front-matter UUIDs and stated scopes. The definitions use adjoint/unitary notation compatible with complex matrices; none of the links points to the real-only Krylov-space definition. No standalone Lean source binding exists for these authored blocks in the pinned editor metadata, so no formal source correspondence is claimed.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or any unstated field/dimension assumptions.

## Registry proposal

The changed and linked matrices `\Sigma` and `\Lambda` are Greek matrix symbols and should be considered for reviewed registry declarations in their specific source scopes. The existing vectors/matrices in these four pages also include `A`, `U`, `V`; scalar indices/eigenvalues such as `k`, `j`, and `\lambda_i` should not be declared bold. No global notation registry edit was made.
