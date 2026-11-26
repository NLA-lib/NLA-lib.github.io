# Luna research cohort 07, part 11

Scope: manifest `research[10]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements reviewed. This is an editorial review, not validation of the mathematics or the Lean correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited references |
| --- | --- | --- | --- | --- | --- |
| `69730256-680f-52ed-b25b-2c3d9a9198af` | `explore/content/statements/nyssi-gapless-error.md` | `0b6f7ff386934caf844e4709a3b453164c81df87f20f9a241eed9f58477d0c4c` | `needs-mathematical-review` | No source edits. | `TroppWebber2023`, Theorem 9.1 (NysSI) |
| `83eaf2e3-a5c0-5758-acdf-61e684bff986` | `explore/content/statements/nyssi-gapped-error.md` | `c148664f858bcc17a091f69d4b68d92f6d38ee0ca0311a1def4dd176c00f85a9` | `needs-mathematical-review` | No source edits. | `TroppWebber2023`, Theorem 9.2 (NysSI) |
| `2f994852-fd90-57d9-8eb6-b3c0d529793f` | `explore/content/statements/nystrom-bki-simulated-block.md` | `930709a8f4493523623e22206d366dfb5daa6bc3025caeb377347d66029544cd` | `proposed` | Replaced unbraced `\\mathbf\\Omega` with `\\boldsymbol{\\Omega}` at each occurrence to use explicit Greek matrix notation. | `ChenEpperlyMeyerMuscoRao2025`, Observation 3.3 |
| `f999f45d-a5f9-55fb-b592-dae1c50c70ab` | `explore/content/statements/randomized-nystrom-expected-error.md` | `0875dfd5db4d97b1e869f804919da1f479ef4020aaf389c038ebd8400c7f0595` | `proposed` | Replaced unbraced `\\mathbf\\Omega` with `\\boldsymbol{\\Omega}` in the Gaussian test-matrix symbol. | `TroppYurtseverUdellCevher2017a`, Theorem A.1; `TroppWebber2023`, Corollary 8.8 |
| `77274ec4-3d45-51a1-9390-7258d66c9efd` | `explore/content/statements/randomized-svd-expected-error.md` | `8e0533ca34c7d808d82b4bdb667b30aaee41de063ef7a78396608465ddbd5081` | `proposed` | Replaced unbraced `\\mathbf\\Omega` with `\\boldsymbol{\\Omega}` in the Gaussian test-matrix symbol and projection subscript. | `HalkoMartinssonTropp2011`, Theorem 10.5 (twice in record); `TroppWebber2023`, Theorem 8.7 |

## Evidence and unresolved issues

- Inherited references were verified through each editor object's `evidence.declaration` and the linked declaration's `record.references`; the exact key/locator pairs are listed above. The editor objects' authored `references` arrays are empty. No duplicate front-matter citations were added; the associations remain attached to the statements and render through their linked declarations.
- The two Nyström subspace-iteration error statements omit source hypotheses. In `NLAlib/LowRank/Gaussian/NystromBlockKrylov.lean`, the gapped declaration's docstring at lines 172–178 describes positive semidefinite input and a standard Gaussian test matrix; the linked theorem at lines 185–188 takes `hH : H.PosSemidef` and `hX : HasLaw X (gaussianMatrix n l) μ`. The gapless declaration's docstring at lines 247–253 and theorem at lines 307–311 likewise require PSD input and the Gaussian law. These hypotheses are absent from the assigned readable statements. Confirm the intended statement scope before changing them.
- No direct, scope-compatible definition page for the Nyström methods or gap quantities was verified. No links were added. No symbol-role registry additions proposed.
- No formulas, assumptions, delimiter segmentation, titles, bindings, IDs or metadata changed. The three `\\Omega` changes alter only font notation.

## Citation record correction

The first report version incorrectly inferred that empty authored object references meant no inherited references. This correction commit records the actual linked declaration citation pairs above. No statement source was changed in this correction.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed the ID, front-matter, kind, binding, title and target-ID checks. It reports 78 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch. The three edited statements are not flagged.
- Preview/rendering was not run in this local source-only review.
## Authoritative inherited citation record audit

This audit resolves each entry through the pinned editor object’s `evidence.declaration` and the corresponding declaration `record.references`. It supersedes any earlier statement that treated an empty authored `object.references` array as proof of no inherited references. The pairs below are already attached through the declaration and were not duplicated in front matter.

| UUID | Linked declaration | Inherited key/locator pairs |
| --- | --- | --- |
| `69730256-680f-52ed-b25b-2c3d9a9198af` | `Matrix.PosSemidef.integral_specNorm_sub_nystrom_pow_mul_le_mul_rpow_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, Theorem 9.1 (NysSI) |
| `83eaf2e3-a5c0-5758-acdf-61e684bff986` | `Matrix.PosSemidef.integral_specNorm_sub_nystrom_pow_mul_le_singularGapRatio_of_hasLaw_gaussianMatrix` | `TroppWebber2023`, Theorem 9.2 (NysSI) |
| `2f994852-fd90-57d9-8eb6-b3c0d529793f` | `Matrix.PosSemidef.nystromBKI_blockKrylovMatrix` | `ChenEpperlyMeyerMuscoRao2025`, Observation 3.3 |
| `f999f45d-a5f9-55fb-b592-dae1c50c70ab` | `Matrix.PosSemidef.integral_nuclearNorm_sub_nystrom_le_of_hasLaw_gaussianMatrix` | `TroppYurtseverUdellCevher2017a`, Theorem A.1; `TroppWebber2023`, Corollary 8.8 |
| `77274ec4-3d45-51a1-9390-7258d66c9efd` | `NLAlib.integral_frobNorm_sub_rsvd_sq_le_of_hasLaw_gaussianMatrix` | `HalkoMartinssonTropp2011`, Theorem 10.5; `TroppWebber2023`, Theorem 8.7; `HalkoMartinssonTropp2011`, Theorem 10.5 |
