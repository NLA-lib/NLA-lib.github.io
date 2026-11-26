# Luna rounding cohort 03 · part 1

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
evidence were checked in `/tmp/nlalib-release-explorer/api/v1/editor/objects/`.
All five entries are authored definitions with no formal declaration. Their
`reference_links.inherited` field is absent; there is no linked declaration record
from which inherited references could be supplied. No citation was moved, added,
or duplicated. No proposal was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `293c93c0-109c-5fc6-b2df-49f56a960c23` (`relative-error-and-absolute-error-floor-293c93c0`) | `3275066abd61eccbb1dd42796449302ab82ec7dbd3f95e336c5df05795a41cff` | `explore/content/statements/relative-error-and-absolute-error-floor-293c93c0.md` | `already-consistent` |
| `5bd8642a-3621-59ba-b33e-e63b422d2803` (`relative-error-blas-matvec-5bd8642a`) | `38854835a6bf8dd098c92260bbf281b38f4d0b46678187e7bc5a2a127630e144` | `explore/content/statements/relative-error-blas-matvec-5bd8642a.md` | `proposed` |
| `3bd3e996-91bc-59ca-a0ac-fb32de488886` (`exact-arithmetic-3bd3e996`) | `d8d928cd0694a27c7baac80351ade8b2b3ba495bcd6979e216325b850713796e` | `explore/content/statements/exact-arithmetic-3bd3e996.md` | `already-consistent` |
| `e571c120-4ca1-5f41-ab7a-d718b5a59289` (`uniform-model-and-oracle-e571c120`) | `c857f8d4ec1f76714d4a0aa1c04408c65b872583a9e3140a84170fd79ebfea14` | `explore/content/statements/uniform-model-and-oracle-e571c120.md` | `already-consistent` |
| `e4a4357b-8f1b-5f40-b418-ed1b6bbfa79a` (`accuracy-budgets-e4a4357b`) | `0e83c4fa5cb7e17c1d2b313ff5031c4f82f2ed218ebf2c7aab94fb3b033f1252` | `explore/content/statements/accuracy-budgets-e4a4357b.md` | `already-consistent` |

## Changes

- In `relative-error-blas-matvec-5bd8642a.md`, changed vector component notation from
  `x_i`, `y_i`, `z_i` to `\mathbf{x}_i`, `\mathbf{y}_i`, `\mathbf{z}_i`, including
  the hatted output, while keeping the vector indices outside the bold arguments.
  Scalar `\alpha`, error coefficients, dimensions, expressions, and inline/display
  segmentation were preserved.
- The other four entries already use appropriate scalar/font roles. Unit roundoff,
  error floors, budgets and coefficients remain scalar. No formulas or prose were
  rewritten.
- No exact existing definition target was useful in these definitions without
  adding a new clause, linking a term to itself, or pointing at a related but
  different concept. No definition links were added.
- IDs, UUIDs, kinds, formulas, conditions, front matter and provenance were retained.

## Symbol-role registry proposal

The global registry was not edited. If these documents are added to it later,
propose only this entry:

```json
"statements/relative-error-blas-matvec-5bd8642a.md": {"matrices": ["A"], "vectors": ["x", "y", "z", "v"]}
```

Here `\mathbf{A}` and `\mathbf{v}` occur in the matvec bound; `\mathbf{x}`,
`\mathbf{y}`, and `\mathbf{z}` are the dot-product and vector-addition operands.
The other assigned entries contain no vector/matrix roles to register.

## Unresolved issues

- `relative-error-blas-matvec-5bd8642a.md` leaves the scalar field and inner-product
  convention implicit. The batch preserves that formulation; if real/complex scope
  needs to be explicit, resolve it as a mathematical review rather than infer it
  from capitalization or the error bound.
- No duplicate, broken definition link, citation conflict, or unsupported math
  command was found in the assigned files.

## Validation and limits

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked,
0 errors. `git diff --check` passed. No rendered browser or repeated-placement
preview was available; this notation check does not verify the mathematics.
