# Luna rounding cohort 03 · part 3

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions,
evidence and inherited citations were checked in `/tmp/nlalib-release-explorer/api/v1/editor/objects/`
and the corresponding declaration records. No proposal was submitted; this is a
local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `b5af9bf0-05f0-5bd0-a29b-b8f4e5d279ea` (`block-golub-kahan-residual`) | `099a9bb4ee1b818724bf4c94465fe209e81d8a847f5ec151fdd94bd4ff7db0cd` | `explore/content/statements/block-golub-kahan-residual.md` | `proposed`; run relation is implicit |
| `30ae638f-d7d8-5b6c-91f0-65d57ae2c0de` (`block-golub-kahan-band-structure`) | `98724cc51a0e7fffc82b2383d7b9c7190e5e852e5316875553c91d890a80dd06` | `explore/content/statements/block-golub-kahan-band-structure.md` | `proposed` |
| `38da53a6-399c-573c-8a5f-af35c80fc1e3` (`block-golub-kahan-existence`) | `6b90b34994ee0a3cbe01c497f97bafcda0e3613023afc4a7bbcaa3e77870c300` | `explore/content/statements/block-golub-kahan-existence.md` | `proposed` |
| `4acf79f1-542a-5cb1-ad06-82ac78de683b` (`block-golub-kahan-factored-output`) | `f73729c5d08e8008dac0b68efd66863662c1f0a1bf5973f43746b87370c81f1b` | `explore/content/statements/block-golub-kahan-factored-output.md` | `proposed` |
| `cb17877c-5b47-5eee-848b-379ce1751a61` (`dense-schur-eigenvalues`) | `23799c10505b30b7ec981704a629adbf1ba40c888e175550ac0d37358924ed42` | `explore/content/statements/dense-schur-eigenvalues.md` | `proposed` |

## Changes and inherited references

- `block-golub-kahan-residual`: linked the existing phrase “rounded run” to the
  `IsBlockGolubKahanErr` definition at
  `/explore/statements/593daa98-8a52-5a89-a792-f46844fd76d6/`. Its definition and
  the linked residual theorem both use real matrices.
- `block-golub-kahan-band-structure` and `block-golub-kahan-existence`: linked the
  original phrase “exact run” to the generic real/complex `IsBlockGolubKahan`
  definition at `/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/`.
  Bolded matrix entries `R_{ic}` and `S_{ic}` as `\mathbf{R}_{ic}` and
  `\mathbf{S}_{ic}` in the band conditions.
- `block-golub-kahan-existence` and `block-golub-kahan-factored-output`: changed
  Greek matrix notation from `\mathbf\Omega` to `\boldsymbol{\Omega}`. In the
  factored-output statement, linked the original phrase “projection of
  \(\mathbf{A}\) onto the range” to the `NLAlib.rbki` definition at
  `/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/`, which defines that
  approximation over real or complex scalars.
- `dense-schur-eigenvalues`: linked “dense Schur theorem” to the exact theorem
  entry at `/explore/statements/9fd58d97-e831-5cb7-9bf8-24b035ded4c6/`. Both source
  statements concern complex input matrices.
- Actual inherited reference pairs from the linked declaration records:
  `block-golub-kahan-residual` — none;
  `block-golub-kahan-band-structure` — none;
  `block-golub-kahan-existence` — none;
  `block-golub-kahan-factored-output` — none;
  `dense-schur-eigenvalues` — `BanksGarzaVargasSrivastava2022`, Theorem 1.4;
  `BanksGarzaVargasSrivastava2025`, Theorem 1.1. `reference_links.inherited` was
  absent in this snapshot, so each linked declaration's `record.references` was
  inspected. No citations were copied into authored front matter.
- All UUIDs, IDs, theorem kinds, result bindings, formulas, hypotheses and existing
  metadata were retained. Inline/display math segmentation is unchanged.

## Symbol-role registry proposals

The global registry was not edited. Proposed roles for a later registry review:

Proposed Latin roles: `block-golub-kahan-residual.md` matrices `A,R,S,U,V`;
`block-golub-kahan-band-structure.md` matrices `R,S`;
`block-golub-kahan-existence.md` matrices `A,R_0,R,S,U,V`;
`block-golub-kahan-factored-output.md` matrices `A,S,U,V`;
`dense-schur-eigenvalues.md` matrices `A,E,T`. The existence and factored-output
entries also use `\boldsymbol{\Omega}` as a Greek matrix; the shared registry's
current examples cover only Latin roles, so its encoding should be reviewed before
adding this Greek role.

These proposals reflect the displayed objects and their source signatures; they
were not added to `explore/notation.json`.

## Unresolved issues

- `block-golub-kahan-residual.md:8–12` says “a rounded run” without spelling out
  the full `IsBlockGolubKahanErr` premise that the linked Lean theorem requires
  (`NLAlib/Krylov/FinitePrecision/BandGolubKahanRun.lean:653–685`). The exact run
  definition link identifies the relevant relation; confirm whether that shorthand
  is sufficient for a standalone theorem statement.
- `dense-schur-eigenvalues.md:8` refers to the hypotheses of the linked main theorem
  rather than repeating them. The direct link supplies context, but verify that this
  cross-reference is accepted as the intended standalone presentation. No hypotheses
  were added or inferred.
- No citation discrepancy or unresolved symbol role was found. The linked block
  Golub–Kahan definitions have field domains matching their respective real or
  generic real/complex statements; the Schur result link targets the complex case.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after
editing. The notation check validates math parsing and declared notation roles, not
mathematical correctness. Definition/result targets were checked against their
Markdown content and declaration signatures. No rendered browser or
repeated-placement preview was available.
