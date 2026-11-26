# Luna generated research cohort 08, part 3

Scope: manifest `research[2]` in `/tmp/nla-luna-cohort-08.json`; five generated results materialized from their exported templates using their existing UUIDs, result bindings and titles.

| UUID | Result key | Source path | Baseline generated-object revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `b27ec719-ddb2-5204-b230-f9041a8695c5` | `schatten-holder` | `explore/content/statements/entry-b27ec719-ddb2-5204-b230-f9041a8695c5.md` | `cb80f659b080632a01a23e276c34a140c44bd3ec86336b6a960cff3883784d3d` | `proposed` | Removed the inline citation marker; the associated reference remains inherited below. No front-matter citation added. | `Bhatia1997`, Corollary IV.2.6 |
| `2a7fc0a6-889a-5d36-a4cb-0f493165d7d8` | `schatten-norm` | `explore/content/statements/entry-2a7fc0a6-889a-5d36-a4cb-0f493165d7d8.md` | `f58b4b4cbf7826b92f4117aac436beeba720fbc58611ba19386af67187fa4eff` | `proposed` | Removed the inline citation marker; the associated reference remains inherited below. No front-matter citation added. | `Bhatia1997`, §IV.2 |
| `b22242ec-234e-50f4-840d-32150ce269e3` | `schur-complement-concave` | `explore/content/statements/entry-b22242ec-234e-50f4-840d-32150ce269e3.md` | `a6de30531eda5554993dd551f85750602c21771a0c342d572fb036b6e1b8664d` | `proposed` | Removed the inline citation marker and clarified its locator-dependent qualification as “The cited form assumes weights sum to one.” This retains the source's contrast with the current nonnegative-weight superadditivity statement. No front-matter citation added. | `EpperlyWebber2026`, Fact 6.1(c) |
| `9181a3ab-3dc1-558e-9188-a9892856796e` | `schur-complement-monotone` | `explore/content/statements/entry-9181a3ab-3dc1-558e-9188-a9892856796e.md` | `c014dd0102390c0f93fd60818221d36e20c406e29cb5b6508c8477283a899ee5` | `proposed` | Removed the two inline citation markers; both associations remain inherited below. No front-matter citation added. | `MartinssonTropp2020`, Corollary 11.2; `EpperlyWebber2026`, Fact 6.1(d) |
| `cb28fc5e-ad1e-5cbd-b266-c3193e81ac6e` | `schur-complement-pd` | `explore/content/statements/entry-cb28fc5e-ad1e-5cbd-b266-c3193e81ac6e.md` | `d145590527f8aa0ccf35a16c4ee1742dfec0a5b8d335a8255933637bde17deef` | `proposed` | Removed the inline citation marker; the associated reference remains inherited below. No front-matter citation added. | `HornJohnson2013`, Theorem 7.7.7 |

## Evidence and unresolved issues

- Baseline text and `reference_links.inherited` were read from each pinned generated-object snapshot in `/tmp/nlalib-release-explorer/api/v1/editor/generated/`. The citations above are already attached; no reference front matter was added.
- No exact scope-compatible definition page was verified for the Schur complement operator `\\mathbf{H}/\\boldsymbol{\\Omega}`. Its local formula remains in the source body. No concept link was guessed.
- The existing Matrix norms definition page `/explore/statements/19646f49-e8db-5918-a0df-83eaf8db1648/` states Schatten norms for complex matrices. The trace Holder, triangle, and duality claims here are over generic RCLike fields; no field-incompatible link was added.
- `schatten-holder` / `schatten-duality` and `schatten-norm` / `schatten-even-moment-smoothness` are related norm results with distinct IDs and claims. The three Schur-complement results state concavity, monotonicity and positive-definiteness criteria separately. No results were merged.
- No formulas, assumptions, delimiter segmentation, titles, result bindings, UUIDs or other front matter changed. No symbol-role registry additions proposed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,339 equations; 0 errors).
- `git diff --check`: passed.
- Manifest UUIDs, actual inherited reference pairs, and staged-path scope: passed.
- Required staged content audit: passed ID, front-matter, kind, result binding, title/options and target-ID checks. It reports 93 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch.
- Preview/rendering was not run in this local source-only review.
