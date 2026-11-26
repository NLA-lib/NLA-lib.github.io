# Luna generated research cohort 08, part 7

Scope: exactly `research[6]` from `/tmp/nla-luna-cohort-08.json`. Baseline revisions, source text and actual inherited references were inspected in the pinned generated objects.

| UUID | Result | Source path | Baseline revision | Outcome | Editorial change | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `eac223be-0768-54e1-803e-7d2236ab7fda` | `sketch-and-precondition-convergence` | `explore/content/statements/entry-eac223be-0768-54e1-803e-7d2236ab7fda.md` | `bd0047f0c71a6d2b573fccf535b02c740e235b7ccb3b248edecbc69d2eae899a` | `proposed` | Removed two inline citation markers. Kept the residual-bound and conditioning qualifications, distinguishing the first and second cited results. Math fonts already matched object roles. | `MartinssonTropp2020`, §10.5; `EpperlyMeierNakatsukasa2024`, Fact 2.2 |
| `de798c5d-2e88-57bb-9343-65f30c7b915b` | `sketch-and-precondition-ls` | `explore/content/statements/entry-de798c5d-2e88-57bb-9343-65f30c7b915b.md` | `6284ca32a864fddc5747b5bd87ff94f1f9ec62d13c69df8d3952f2af23ec490f` | `proposed` | Removed inline citation marker; retained the stated contrast with the unsquared bound. Notation unchanged. | `MartinssonTropp2020`, §10.5 |
| `65af7594-ed4f-5ae9-93e2-6c8ddf8141b7` | `sketch-and-precondition-realisation` | `explore/content/statements/entry-65af7594-ed4f-5ae9-93e2-6c8ddf8141b7.md` | `a94d4b53a5e2a27219dcc7127fcb86fdfa22c2e48e3093b255401bccdd29da40` | `proposed` | Removed inline citation and changed its attached “there for” phrase to “For the cited case” to preserve the model qualification without a dangling antecedent. | `EpperlyMeierNakatsukasa2024`, §2.1 |
| `122f4300-7a23-5007-9a91-425f0b399816` | `sketch-and-project` | `explore/content/statements/entry-122f4300-7a23-5007-9a91-425f0b399816.md` | `08e71ef1c0b2dffe8216389a26b9fc6ccc93bdfc8ee297a7052a454a48f1c89e` | `proposed` | Removed inline citation marker. The precise Lean theorem identifier remains as supplied; notation unchanged. | `GowerRichtarik2015`, Theorem 4.6 |
| `faa9a467-a3b4-508c-9446-0f246057405a` | `sketch-and-solve-error-decomposition` | `explore/content/statements/entry-faa9a467-a3b4-508c-9446-0f246057405a.md` | `be573cdd446fd2fed97a20d4991badcb3805fe2c1af16374dbe39a5096012803` | `needs-mathematical-review` | Removed the two inline citation markers and retained the complement-frame comparison in prose. Notation unchanged. | `TroppYurtseverUdellCevher2017`, Lemma A.4; `CamanoEpperlyMeyerTropp2025`, Lemma 2.6 |

The inherited citation pairs above come from `reference_links.inherited`, not from authored `object.references`. No new citation metadata was added. No definition links were added; no precise compatible definition target was verified for the concepts needing links. All source formulas, assumptions, identities, titles, theorem bindings and front matter were retained. No symbol-role registry additions proposed.

## Unresolved issues

- The error-decomposition prose says that the cited comparison uses a complement frame, but does not make clear whether that qualification applies to Lemma A.4, Lemma 2.6, or both. The source's two inherited associations are preserved; the exact attribution needs confirmation.
- In the first statement the existing prose distinguishes a residual bound from the conditioning source. Those distinctions are retained through “first cited result” and “second”; no stronger mathematical comparison is intended.
- No mathematical correctness review or rendering preview was performed.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,546 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit and manifest UUID/staged-path checks: passed.
