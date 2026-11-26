# Luna research cohort 07, part 14

Scope: manifest `research[13]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements reviewed. This review does not validate the mathematics or formal correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited key/locator pairs |
| --- | --- | --- | --- | --- | --- |
| `a3ae6eab-cfd1-54a1-a5cb-aabb2ed528b6` | `explore/content/statements/shifted-qr-rounded-small-eig-backward-error.md` | `c40e26f12e903225c7b8db767ecbcb0ec1cf7ea91095673e4da771a83820fcd2` | `needs-mathematical-review` | No source edit in this batch. | `BanksGarzaVargasSrivastava2022`, Theorem 6.3 |
| `bfa69b03-df3e-57c8-a9a5-dbb0ca6bab06` | `explore/content/statements/shifted-qr-rounded-small-eig-certificate-accuracy.md` | `e1f6be38cff986459b7eb9751079fb6b3b1953e87365abbac079ca52d7e13049` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2022`, Theorem 6.3 with Theorem 1.4's quantifiers, corrected |
| `96f14e8b-ee12-585f-a7a5-5142971ee656` | `explore/content/statements/small-eig-certificate-accuracy.md` | `a007828cf7b37d55473cc086f89028741dd655ac13afdb7217a1e675d2173a0b` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2025`, Theorem 1.1 |
| `5122ab2d-9ad3-5c4d-a1d7-1ae5aed4b848` | `explore/content/statements/small-eig-forward-error.md` | `c1ac6b120dcf1df555552d527950ca99f7b682dd1639eeccf86140dd5b298af6` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2025`, Corollary 1.3 |
| `c6b82b37-af7d-54c6-8a6e-3649062c1667` | `explore/content/statements/spectral-bisection-operation-count-accuracy.md` | `c4445d5eb1f90eab73629d35f93772d6acd2f9190a1d078198337abb063cf349` | `proposed` | Earlier out-of-order commit `babd861f2cdb937bde276a8eccfebc419580aef1` changed `\\mathbb C` to `\\mathbb{C}` in this assigned file. This is a bracing-only notation improvement; it is recorded here and was not repeated. | `Shah2024`, Theorem 4.2 |

## Evidence and unresolved issues

- Inherited references were read from each editor object's `evidence.declaration` and the linked declaration's `record.references`. The exact pairs are above; object-authored `references` arrays were not used to infer absence. No front-matter citation additions were made.
- The first two shifted-QR statements depend on “hypotheses above,” “machine and tape” context, “theorem above,” and a guarantee shape not reproduced in each standalone statement. Clarify intended context and relationships before rewriting. No conditions were inferred from neighboring entries.
- `small-eig-certificate-accuracy` refers to “Theorem 1.1” and “the certificate” without a direct stable result link or self-contained certificate definition. Verify the intended target and quantitative certificate source before changing the wording.
- `small-eig-forward-error` uses “machine and streams as above” without carrying that context locally. No new hypotheses were supplied.
- `spectral-bisection-operation-count-accuracy` says the Lean statement supplies conditions on roundoff, accuracy, and range rather than stating them. The pinned declaration is `NLAlib.SpectralBisection.measureReal_not_accepts_countedSpecification_le` in `NLAlib/Eigensolvers/SpectralBisection/RunTheorem.lean`; its complete assumptions are extensive. Review whether to give a concise, exact hypothesis list or keep the cross-reference. The earlier `\\mathbb C` bracing change did not alter the formula or delimiter segmentation.
- No direct, scope-compatible definition page was verified for the referenced certificates or algorithms. No definition links were added. No symbol-role registry additions proposed.
- The two shifted-QR results and two SmallEig results have distinct bindings and scopes. No entries were merged or identifiers changed.
- The only verified out-of-order group14 source edit is `spectral-bisection-operation-count-accuracy.md`, changed in commit `babd861f2cdb937bde276a8eccfebc419580aef1` as described above. `shifted-qr-rounded-small-eig-backward-error.md` has no diff in that commit or another prior cleanup commit. Neither file was changed in the current commit.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed ID, front-matter, kind, binding, title and target-ID checks. It reports 81 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch.
- Preview/rendering was not run in this local source-only review.
