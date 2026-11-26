# Luna research cohort 07, part 13

Scope: manifest `research[12]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements reviewed. This editorial review does not validate the mathematical claims or their formal correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited key/locator pairs |
| --- | --- | --- | --- | --- | --- |
| `1d855d8f-f49a-5243-9071-144b23a999ad` | `explore/content/statements/rbki-simulated-block.md` | `b6c336cc6baaa38de9abda76e0128198796d5c8b3db6d8c53dcb15bcdab9ad5c` | `proposed` | Replaced unbraced `\\mathbf\\Omega` with `\\boldsymbol{\\Omega}` throughout. | `MeyerMuscoMusco2023`, §3.1; `ChenEpperlyMeyerMuscoRao2025`, Observation 3.3 |
| `023fc92c-a7f4-5544-8eaf-7774ad5ced2f` | `explore/content/statements/rbki-single-vector-gapless-error.md` | `dc8791a00b22ba9a49d61f920f18cb7589f762167dbeb2f4ff61eada6f37156c` | `needs-mathematical-review` | No source edits. | `MeyerMuscoMusco2023`, Theorem 1 |
| `6465b959-693e-56a3-8315-d53e6f666abd` | `explore/content/statements/rsi-gapless-error.md` | `85eb70f6586af2ec780bc42f364c2d69538da066734426679d5dc3fc74c2823b` | `needs-mathematical-review` | No source edits. | `TroppWebber2023`, Theorem 9.1 (RSI); `HalkoMartinssonTropp2011`, Proposition 8.6 |
| `6d8bbd02-a064-5571-b084-98e3cfe2ee2d` | `explore/content/statements/rsi-gapped-error.md` | `230e93b4a0ddaac2057563efc1e447deb29c86b3ff72ec2eb9d504839958f6f0` | `needs-mathematical-review` | No source edits. | `TroppWebber2023`, Theorem 9.2 (RSI) |
| `806dec5b-0402-5070-b77e-7e1cb8ddef57` | `explore/content/statements/shifted-qr-rounded-schur-any-leaf.md` | `e9d71021e8956862389747407e77f71d98bc75ede00767e5c65127cf1a118f2d` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2022`, Theorem 6.3 (two record entries) |

## Evidence and unresolved issues

- Inherited citations were checked through each editor object's `evidence.declaration` and the corresponding declaration `record.references`. The pairs above are already attached and rendered; the objects' authored `references` arrays are empty, so no citation front matter was added.
- `rbki-single-vector-gapless-error` supplies a standard real Gaussian start vector but leaves the field of `\\mathbf{A}` unstated. The pinned source `NLAlib/LowRank/Gaussian/SmallBlock.lean` docstring at lines 966–982 and theorem at lines 984 onward specify a real matrix. Clarify the intended readable scope before making a source edit.
- `rsi-gapless-error` and `rsi-gapped-error` omit the real-matrix domain and standard Gaussian law on `\\mathbf{X}` present in the source docstrings and declaration signatures. In `NLAlib/LowRank/Gaussian/BlockKrylovGapless.lean` the gapless RSI declaration takes `A : Matrix m n ℝ` and `hX : HasLaw X (gaussianMatrix n l) μ`; `NLAlib/LowRank/Gaussian/BlockKrylov.lean` has the corresponding gapped RSI assumptions. The hypotheses were not inserted by inference.
- `shifted-qr-rounded-schur-any-leaf` depends on “machine and sampler as above,” several parameter ranges “above,” and the “Shape of the guarantee” above. The standalone statement does not carry those referenced definitions/context. Preserve this and clarify the intended surrounding source rather than reconstructing assumptions from another declaration.
- No direct, scope-compatible definition page was verified for RBKI, RSI or the shifted-QR contracts. No links were added. No symbol-role registry additions proposed.
- The three iterative SVD/RBKI/RSI error statements are related variants but have distinct result IDs, algorithms and parameter regimes; no entries were merged. The RBKI and Nyström BKI simulated-block statements are also distinct algorithm families.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed ID, front-matter, kind, binding, title and target-ID checks. It reports 81 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch. The edited RBKI statement is not flagged.
- Preview/rendering was not run in this local source-only review.
