# Luna research cohort 07, part 10

Scope: manifest `research[9]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements inspected. This editorial review does not certify the mathematics or its formal correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- |
| `60207554-de12-55e9-aa40-b0c5c81d3f44` | `explore/content/statements/nlalib-spectralbisection-initialbytes-add-staticpeak-workspaceenvelope-le.md` | `eb1e333596ec3aafa9ef7284cf33f1a7e6eedab50669ba6dab604e6809e646bb` | `needs-mathematical-review` | No source edits. | None in linked declaration record |
| `67eaecd1-e828-5359-a866-13159be34f30` | `explore/content/statements/nlalib-spectralbisection-measurereal-not-accepts-le-of-wordspecification.md` | `ff08ca3228c36f2540861e8ec23d520c0977585eabacc87121756b46b3a82002` | `already-consistent` | No source edits; vector/matrix font and adjoint notation are consistent. | None in linked declaration record |
| `cf88b5ab-1c6e-5e1b-a9b7-3af59a9bf94b` | `explore/content/statements/nlalib-spectralbisection-staticpeak-workspaceenvelope-le.md` | `74fe381242552b4fd68fe4937632a04f19822cd95449b991acd56e762f96897f` | `needs-mathematical-review` | No source edits. | None in linked declaration record |
| `18fb3656-465b-5da8-bce5-1fa5a2eab23c` | `explore/content/statements/nysbki-gapless-error.md` | `f1bbb9589c929dd093219a42f8926be692f91e3affcb00f3a4882fdeead27e03` | `needs-mathematical-review` | No source edits; existing matrix/vector notation is consistent. | None in linked declaration record |
| `d74a9224-eb70-5c39-9686-25440e2eceab` | `explore/content/statements/nysbki-gapped-error.md` | `1069418088c9870a096b11bb044ba601af1ab93c96c0a9c36a355f7d63dbc2bf` | `needs-mathematical-review` | No source edits; existing matrix/vector notation is consistent. | None in linked declaration record |

## Evidence and unresolved issues

- For all five entries, the editor object has no authored references, and the linked declaration's `/tmp/nlalib-release-explorer/api/v1/declarations/{declaration}.json` record has no references. No citation associations were added. The NysBKI Lean comments contain literature citations (including Tropp and Webber 2023), but those source comments do not establish that those citations are attached to these particular shared statement objects; they were not copied into front matter.
- The two storage bounds use `E(n)` without defining it in their statement text. The pinned Lean source `NLAlib/Eigensolvers/SpectralBisection/StoragePolynomial.lean`, declarations `staticPeak_workspaceEnvelope_le` and `initialBytes_add_staticPeak_workspaceEnvelope_le` (lines 82 and 124), bounds the corresponding storage with `MatrixOp.workspaceEnvelope matrixWorkspace n`. Clarify whether `E(n)` denotes that argument-dependent envelope before revising the statement. The source has no matching user-facing definition page verified for linking.
- Both NysBKI expected-error statements describe a symmetric positive semidefinite matrix and a Gaussian test matrix in the pinned source, but the readable statements do not state these hypotheses or define a probability law. The source declarations in `NLAlib/LowRank/Gaussian/NystromBlockKrylov.lean` take `hH : H.PosSemidef` and `hX : HasLaw X (gaussianMatrix n l) μ`; the gapless exponential result also requires `q ≥ 2` and `σ_r(H)>0`, while the gapped result requires `h+1=r`, `r≤t`, `t+2≤ℓ`, and `q≥1`. The statement parameters/formulas differ in presentation from those declarations. Review the intended support and hypotheses before proposing edits; none were invented or inserted.
- No direct, scope-compatible definition page was verified for the workspace envelope or the NysBKI procedure, so no links were added. No symbol-role registry additions proposed.
- `measureReal_not_accepts_le_of_wordSpecification` is a transfer statement and explicitly says its reference numerical hypotheses are established separately. No unsupported hypotheses were introduced.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed the ID, front-matter, kind, binding, title and target-ID checks. It reports 75 statement files changed in branch history; the only mathematical-fragment discrepancy requiring explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch. No group10 statement source changed or was flagged by the audit.
- Preview/rendering was not run in this local source-only review.
