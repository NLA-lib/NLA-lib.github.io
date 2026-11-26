> Coordinator notice: this report covers the wrong assigned group, overlapping
> definitions04 part3. Its source changes are excluded; it adds no scope coverage.

# Luna research cohort 04 · part 3

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
formal evidence were checked against `/tmp/nlalib-release-explorer/api/v1/editor/objects/`;
inherited references were checked through the linked declaration records. No proposal
was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `33cd8a3d-4740-5cbd-82aa-7e67e7c152da` (`newton-schulz-sign-iteration-33cd8a3d`) | `f55ea43e3a3fd3543c37c7cb4e66434f2586d327c7c69a1dca6454391a5b4710` | `explore/content/statements/newton-schulz-sign-iteration-33cd8a3d.md` | `already-consistent` |
| `cdd691bb-6aef-5d59-b7e9-615785a98d27` (`nlalib-earlytruncatedgeneralizednystrom-cdd691bb`) | `5166146074d8853c6b2e1b968d9ae6549299566e5c49b7015d7022673683b945` | `explore/content/statements/nlalib-earlytruncatedgeneralizednystrom-cdd691bb.md` | `proposed` |
| `d1ee9b33-de78-5b4f-8a2d-d80147ea5587` (`nlalib-girardhutchinson-d1ee9b33`) | `84fb40c9183a2762085e89aa50dc0f75334173be131566052b039c4ab1df90b2` | `explore/content/statements/nlalib-girardhutchinson-d1ee9b33.md` | `already-consistent` |
| `21c93d07-2c81-555f-80b2-eff7e5316a67` (`nlalib-hessenbergreduction-21c93d07`) | `939dc6bc58f7fd886ddf04e8547300df0722548679067dcc5c39dd84a9aa5dbd` | `explore/content/statements/nlalib-hessenbergreduction-21c93d07.md` | `already-consistent`; similarity bound wording merits review |
| `b6d6ec43-d148-5545-bb84-195688281b33` (`nlalib-hutchpp-b6d6ec43`) | `d87997d384e7924ffead08a37e767f1d6c2c6bca2041908dc65516d109a51927` | `explore/content/statements/nlalib-hutchpp-b6d6ec43.md` | `proposed` |

## Changes and inherited references

- `nlalib-earlytruncatedgeneralizednystrom-cdd691bb`: changed sketch matrices from
  `\mathbf\Omega` and `\mathbf\Psi` to `\boldsymbol{\Omega}` and
  `\boldsymbol{\Psi}`. Linked the original phrase “rank-$k$ subspace” to the
  singular-value-decomposition definition at
  `/explore/statements/d5bca832-63a1-5043-ab6e-03b8402a2a55/`. The target defines
  leading singular-component truncation and is generic over real/complex matrices,
  matching the declaration's `RCLike` domain.
- `nlalib-hutchpp-b6d6ec43`: linked the existing phrase “Girard–Hutchinson estimate”
  to `/explore/statements/d1ee9b33-de78-5b4f-8a2d-d80147ea5587/`. The target is the
  same trace estimator over real or complex scalars, applied here to the residual
  matrix with fresh probes.
- `newton-schulz-sign-iteration-33cd8a3d`, `nlalib-girardhutchinson-d1ee9b33`, and
  `nlalib-hessenbergreduction-21c93d07` already use role-appropriate notation. No
  link was added to the authored Newton–Schulz definition: the nearby
  `NLAlib.signNewtonIterate` definition is the inverse-averaging update and explicitly
  distinguishes itself from this inverse-free Newton–Schulz update.
- Actual inherited citation pairs from linked declaration records:
  `newton-schulz-sign-iteration-33cd8a3d` — none (authored definition, no formal
  declaration); `nlalib-earlytruncatedgeneralizednystrom-cdd691bb` —
  `TroppYurtseverUdellCevher2017`, §7.3.1 and (7.3);
  `nlalib-girardhutchinson-d1ee9b33` — `Epperly2023`, “Girard–Hutchinson Estimator:
  The Basics”; `nlalib-hessenbergreduction-21c93d07` — `GolubVanLoan2013`,
  Algorithm 7.4.2; `nlalib-hutchpp-b6d6ec43` — `MeyerMuscoMuscoWoodruff2021`,
  Algorithms 1 and 3, and `EpperlyTroppWebber2024`, (1.3).
  `reference_links.inherited` is absent in this snapshot; each linked declaration's
  `record.references` was inspected. No citation was duplicated or moved inline.
- All IDs, UUIDs, definition kinds, declaration bindings, formulas, prose, and
  metadata were preserved apart from the stated font and link edits.

## Symbol-role registry proposals

The global registry was not edited. Suggested roles for later review:

- `newton-schulz-sign-iteration-33cd8a3d.md`: matrix `X` (and identity `I`).
- `nlalib-earlytruncatedgeneralizednystrom-cdd691bb.md`: matrices `A`, `Y`;
  Greek matrices `Ω`, `Ψ`.
- `nlalib-girardhutchinson-d1ee9b33.md`: matrix `A`, vectors `g`.
- `nlalib-hessenbergreduction-21c93d07.md`: matrices `A`, `Q`, `H`, `I`.
- `nlalib-hutchpp-b6d6ec43.md`: matrices `A`, `S`, `P`, `I`.

The current registry's examples cover Latin matrix/vector roles; Greek matrix-role
encoding should be reviewed before any registry update.

## Unresolved issues

- `nlalib-hessenbergreduction-21c93d07.md:8` says the construction uses `n-2`
  similarities and then states that for `n≤2` it returns `(I,A)`. Confirm whether
  the first clause is understood to apply only for `n>2`; no condition was added.
- No citation discrepancy, duplicate, or missing proof URL was found among these
  five entries. The four linked declarations have `admission_reported: false`.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after
editing. The notation check validates math parsing and registered notation roles,
not mathematical correctness. The SVD and trace-estimator definition targets were
checked against their Markdown and declaration domains. No rendered browser or
repeated-placement preview was available.
