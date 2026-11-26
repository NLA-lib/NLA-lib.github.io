# Luna generated research cohort 10, part 3

Scope: exactly `generated[2]` in `/tmp/nla-luna-cohort-10.json`.

| UUID | Result | Source path | Baseline revision | Outcome | Change | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `41e7588a-0b75-5486-9e74-ee831166343e` | `truncation-lemma` | `explore/content/statements/entry-41e7588a-0b75-5486-9e74-ee831166343e.md` | `b27688ec17c96e9d245507488260d502771671a0f32047c7dbc4cd526468d5d2` | `proposed` | Removed inline citation and retained the exact scope comparison between the cited spectral-norm case and this all-gauge statement. | `HalkoMartinssonTropp2011`, Theorem 9.3 |
| `f10639b1-227e-50f0-8936-812adec828cd` | `two-pass-low-rank-lower-bound` | No source file materialized; generated prose left unchanged. | `6b1c8bfe304fe5f4fa33df17f0c1586a4fa8ae54dfc5aa4827d125c76b26f05d` | `already-consistent` | No inline citation; “No printed source” retained. | None in `reference_links.inherited` |
| `60b21f16-92a6-525f-b458-1d1118bbdc59` | `unitarily-invariant-norm` | `explore/content/statements/entry-60b21f16-92a6-525f-b458-1d1118bbdc59.md` | `ae5d5eb4344d114bf938a85a9a43f11a5005156901ba9d7a4f01a1954816e59d` | `proposed` | Replaced the inline bibliographic citation with “the cited theorem,” retaining the comparison's attribution. | `Bhatia1997`, Theorem IV.2.1 |
| `731bacba-eb21-566d-bb10-813628fe5a7e` | `unreduced-hessenberg-krylov-basis` | `explore/content/statements/entry-731bacba-eb21-566d-bb10-813628fe5a7e.md` | `e307064644e4aa41dd35d158d70c092c66fe69f6d14d72b6d439b41d73d504a4` | `proposed` | Removed inline citation marker. Matrix notation was already role-consistent. | `GolubVanLoan2013`, §7.4.3 |
| `3cbe2323-ea8a-5f66-8e2c-cee16108a531` | `ville-inequality` | No source file materialized; generated prose left unchanged. | `7b1cb6ad5a7469d24e1b1413abf0a1d0298d87a747cff2037eba12e318d20b24` | `already-consistent` | No bracketed inline bibliography citation or inherited association. The existing “Due to Ville (1939)” attribution remains. | None in `reference_links.inherited` |

The reference pairs above are from `reference_links.inherited`; no authored duplicates were added. No definition link was added because no precise scope-compatible target was verified. Formulas, assumptions, IDs, titles, bindings and front matter were preserved.

## Unresolved issues

- `ville-inequality` retains “Due to Ville (1939)” without an inherited structured reference. No citation key was inferred or added; a reference metadata review would be needed if this attribution should appear in the page's References section.
- No mathematical audit or preview/rendering was performed.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,827 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit and manifest UUID/staged-path checks: passed.
