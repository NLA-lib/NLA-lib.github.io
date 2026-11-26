# Luna research cohort 07, part 9

Scope: manifest `research[8]` in `/tmp/nla-luna-cohort-07.json`; five assigned statements inspected. This report records an editorial review; it does not validate the mathematics or the Lean correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- |
| `20efeb03-db73-58b6-b181-c8ccc263a5a2` | `explore/content/statements/nlalib-smalleig-smalleigprog-pwrites-schur.md` | `b383896c1ca7bb2057807ea3cdf4bbad8521b05c859ea68b7d1126d6eba17a42` | `needs-mathematical-review` | No source edits. Existing bold vector and matrix notation is consistent; no safe, direct definition link was identified. | `BanksGarzaVargasSrivastava2025`, Theorem 1.1 |
| `69d70e2e-9dfa-5224-b7b9-d22da53af29f` | `explore/content/statements/nlalib-smalleig-smalleigprog-randomschurleafcontract.md` | `e100a402ce69910f8ee8f7ae54c95a79e9352a58ffc9b28a603c9e88c4f94d90` | `needs-mathematical-review` | No source edits. Existing bold vector and matrix notation is consistent; no safe, direct definition link was identified. | `BanksGarzaVargasSrivastava2025`, Theorem 1.1 and Corollary 1.3 |
| `0cd1700e-4394-558a-9ae2-d85e718cf79c` | `explore/content/statements/nlalib-spectralbisection-bisectionroutine-meets.md` | `99069dd354533b425f7fa606d8805b45cdd4fbdeef86639d7fd61cfdf7879d2c` | `already-consistent` | No source edits; no notation issue or useful direct definition link found. | None in linked declaration record |
| `f7cd488d-0af0-5fd3-8467-b88519a1ea9d` | `explore/content/statements/nlalib-spectralbisection-certifies-work.md` | `58e05d0d6033f98d124d18c7ca4d404ce2e57dbf3adffdc6db0a8b4de3e3654b` | `needs-mathematical-review` | No source edits. No safe direct definition link identified. | None in linked declaration record |
| `f80f0ee3-19d9-5a56-9908-696b3c4dda51` | `explore/content/statements/nlalib-spectralbisection-eigh-tapemachine-roundtape.md` | `4400eb7725907cfe8f4df7539fd73f6d4dc82e213206e0008cabd0e45e784985` | `already-consistent` | No source edits; no notation issue or useful direct definition link found. | None in linked declaration record |

## Evidence and unresolved issues

- Reference associations were read from each linked declaration's `record.references` in `/tmp/nlalib-release-explorer/api/v1/declarations/`. The SmallEig files have the associations shown above, so no front-matter citations were added. The other three declaration records have empty `record.references`.
- Both SmallEig statements say “machine and streams as above” or “machine and streams above.” Their standalone statement text does not specify that context. Preserve the wording pending a decision about its intended source section and whether that context can be included without changing the claim. The first statement also refers to “the eigenvalue theorems below.” These source-context dependencies merit review; no hypotheses were inferred.
- `certifies_work` states a bound with scalar budget `\\mathcal{H}(n,L,c)`, but neither the statement nor the linked theorem's surrounding source defines this symbol. In the pinned Lean source, `NLAlib/Eigensolvers/SpectralBisection/WorkCertification.lean` theorem `certifies_work` certifies `workSpecification`; `Resources.lean` defines the full instruction budget as `staticBudget d`, while `WorkSpecification.lean` describes work as that static resource charge plus `(L+1)(2c+11)T(n)`. The sources do not establish that `\\mathcal{H}(n,L,c)` is an unambiguous readable rendering of that budget. Define/clarify it from the authoritative model before editing the formula.
- `bisectionRoutine_meets` refers to a mathematical word algorithm without a direct definition link. No exact existing definition page was verified as a scope-compatible target, so none was guessed.
- `eigh_tapeMachine_roundTape` distinguishes the rounded-tape reference from the ideal-sample recursion. No direct definition target was verified that preserves that distinction; no link was added.
- No symbol-role registry additions proposed. No hypotheses, formulas, prose, citations, titles, bindings, or metadata were changed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed the ID, front-matter, kind, binding, title and target-ID checks. It reports 75 statement files changed in the branch history; the only mathematical-fragment discrepancy requiring explicit review is the pre-existing `markov-inequality.md` change, and the only newly added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither file is part of this batch. No group9 statement source is changed or flagged by the audit.
- Preview/rendering was not run in this local source-only review.
