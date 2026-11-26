# Luna generated research cohort 08, part 10

Scope: exactly `research[9]` from `/tmp/nla-luna-cohort-08.json`, the final five entries in this manifest.

| UUID | Result | Source path | Baseline revision | Outcome | Change | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `156a906a-a0e2-5c5c-af09-d55eb98f3272` | `spectral-norm-net` | `explore/content/statements/entry-156a906a-a0e2-5c5c-af09-d55eb98f3272.md` | `4c25d05722c60e3bdd8d5dcb9ef9c7478292f84e5982dc78489e10bcb1d12d89` | `proposed` | Removed inline citation marker; notation was already role-consistent. | `Vershynin2018`, Lemma 4.4.1 with Corollary 4.2.13 |
| `80d1186e-808a-5ca5-a1b6-380529a18492` | `spectral-theorem-hermitian` | `explore/content/statements/entry-80d1186e-808a-5ca5-a1b6-380529a18492.md` | `33145dda3a128a88639ea22070bad7371e8f1b4b03bb22225844e07b8b76a06c` | `proposed` | Removed inline citation marker; matrix font and Hermitian transpose were already consistent. | `HornJohnson2013`, Theorem 2.5.6 |
| `31990abb-844c-57f6-af5c-5d27986d72ef` | `sphere-projection-beta` | No source file materialized; generated prose left unchanged. | `6ee69d38660abfab0faec203277a1aa202783059e8cc8e279d37d1b367edf5df` | `already-consistent` | No inline citation to move; “No printed source” retained. | None in `reference_links.inherited` |
| `57a50ed5-8ec1-58c2-87c3-9e66b8fe18c0` | `sphere-projection-tail` | `explore/content/statements/entry-57a50ed5-8ec1-58c2-87c3-9e66b8fe18c0.md` | `38db138c2bc318862a06eda0fa4813cfd590fa3ac021f6eb7ebf9e5ca633524c` | `proposed` | Removed inline citation marker and retained its role as the Beta proxy before Hoeffding's inequality. | `MarchalArbel2017`, Theorem 1 |
| `bd3fc175-221b-5b2e-8e81-4a6eb1299f06` | `srht-ose` | `explore/content/statements/entry-bd3fc175-221b-5b2e-8e81-4a6eb1299f06.md` | `39d7593704981cddf5d0aa8b69b9c6c0b87a13663d0db826077f7f287379b0f4` | `proposed` | Removed four inline citation markers and retained the four source-specific comparison claims in their original order. | `Woodruff2014`, Theorem 7; `MartinssonTropp2020`, §9.3; `HalkoMartinssonTropp2011`, Theorem 11.1; `Tropp2011a`, Theorems 1.3 and 3.1 |

Inherited associations are taken from `reference_links.inherited`; no duplicate authored references were added. No definition links were added because no precise compatible existing target was verified. No formulas, assumptions, identities, bindings, titles or front matter changed. The Beta projection statement and the sample-mean tail statement concern related but distinct claims; their IDs were retained independently.

## Unresolved issues

- No printed source is listed for `sphere-projection-beta`; that metadata and wording remain unchanged.
- The four SRHT comparisons are retained in the same order as the four inherited associations, without claiming that one cited result establishes another's parameters.
- No mathematical correctness review or preview/rendering was performed.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,746 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit and manifest UUID/staged-path checks: passed.
