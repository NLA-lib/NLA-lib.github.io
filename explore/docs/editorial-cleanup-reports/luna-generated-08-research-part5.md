# Luna generated research cohort 08, part 5

Scope: manifest `research[4]` in `/tmp/nla-luna-cohort-08.json`; five generated results materialized from their pinned templates using the same UUIDs, result bindings and titles.

| UUID | Result key | Source path | Baseline generated-object revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `70c17739-9ee4-52eb-b143-200b51164396` | `schur-triangularization` | `explore/content/statements/entry-70c17739-9ee4-52eb-b143-200b51164396.md` | `dc89953c5dc70375cc030f07c35dc58f63726645ecba03645773003e31525379` | `proposed` | Removed the inline citation marker; the inherited reference remains attached below. No front-matter citation added. | `HornJohnson2013`, Theorem 2.3.1 |
| `31230bd6-7306-5980-a55f-4a557ca361cb` | `shifted-qr-normal-decoupling` | `explore/content/statements/entry-31230bd6-7306-5980-a55f-4a557ca361cb.md` | `bc1768495741b9cb63184ffd74c43bc729b76514fdf1b9e2f7542af61ed45d73` | `needs-mathematical-review` | Removed the inline citation marker and preserved the source theorem comparison and strategy qualification in prose. No front-matter citation added. | `BanksGarzaVargasSrivastava2021`, Theorem 1.2 |
| `3bbe8a2b-7015-5f3b-825d-69be73b21a79` | `shifted-qr-rapid-decoupling` | `explore/content/statements/entry-3bbe8a2b-7015-5f3b-825d-69be73b21a79.md` | `34856ccdf1ca2aff55f584028a5ef4a9c54a15ae1e57868e867ecfa750064626` | `proposed` | Removed the inline citation marker and retained the citation's ceiling-bound qualification. No front-matter citation added. | `BanksGarzaVargasSrivastava2021`, Definition 1.5; `BanksGarzaVargasSrivastava2021`, Theorem 1.6, item 1 |
| `d87a4d6a-1227-58b3-a62d-c7efe303ce7d` | `shifted-qr-ritz-dichotomy` | `explore/content/statements/entry-d87a4d6a-1227-58b3-a62d-c7efe303ce7d.md` | `5265f4908aa6f2217d1293f246a345eb4c8924cae5dc89e401ac37a2bd53971a` | `proposed` | Removed the inline citation marker and retained its constant/strict-inequality qualifications. No front-matter citation added. | `BanksGarzaVargasSrivastava2022`, Theorem 4.1 |
| `a8cb327d-7e48-5c55-8ecb-e5d90758d5d9` | `simple-eigenvalue-perturbation` | `explore/content/statements/entry-a8cb327d-7e48-5c55-8ecb-e5d90758d5d9.md` | `b8355888e20243e7470765e1e49a4c8de37457e6804ae5f5f7f5eed927f1dec6` | `proposed` | Removed the two inline citation markers; both inherited references remain attached below. No front-matter citations added. | `StewartSun1990`, Theorem IV.2.3; `HornJohnson2013`, Theorem 6.3.12 |

## Evidence and unresolved issues

- Baseline source and `reference_links.inherited` were checked from each pinned generated-object snapshot. The exact citations above are already attached, so no bibliography associations were duplicated.
- `shifted-qr-normal-decoupling` has an apparent locator inconsistency in its explanatory text: its inherited association is Theorem 1.2, while the source text parenthetically describes “Theorem 3.3 there for $k=2$.” This may distinguish the general theorem from its $k=2$ case, but the intended numbering should be confirmed. The text retains both details without choosing between them.
- `simple-eigenvalue-perturbation` intentionally uses the bilinear left-eigenvector expression with transpose, not Hermitian transpose, and explicitly explains that distinction. The notation and formulas were preserved.
- No scope-compatible direct definition links were verified for the QR strategies, Ritz values, or simple-root perturbation. No links were added. No symbol-role registry additions proposed.
- No formulas, hypotheses, delimiter segmentation, titles, result bindings, UUIDs or other front matter changed.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,443 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Manifest UUIDs match all five report rows; inherited references were checked against each pinned generated object; staged paths contain only these five sources and this report.
- Required staged content audit: passed; 103 statement files checked. The only reported differences were `markov-inequality.md` math and `cg-chebyshev-bound.md` reference metadata, both outside this batch and previously recorded.
- Preview/rendering was not run in this local source-only review.
