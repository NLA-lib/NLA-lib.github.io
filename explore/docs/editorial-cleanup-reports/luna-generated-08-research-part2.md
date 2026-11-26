# Luna generated research cohort 08, part 2

Scope: manifest `research[1]` in `/tmp/nla-luna-cohort-08.json`; five generated results materialized from their exported templates using the same UUIDs, result bindings and titles. No additional entries were touched.

| UUID | Result key | Source path | Baseline generated-object revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `7822ac76-a0dc-569a-a29e-b4c7974963d5` | `rouche-capelli` | `explore/content/statements/entry-7822ac76-a0dc-569a-a29e-b4c7974963d5.md` | `04dec7604e30c1dd61fe2ae735e6bcf28de322a9d768d8b98908f5d823524ffe` | `proposed` | Removed the inline `[HornJohnson2013, §0.4.2]` marker; the existing declaration reference renders below the statement. No front-matter citation added. | `HornJohnson2013`, §0.4.2 |
| `c5404b4e-7460-5bd2-8df6-f30cd59c408a` | `sampling-without-replacement-ose` | `explore/content/statements/entry-c5404b4e-7460-5bd2-8df6-f30cd59c408a.md` | `03463fb72e255aa3429db95e9c59b12f6dd11f800fab384d8c7435a9f151fe47` | `proposed` | Removed both inline citation markers and retained their source qualifications in prose. Added a direct link on “subspace embedding” to the existing definition page `/explore/statements/dd0c654f-b783-516b-b7c3-04b96f1a90f3/`. No front-matter citation added. | `Tropp2011a`, Lemma 3.4; `Tropp2015`, Theorem 5.1.1 |
| `148514ea-a72c-563e-8654-7835e74e5659` | `sampling-without-replacement-osi` | `explore/content/statements/entry-148514ea-a72c-563e-8654-7835e74e5659.md` | `8e815e3f52e0be1a72063484067438f028e5e71c411e6457935f2f0cb7e17487` | `proposed` | Removed the inline citation marker and retained the comparison's orthonormal-column and sample-size qualifications in prose. No front-matter citation added. | `Tropp2011a`, Lemma 3.4 |
| `1b98ad4f-9cac-578b-81cf-ba9d8a44c47f` | `schatten-duality` | `explore/content/statements/entry-1b98ad4f-9cac-578b-81cf-ba9d8a44c47f.md` | `18272d2a2669407a97ea53bae9ffbdfdcfee21fba4afd890d1d8bbfe0a5478e9` | `proposed` | Removed the inline Bhatia citation marker; the associated reference is rendered below the statement. No front-matter citation added. | `Bhatia1997`, §IV.2 |
| `a4d06846-2e96-5963-9c28-7e6fed02fb0b` | `schatten-even-moment-smoothness` | `explore/content/statements/entry-a4d06846-2e96-5963-9c28-7e6fed02fb0b.md` | `b79fa562a35b32a8b834b00266ee3bc0d6891229eb4eaabf70ee84821cc131ab` | `proposed` | Removed the inline citation and retained its even-exponent qualification as readable prose. No front-matter citation added. | `Tropp2022`, Theorem 8.2 and §8.5 |

## Evidence and unresolved issues

- Baseline text and `reference_links.inherited` were read from the pinned generated-object snapshots under `/tmp/nlalib-release-explorer/api/v1/editor/generated/`. All citations above were already inherited; none were duplicated in Markdown front matter.
- The link on “subspace embedding” targets the existing definition [Subspace embedding](/explore/statements/dd0c654f-b783-516b-b7c3-04b96f1a90f3/), which defines squared-norm distortion for a subspace and is compatible with the statement's constants `1 ± ε`.
- The existing Matrix norms definition page `/explore/statements/19646f49-e8db-5918-a0df-83eaf8db1648/` defines Schatten norms only for complex matrices. `schatten-duality` is stated over generic RCLike fields, and `schatten-even-moment-smoothness` allows real or complex matrices, so no field-incompatible link was added.
- `sampling-without-replacement-ose` does not define the row-sampling law in its body; the source signature requires a matrix with law `samplingSketchWithoutReplacement`. No separate exact definition page was found. `sampling-without-replacement-osi` includes a code-defined `samplingInjectionDim` placeholder and the term `\\alpha` from its literature comparison; their definitions/meaning are not supplied in the natural-language body. Clarify those only if self-contained prose is required; no formula or condition was invented.
- `sampling-without-replacement-ose` and `sampling-without-replacement-osi` are related row-sampling results but provide different guarantees (embedding versus injection), with separate identities and references. The two Schatten statements are also related but distinct (duality versus even-moment smoothness). No IDs were merged.
- No hypotheses, formulas, titles, result bindings, UUIDs or other front matter changed. No symbol-role registry additions proposed.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,322 equations; 0 errors).
- `git diff --check`: passed.
- Manifest UUIDs, actual inherited reference pairs, and staged-path scope: passed.
- Required staged content audit: passed ID, front-matter, kind, result binding, title/options and target-ID checks. It reports 88 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch.
- Preview/rendering was not run in this local source-only review.
