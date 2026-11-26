# Luna research cohort 04 · part 1

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
formal evidence were checked against `/tmp/nlalib-release-explorer/api/v1/editor/objects/`;
inherited references were checked through each linked declaration record. No proposal
was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `3f4f0fa3-7a5c-5871-83e4-2b9fceb23147` (`cgs2-basis-extension-error`) | `c1a621e702f709fce370c96f32e55b9284702f45e670cfa4e2da3d97a026d2d4` | `explore/content/statements/cgs2-basis-extension-error.md` | `proposed` |
| `501be497-13e8-5f2d-b5bc-aeb5ccee7c75` (`cgs2-basis-extension`) | `e2430ea84e538bc561db2d603ec5de69b666e0d71570331723e890d47827b68a` | `explore/content/statements/cgs2-basis-extension.md` | `proposed` |
| `2ddefe08-7b63-50a0-a85b-a0d1f4e05a14` (`cholesky-backward-error`) | `76cb247e57915b91314c1258c0e43f4da918c1a27981825500a834e7ef2cfd09` | `explore/content/statements/cholesky-backward-error.md` | `already-consistent`; source notation merits review |
| `73049bd9-26db-573c-bb15-c64708b469fb` (`cholesky-existence`) | `b6849b65c587f48893874cdbf7362511632201ea3df83ffab47034bdcaa3700c` | `explore/content/statements/cholesky-existence.md` | `proposed`; field/index scope merits review |
| `257222e6-7828-5cbd-82ba-e05f7e257514` (`countsketch-second-moment`) | `4081c439871029691f0fb5537d0ca6f8a6427e13aa4408293155fbca0a1349e2` | `explore/content/statements/countsketch-second-moment.md` | `proposed` |

## Changes and inherited references

- `cgs2-basis-extension-error`: bolded the matrix entries `r_{cc}` as
  `\mathbf{R}_{cc}` and braced `\mathbf{0}`. Linked “rounded extension” to
  `/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/`; its definition is
  real-matrix-valued, matching this theorem.
- `cgs2-basis-extension`: braced `\mathbf{0}` and linked “exact extension” to
  `/explore/statements/12a7ec72-6c64-59e6-b7de-7aff8d055ba2/`. Its formal
  definition supports real or complex matrices, matching the theorem's stated
  domain.
- `cholesky-backward-error`: no notation edit was needed. Its declaration record
  inherits `Higham2002`, Theorems 10.3 and 10.7; this association was retained and
  not duplicated in front matter.
- `cholesky-existence`: linked “Cholesky factor” to the existing factorization
  definition at `/explore/statements/d00946c1-7d12-50e4-a6da-635456a9fca7/`.
  The target defines the lower-factor form with positive real diagonal for Hermitian
  positive-definite matrices and supports the theorem's real/complex field.
- `countsketch-second-moment`: braced `\mathbb{R}` and `\mathbb{E}`; linked
  “CountSketch” to its generic real/complex definition at
  `/explore/statements/161d8fd6-2f0a-5e7e-8b4c-e7e67c1e6289/`.
- Actual inherited references from linked declaration records: `cgs2-basis-extension-error` — none;
  `cgs2-basis-extension` — none; `cholesky-backward-error` — `Higham2002`,
  Theorems 10.3 and 10.7; `cholesky-existence` — none; `countsketch-second-moment` —
  none. `reference_links.inherited` is absent in this snapshot, so the declaration
  records were checked directly. No inline bibliography citation was moved.
- The two CGS2 statements are related but distinct: one converts per-column rounded
  guarantees into the rounded-extension contract over reals; the other establishes
  an exact extension after two passes over real or complex scalars. Their IDs and
  separate bindings remain intact.
- All titles, UUIDs, IDs, result bindings, kinds, formulas, delimiter segmentation,
  conditions and other metadata were preserved.

## Symbol-role registry proposals

The global registry was not edited. For later review, the symbol roles are:

- `cgs2-basis-extension-error.md`: matrices `Q`, `W`, `W'`, `Q'`, `H`, `R`, `V`;
  vectors `w`, `q`, `h`.
- `cgs2-basis-extension.md`: matrices `Q`, `W`, `Q'`, `H_1`, `H_2`, `R_1`,
  `R_2`, `W_1`, `W_2`, `D`; vector `w`.
- `cholesky-backward-error.md`: matrices `A`, `L`.
- `countsketch-second-moment.md`: matrices `U`, `S`.
- `cholesky-existence.md` contains no displayed Latin matrix/vector symbols.

## Unresolved issues

- `cholesky-backward-error.md:8–10` writes `\kappa_2(\mathbf{A})`; the linked
  theorem signature uses `pseudoConditionNumber A`. Confirm that this notation is
  the intended specialization for the stated positive-definite real matrix. The
  formal source is `NLAlib/Matrix/FinitePrecision/CholeskyRoundingError.lean:800–843`.
- `cholesky-existence.md:8` leaves the scalar field and finite linearly ordered
  index type implicit, while the linked declaration is over `RCLike` scalars and a
  finite linearly ordered index type (`NLAlib/Matrix/Factorizations/Cholesky.lean:416–426`).
  Confirm whether the broad prose is intended; no domain restriction was added.
- The CountSketch statement is explicitly the real specialization of the checked
  real-or-complex identity; that scope distinction was preserved.
- No possible duplicate entries were found within this batch.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after
editing. The notation check validates math parsing and registered notation roles,
not theorem correctness. Definition targets and field domains were checked against
their Markdown and declaration signatures. No rendered browser or
repeated-placement preview was available.
