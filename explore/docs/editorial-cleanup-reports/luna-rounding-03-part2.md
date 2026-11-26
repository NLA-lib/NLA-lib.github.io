# Luna rounding cohort 03 · part 2

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
evidence were checked in `/tmp/nlalib-release-explorer/api/v1/editor/objects/`.
No proposal was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `6de47ac7-7c9b-54be-ac7e-f83d8d458672` (`random-tape-6de47ac7`) | `89f6cf5f5dfa0a55c31ea02786f9b35f3ae714d4c030d76a99bdb826c053292c` | `explore/content/statements/random-tape-6de47ac7.md` | `already-consistent` |
| `b7eb3355-2d35-5924-915e-ad08d22c20cc` (`closed-and-manifest-work-b7eb3355`) | `f89fb9c2e6e2d91a60fb8200fd42537f81eae47827560d30bd457eb8e1782915` | `explore/content/statements/closed-and-manifest-work-b7eb3355.md` | `already-consistent` |
| `1b2b66d6-11bb-5c95-be41-014310fedb97` (`lanczos-scalar-rounded-operation-count-ritz-residual`) | `53331ac86e0fe65fd3ffc37e318f35f3ddc0dd3431cf3d543e5810b758915943` | `explore/content/statements/lanczos-scalar-rounded-operation-count-ritz-residual.md` | `proposed`; source/body scope merits review |
| `a9113600-2f7a-5cd9-a415-1e61064f8920` (`block-golub-kahan-forward-error`) | `e7e590e4794cbed124eaf37d17b6e935ca3e3260ccfbef742d7f6ec2fabd8d74` | `explore/content/statements/block-golub-kahan-forward-error.md` | `already-consistent`; source/body scope merits review |
| `744bc84b-2659-5cf7-9107-9cf1b628c872` (`block-golub-kahan-orthogonality`) | `bd007926822e59efa1edd5a3b5fc4bc848fa2018e16f0e687c82d73e495d3cec` | `explore/content/statements/block-golub-kahan-orthogonality.md` | `proposed`; source/body scope merits review |

## Changes and inherited references

- `lanczos-scalar-rounded-operation-count-ritz-residual.md`: braced `\mathbb{R}`
  and `\mathbf{0}`. Existing `\mathbf{T}_q` notation is already correct because
  the prose identifies it as the stored tridiagonal matrix; vector and matrix
  roles elsewhere are already bold.
- `block-golub-kahan-orthogonality.md`: linked the existing phrase “Gram defect on
  the support” to `/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/`.
  That definition explicitly sets `\mathbf{D}(\mathbf{Q})` to the Gram defect on
  the support. Its Lean declaration is for real matrices, matching the linked
  orthogonality theorem's real-matrix signature.
- The random-tape and closed/manifest-work entries are authored definitions without
  formal declarations. The Lanczos, block forward-error, and block orthogonality
  entries link to declarations `NLAlib.Krylov.Lanczos.Rounded.Stored.Certification.exec_scalarProgram_work_le_and_ritzResidual`,
  `NLAlib.IsBlockGolubKahanErr.frobNorm_sub_mul_transpose_mul_transpose_le`, and
  `NLAlib.IsBlockGolubKahanErr.frobNorm_gramDefect_left_le`, respectively. Their
  declaration records each have an empty `record.references` array. The definitions
  have no linked declaration and no inherited reference record. No citations were
  moved, added, or duplicated.
- No link was added for “tape” or “Ritz residuals”: the available tape entry defines
  a random tape and tape law, while the Lanczos theorem quantifies over every tape;
  the other Ritz entry is a related result, not a definition of the term. The
  orthogonal-projection target defines a projector using orthonormal columns, while
  the forward-error statement concerns a rounded computed basis, so it was not
  selected as a definition link.
- All IDs, UUIDs, theorem/definition kinds, result bindings, formulas, conditions,
  and metadata were preserved.

## Symbol-role registry proposals

The global registry was not edited. If expanded later, propose:

```json
"statements/lanczos-scalar-rounded-operation-count-ritz-residual.md": {"matrices": ["A", "T", "V"], "vectors": ["b", "v", "y"]},
"statements/block-golub-kahan-forward-error.md": {"matrices": ["A", "I", "P", "S", "U", "V"]},
"statements/block-golub-kahan-orthogonality.md": {"matrices": ["D", "U", "V"]}
```

The random-tape and work definitions contain no Latin vector/matrix symbols.

## Unresolved issues

- The Lanczos authored body describes the program and output but does not spell out
  the linked theorem's `Lanczos.Rounded.Output` relation or its dependent
  `Lanczos.Rounded.RitzResidual` property. Verify that “the values of a rounded
  Lanczos run” is intended to carry those source hypotheses. Formal source:
  `NLAlib/Krylov/Lanczos/Rounded/ScalarTheorem.lean:36–99`.
- The block forward-error statement does not state the full
  `IsBlockGolubKahanErr` relation between the input and returned factors, which is
  a formal premise in `NLAlib/Krylov/FinitePrecision/BandGolubKahanRun.lean:789–829`.
  Confirm whether “a rounded run” is sufficient reader-facing shorthand; do not
  insert the omitted relation without review.
- The block orthogonality statement likewise says the bases come from a rounded run
  but does not spell out the formal `IsBlockGolubKahanErr` premise
  (`BandGolubKahanRun.lean:496–512`). The exact Gram-defect definition is linked;
  the run hypothesis remains a mathematical/editorial review question.
- No unlinked inline citation or missing proof URL was found in these five bodies.

## Validation and limits

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked,
0 errors. `git diff --check` passed. The Gram-defect link was checked against its
Markdown definition and declaration field. No rendered browser or repeated-placement
preview was available; notation validation does not verify mathematical claims.
