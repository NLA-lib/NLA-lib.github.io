# Luna generated research cohort 08, part 6

Scope: exactly `research[5]` from `/tmp/nla-luna-cohort-08.json`. Pinned template revisions and inherited references were read from the generated object records in `/tmp/nlalib-release-explorer/api/v1/editor/generated/{uuid-prefix}.json`.

| UUID | Result | Source path | Baseline revision | Outcome | Edits | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `c352085a-fd88-5493-a92d-97c059c35625` | `simultaneous-diagonalization` | `explore/content/statements/entry-c352085a-fd88-5493-a92d-97c059c35625.md` | `3976c3c3b16d12b1c3fafb36419ab6ad0366f7bb02a055a81e09384a1cdc2385` | `proposed` | Removed inline citation marker; retained punctuation. All vectors/matrices were already bold, with Hermitian transpose explicit. | `HornJohnson2013`, Theorem 4.1.6 context |
| `0512657a-2988-5bb5-955b-68e4435c629f` | `simultaneous-diagonalization-congruence` | `explore/content/statements/entry-0512657a-2988-5bb5-955b-68e4435c629f.md` | `bcbc5fb4feee138ccdae5d0b47e6a5cc181b161c3155a3d493e69572e27199d7` | `proposed` | Removed inline citation and kept its qualification that ranks and common nullity are stated explicitly. Matrix fonts and adjoints were already consistent. | `HornJohnson2013`, §7.6 |
| `6cf4698e-0d4d-54e6-8eaf-f7b63d2b78d1` | `simultaneous-triangularization` | No source file materialized; generated prose left as-is. | `a1b6011a941752cf869457d5eaa534858f2b14b21db8f21e29efb746fe975fd2` | `already-consistent` | No citation marker to relocate. Matrices, inverse, and Hermitian transpose already use explicit notation. | None in `reference_links.inherited`; prose retains its source provenance note. |
| `b5ff4232-e766-5fc9-bdef-1b122ff6c3d8` | `singular-value-interlacing` | `explore/content/statements/entry-b5ff4232-e766-5fc9-bdef-1b122ff6c3d8.md` | `a8320e6be5faf25d2a135b585852cd394c4d82b67ee0e0d39426d5a169cc8d05` | `proposed` | Removed inline citation marker. Matrix typography was already consistent. | `HornJohnson1991`, Corollary 3.1.3 |
| `4ee993e5-350e-5cd5-a44e-a974c88c0c51` | `sketch-and-precondition` | `explore/content/statements/entry-4ee993e5-350e-5cd5-a44e-a974c88c0c51.md` | `c3ed14d81811b9f6160ef2113361213df15f13aa45ad23f85415b4b584e69b9a` | `proposed` | Removed inline citation, retaining the exact-model qualification as “For the cited case”. Vector and matrix notation was already consistent. | `MartinssonTropp2020`, §10.5 |

No duplicate citation metadata was authored. The pairs above are from each generated object's `reference_links.inherited`; authored `object.references` was not treated as a complete inventory. No definition links were added because no scope-compatible target was verified for concepts in these statements. No theorem identifiers, formulas, hypotheses, IDs, bindings, titles, or front matter changed. The existing prose/title on simultaneous diagonalization carries its hypotheses; this review did not alter them. The triangularization statement's “No printed source” and repository/commit note are preserved provenance, not a bibliographic citation.

## Unresolved issues

- The simultaneous-diagonalization body begins “with real diagonals” and relies on the title for the commuting-Hermitian family context. This is preserved as supplied; any self-containment change would need mathematical/editorial review.
- The triangularization result is explicitly described as generalized from a repository theorem using QR and has no printed source. This provenance remains as-is; it is not represented as a bibliographic reference or a complete proof.
- No mathematical claims were independently validated. No preview/rendering was run in this source-only workspace.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,490 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit: passed; 107 statement files checked. Only the previously recorded `markov-inequality.md` math and `cg-chebyshev-bound.md` reference metadata differences were reported, both outside this batch.
- Manifest UUIDs and staged paths were checked against `research[5]`; the unchanged triangularization result was not materialized, and staged paths include only the four edited entries and this report.
