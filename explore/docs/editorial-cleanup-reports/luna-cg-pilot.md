# Luna CG editorial cleanup pilot

Source: pinned Explorer snapshot `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`.
Baseline revisions and evidence are from `/tmp/nlalib-release-explorer/api/v1/editor/objects/{UUID}.json`.
No proposal was submitted; this local batch is committed for review only.

| UUID / statement | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `de598675-e038-5a75-a6b5-f471cab1156a` (`cg-optimality`) | `d6fa9fa822e0059a2ecf66a569b7552cfa56cd1f56345e96ab3c67b75dc7fef0` | `explore/content/statements/cg-optimality.md` | `proposed`; needs mathematical review of standalone assumptions |
| `aa1d5b60-6ec3-58e0-9168-e25e60a9d5a7` (`cg-polynomial-bound`) | `89faafc4df0c245572f2e7a460cb345596725bbec9494a1e1f29c779fa5cae83` | `explore/content/statements/cg-polynomial-bound.md` | `proposed`; needs mathematical review of standalone assumptions |
| `845426ae-8454-5066-81fd-41b93a3e12c0` (`cg-chebyshev-bound`) | `3d009691cb6d00a479389293af7d1ccd5b3c38b41b2d92ae2f624328e6b9499a` | `explore/content/statements/cg-chebyshev-bound.md` | `proposed`; needs mathematical review of standalone assumptions |
| `7cff0d5e-11c8-51c3-8620-0c3b8dc915fe` (`cg-finite-termination`) | `dad72771132dcbb4c2cff9f672ccef78e7920379ddf251c27084246056697d74` | `explore/content/statements/cg-finite-termination.md` | `proposed`; needs mathematical review of standalone assumptions |

## Edits

- `cg-optimality`: linked the first occurrence of “Krylov space” to its definition at `/explore/statements/615008ca-f5db-5cff-ab6b-b07f178cbd05/`. Its citations are inherited from the declaration record and were not added to front matter.
- `cg-polynomial-bound`: consistently bolded Latin vectors and matrix in both formulas. Kept the original explanation; left “polynomial” unlinked because the existing definition concerns evaluating a polynomial on a matrix, not the scalar polynomial term used here. Its citation is inherited from the declaration record and was not added to front matter.
- `cg-chebyshev-bound`: consistently bolded the matrix and vectors and kept the original explanatory wording. The primary declaration's `Saad2003`, Theorem 6.29 and `TrefethenBau1997`, Theorem 38.5 citations are inherited. Added only `Saad2003`, (6.128), which appears in the docstring for the related condition-number declaration `Matrix.PosDef.re_quadForm_sub_cgIterate_le_four_mul_pow_pseudoConditionNumber` at `CG.lean:296–299`, but is absent from the primary declaration's inherited references. The verified first-kind Chebyshev definition was not linked because the original prose does not mention it.
- `cg-finite-termination`: consistently bolded the solution and iterate vectors; linked “Krylov space” to `/explore/statements/615008ca-f5db-5cff-ab6b-b07f178cbd05/`. Its citation is inherited from the declaration record and was not added to front matter.
- No changes were needed to `cg-optimality`'s existing vector/matrix fonts or transpose notation. No transpose or Hermitian-transpose convention occurs in these four statements.
- All UUIDs, IDs, theorem result bindings, kinds, formulas, provenance, and existing review metadata were retained. All citation keys exist in `explore/content/references/`.

The pinned editor objects' `object.references` arrays are empty because they describe only authored references. Inherited references come from each evidence declaration's record. Their actual pairs are: `cg-optimality` — `Saad2003` §5.2; `TrefethenBau1997` Theorem 38.1. `cg-polynomial-bound` — `Saad2003` §6.11.3. `cg-chebyshev-bound` — `Saad2003` Theorem 6.29; `TrefethenBau1997` Theorem 38.5. `cg-finite-termination` — `Saad2003` §6.2. These pairs are already rendered with their theorem pages. The sole front-matter citation retained is the additional `Saad2003` (6.128) locator, verified in the related condition-number declaration's Lean docstring as described above; it is not in the primary declaration record.

## Symbol-role registry proposals

The current `explore/notation.json` declares only `cg-optimality`. For a later registry update, propose:

```json
"statements/cg-polynomial-bound.md": {"matrices": ["A"], "vectors": ["x"]},
"statements/cg-chebyshev-bound.md": {"matrices": ["A"], "vectors": ["x"]},
"statements/cg-finite-termination.md": {"vectors": ["x"]}
```

These are based on the named matrix and iterate/solution vectors in the text; they are proposals only and the shared registry was not edited.

## Unresolved mathematical review

The standalone bodies do not state all assumptions or define all symbols used; the CG algorithm page supplies some shared context, but the statement files are independently readable content:

- `cg-optimality.md:8–10` uses `\mathbf{A}`, `\mathbf{x}_\star`, and `\mathbf{r}_0` without stating positive definiteness, `\mathbf{A}\mathbf{x}_\star=\mathbf{b}`, or defining the initial residual. The Lean signature and docstring at `CG.lean:167–173` state positive definiteness, the solution equation, and describe the residual through its definition in the Krylov space. Do not add missing hypotheses or a residual definition without editorial review.
- `cg-polynomial-bound.md:8–12` does not state the positive-definiteness and solution assumptions present in `CG.lean:218–244`; its notation `x_k` is not independently bound in the body. The authored bound is the “beats every residual polynomial” form, while the same Lean `result:` ID also covers a spectral-set/`\eta` bound at `CG.lean:240–256`. Confirm intended scope and correspondence before changing mathematics.
- `cg-chebyshev-bound.md:8–12` gives an interval of eigenvalues with `a>0`, but not the CG solution equation or definitions of `\mathbf{x}_\star`, `\mathbf{x}_k`, or `\kappa` beyond its displayed ratio. The formal source at `CG.lean:277–299` states a Hermitian matrix, spectrum inclusion in `[a,a']`, positivity, and a solution equation. Confirm whether the page context is intended to supply the omitted hypotheses.
- `cg-finite-termination.md:8` does not state positive definiteness, the solution equation, or define the initial residual. The formal source at `CG.lean:502–508` has those assumptions and defines `\mathbf{r}_0=\mathbf{b}-\mathbf{A}\mathbf{x}_0`; it gives the bound by the grade and in particular `q=|n|`. Confirm the informal “dimension n” wording and self-contained hypotheses.

No hypotheses or proof claims were invented or added. No external proof URL was needed because these results have complete Lean proofs in the pinned source (`admission_reported: false`). No unresolved/ambiguous definition target was used. The polynomial-evaluation definition was deliberately not linked because it does not define a scalar polynomial.

## Validation and limits

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX; 0 errors. `git diff --check` passed. Definition links were checked against existing Markdown definitions and matching UUIDs in the pinned editor objects. No browser render or repeated-placement preview was available in this source-only pilot; the notation check does not establish mathematical equivalence between readable prose and formal evidence.
