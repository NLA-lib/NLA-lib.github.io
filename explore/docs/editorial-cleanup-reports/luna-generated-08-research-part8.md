# Luna generated research cohort 08, part 8

Scope: exactly `research[7]` from `/tmp/nla-luna-cohort-08.json`. Baseline revisions and inherited reference pairs were read from the pinned generated objects.

| UUID | Result | Source path | Baseline revision | Outcome | Edit | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `4d1b1b67-3584-59da-afa2-88e28edb2386` | `sketch-and-solve-expected-error` | `explore/content/statements/entry-4d1b1b67-3584-59da-afa2-88e28edb2386.md` | `90cd12bf241e737ddc608be4a51983df3dfc55540d42a8b12645fa9b3446ff56` | `proposed` | Removed inline citation marker; retained the real-Gaussian identity qualification and described its role in the sufficient-size corollary. | `EpperlyWebber2026`, Theorem 2.1 and §2.1 |
| `819cba98-32b4-5c5b-923a-ad88bfe9e2cd` | `sketch-and-solve-lower-bound` | `explore/content/statements/entry-819cba98-32b4-5c5b-923a-ad88bfe9e2cd.md` | `be663f7445d599a5a3fa9396453d8d678fc57fb53370bbbf4286e010fbdd0a4f` | `proposed` | Removed inline citation marker; retained that the cited result is a supremum over problems of rank $r$. | `EpperlyWebber2026`, Theorem 2.2 |
| `b3f87cd3-8025-5d33-84b4-336a93096955` | `sketch-and-solve-ls` | `explore/content/statements/entry-b3f87cd3-8025-5d33-84b4-336a93096955.md` | `c060000d6b6744a5a20a58e151e665d3c09db2758b9841efc5a2841e50cae8a7` | `proposed` | Removed inline citation marker; retained the injection-plus-multiplication route, Gaussian second JL moment, and squared-residual qualification. | `Woodruff2014`, proof of Theorem 23 |
| `e962a3b2-c298-5787-98e1-6894fca5f05c` | `sparse-ose` | `explore/content/statements/entry-e962a3b2-c298-5787-98e1-6894fca5f05c.md` | `dbf64ceeafadca0af20e89e665ba2a83493035d05b566af065744a40f847cf4c` | `proposed` | Removed the inline citation marker and retained the comparison to the cited theorem and the distinct proof routes/constant qualifications. | `Woodruff2014`, Theorem 9 |
| `359849ef-b85d-5023-8dc4-9b11f8ec250e` | `sparse-pcp` | `explore/content/statements/entry-359849ef-b85d-5023-8dc4-9b11f8ec250e.md` | `91a0adc9d0c30fcd3295a42b921a2038b3f5bfb7b339c9f16373f8213267367c` | `proposed` | Removed inline citation marker. | `CohenElderMuscoMuscoPersu2015`, Theorem 12, Lemma 11, family 2 |

The exact inherited pairs are taken from each generated object's `reference_links.inherited`; no new citation metadata was authored. Vector and matrix fonts and transpose conventions were already consistent. No definition links were added because no precise scope-compatible existing target was verified. Formulas, conditions, titles, IDs, result bindings and front matter are preserved.

## Unresolved issues

- `sparse-ose` preserves the source's discussion of second-moment work by Meng and Mahoney and Nelson and Nguyen and explicitly does not attribute its constant to those works; no separate references for them were present in the inherited associations. The prose remains as supplied apart from removal of the Woodruff citation marker. A bibliography/reference review would be needed to add any further associations.
- No mathematical audit or preview/rendering was performed.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,589 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit and manifest UUID/staged-path checks: passed.
