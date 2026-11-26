# Luna generated research cohort 08, part 4

Scope: manifest `research[3]` in `/tmp/nla-luna-cohort-08.json`; five generated results materialized from exported templates with their original UUIDs, result bindings and titles.

| UUID | Result key | Source path | Baseline generated-object revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `2c359366-8d29-533a-b8a7-149cc46a9841` | `schur-complement-rank` | `explore/content/statements/entry-2c359366-8d29-533a-b8a7-149cc46a9841.md` | `f9e77e50396bef3f91492c7903e6ae97adb74ea5699d9c404a631c09bb628ada` | `proposed` | Removed the inline reference marker and retained “This holds over any field.” No front-matter citation added. | `HornJohnson2013`, §0.8.5 |
| `d6550e6d-9c4b-58e0-877c-0ccfb5c5db7e` | `schur-complement-variational` | `explore/content/statements/entry-d6550e6d-9c4b-58e0-877c-0ccfb5c5db7e.md` | `a448b08bfdab5f9145d6f4069c83e475bc1a223180f7b8d13864e3de83038791` | `proposed` | Removed the inline citation marker; the inherited reference remains attached below. No front-matter citation added. | `HornJohnson2013`, §7.7 |
| `0ede5147-2b69-5e88-9b61-0da666b4709c` | `schur-horn` | `explore/content/statements/entry-0ede5147-2b69-5e88-9b61-0da666b4709c.md` | `5a7089727fcc0c34710e4d3cdf2aa100bd57ec1ddef7ba3b2419016a9dc07d80` | `needs-mathematical-review` | Removed the inline citation marker; the inherited pair remains attached below. No front-matter citation added. | `HornJohnson2013`, Theorems 4.3.45 and 4.3.48 |
| `86f124a4-cb74-570d-bb01-8bfaab2bd74e` | `schur-majorization` | `explore/content/statements/entry-86f124a4-cb74-570d-bb01-8bfaab2bd74e.md` | `dae7401bd3e339d030144a1f39b38cd69307cbb10474b8c99dee97dfac43f86c` | `needs-mathematical-review` | Removed the inline citation marker; the inherited pair remains attached below. No front-matter citation added. | `HornJohnson2013`, Theorem 4.3.45 |
| `f518e331-6b89-52b4-a076-944c38cd8212` | `schur-product-power-series` | `explore/content/statements/entry-f518e331-6b89-52b4-a076-944c38cd8212.md` | `353541fbc89450d4f425e6c4d0ab693277c421e043c9f0a059d203ed7623cbdf` | `proposed` | Removed both inline citation markers; both inherited associations remain attached below. No front-matter citations added. | `HornJohnson2013`, Theorem 7.5.9; `HornJohnson1991`, Theorem 6.3.6 context |

## Evidence and unresolved issues

- Baseline text and `reference_links.inherited` were checked in the pinned generated-object snapshots. All bibliography associations listed above are inherited; none were duplicated.
- `schur-horn` and `schur-majorization` need a notation/mathematical interpretation review. The latter explicitly says eigenvalues use Mathlib's enumeration “indexed by n rather than sorted,” while the existing Loewner order and majorization definition (UUID `94212462-4541-5bf1-96ea-38d5e791525e`) describes majorization of ordered scalar lists. Confirm how the eigenvalue enumeration interacts with that definition before linking or editing. No claim was repaired by assumption.
- The Schur-complement items use the Schur complement in distinct rank, variational, monotonicity and positivity contexts. No existing page was verified as a direct definition of the generic Schur complement, so no definition link was added.
- The power-series result's phrase “converging at every entry” and its real positive-semidefinite matrix domain were retained as written; no convergence claim was inferred beyond the statement.
- No formulas, delimiter segmentation, theorem bindings, UUIDs, titles, or other front matter changed. No symbol-role registry additions proposed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,359 equations; 0 errors).
- `git diff --check`: passed.
- Manifest UUIDs, actual inherited reference pairs, and staged-path scope: passed.
- Required staged content audit: passed ID, front-matter, kind, result binding, title/options and target-ID checks. It reports 98 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch.
- Preview/rendering was not run in this local source-only review.
