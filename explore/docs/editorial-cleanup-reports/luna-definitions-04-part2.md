# Luna matrix definitions cohort 04, part 2

This report covers only the second five files in the assigned matrix cohort. Baseline revisions, evidence and reference associations were read from the pinned release Explorer editor objects at `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`. Every assigned object is an authored definition with `object.references: []` and `reference_links: null`, without a Lean declaration binding. No inherited declaration citations or inline bibliographic strings apply to the five assigned bodies.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `08c095ab-87a1-5868-9d7c-58a93e407feb` | `explore/content/statements/late-truncated-gn-08c095ab.md` | `108c1cbb0a645c222b632becb8f237e6684e785b97bfda89dc2dd0ddb4728741` | `proposed` |
| `9762adf8-8884-5899-b695-2aa9850f0186` | `explore/content/statements/late-truncated-nystr-m-block-krylov-iteration-9762adf8.md` | `cf163e8fbd978e58dea82f7204f9ae7137f53ada81c5475f04425aebecd10b38` | `proposed` |
| `21bd0b0f-4c55-5413-bc01-5a13cb925690` | `explore/content/statements/late-truncated-nystr-m-subspace-iteration-21bd0b0f.md` | `b55e283ea6a45d8423cbfe0bfd7cffd7f33a5131af2131c1f936ac5238023184` | `proposed` |
| `100d7ac0-44b3-5c2a-8737-9d2b4faad068` | `explore/content/statements/late-truncated-rbki-100d7ac0.md` | `4e5abb2be155497770540403bcd08f67b16ed152cd6246e0831c2985e722abd5` | `proposed` |
| `c87bfc3a-e18e-553a-90a0-c82558421a6d` | `explore/content/statements/late-truncated-rsi-c87bfc3a.md` | `c979a7677e5d0afaffa3da9119ef3a5625177cdf37ec1784c35799d4a96e80f0` | `proposed` |

## Changes and links

- **Late-truncated GN**: changed Greek matrix symbols `\mathbf\Omega` and `\mathbf\Psi` to `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}`. Linked the existing phrase “best rank-at-most-$k$ approximation” to the truncated-SVD definition, UUID `22476dc5-4a8c-59f3-95a5-929740cd4e5b`, which defines the leading-singular-value truncation and rank bound used by `[..]_k`. The generalized Nyström formula and output statement are otherwise unchanged.
- **Late-truncated Nyström block Krylov iteration**: changed `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing “rank-$r$ truncated singular-value decomposition” phrase to UUID `22476dc5-4a8c-59f3-95a5-929740cd4e5b`. Its positive-semidefinite Hermitian hypothesis and formula are unchanged.
- **Late-truncated Nyström subspace iteration**: changed both occurrences of `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing truncated-SVD phrase to UUID `22476dc5-4a8c-59f3-95a5-929740cd4e5b`. The power and Nyström formulas remain exactly as stated.
- **Late-truncated RBKI**: changed `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing truncated-SVD phrase to the same specific definition. The block-width rank bound and output rank remain unchanged.
- **Late-truncated RSI**: changed both occurrences of `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing truncated-SVD phrase to the same definition. The adjoint, rank bounds, and output remain unchanged.

The target's pinned declaration `NLAlib.truncatedSVD` accepts `[RCLike 𝕜]` and rectangular matrices, so it is compatible with the real/complex and rectangular contexts here. That target itself has an inherited `GolubVanLoan2013`, edition 4, Theorem 2.4.8 citation. This association remains on the target; no citation was copied to any assigned object. Every assigned editor object has empty authored `object.references` and no declaration evidence, so none has inherited declaration references. No inline bibliographic strings occurred in the assigned bodies; no citations were relocated or added.

## Validation

Verified the target Markdown UUID and its formal declaration scope. All Greek sketch symbols bolded here are matrices; scalar indices and powers remain outside the bold arguments. Added links preserve existing wording, and the inline/display math delimiters and expressions were retained. No field restrictions, hypotheses, identities, output claims, IDs, kinds, provenance or review metadata were changed. No helper content was expanded.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

Consider reviewed matrix-role entries for `\Omega` and `\Psi` in these files if the notation registry owner expands coverage. No global registry change was made.
