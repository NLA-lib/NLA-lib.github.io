# Luna research cohort 07, part 16

Scope: manifest `research[15]` in `/tmp/nla-luna-cohort-07.json`; all three assigned statements reviewed. This is an editorial review, not validation of the mathematics or formal correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited key/locator pairs |
| --- | --- | --- | --- | --- | --- |
| `045e0daf-23ac-5e28-a6ba-063cb765120c` | `explore/content/statements/verified-schur-failure.md` | `13e0b41334c752edbf365a6628b8cd8f5aa6b7dc8c2c69a01561057c976dfba4` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2022`, Theorem 1.4; `BanksGarzaVargasSrivastava2025`, Theorem 1.1 |
| `777e5b76-3146-59ce-aa61-62433005ed7f` | `explore/content/statements/weyl-perturbation.md` | `79c65d9b78344d4843d629553ad0e2c619c441ae70d857ce7d5cabe93275b079` | `already-consistent` | No source edits. | `HornJohnson2013`, Corollary 4.3.15 |
| `8ba94112-3da1-543b-8c52-509a006866b6` | `explore/content/statements/weyl-singular-values.md` | `8f64a2363b019caba1ecfc5f6d6964c10c4ea599b19c86380c667da024ee6349` | `already-consistent` | No source edits. | `HornJohnson2013`, Corollary 7.3.5 |

## Evidence and unresolved issues

- Inherited citations were read from each editor object's `evidence.declaration` and the corresponding declaration `record.references`. These associations are already attached; no front-matter citations were added.
- `verified-schur-failure` depends on the dense Schur theorem's machine and stream setup and uses `u_ver`, `delta_int`, and `R` without local definitions. Its pinned source, `NLAlib/Eigensolvers/Schur/VerifiedDense.lean`, defines the context in the declaration docstring around lines 144–164, including `delta_int = delta/(16(n+1))` and the rotation count. Clarify the standalone context and notation before revising; do not assume readers have the neighboring theorem in view.
- The Weyl eigenvalue and singular-value statements match the source's same-index ordering and field/domain behavior. The source declarations accept complex matrices where appropriate, so no field qualification was added. No safe definition page was verified for linking the generic eigenvalue or singular-value terms.
- No formulas, hypotheses, titles, bindings, IDs or metadata changed. No symbol-role registry additions proposed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed ID, front-matter, kind, binding, title and target-ID checks. It reports 82 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch.
- Preview/rendering was not run in this local source-only review.
