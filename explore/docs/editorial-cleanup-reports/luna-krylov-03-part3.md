# Luna Krylov cohort 03, part 3

This report covers only the final five files in the assigned `krylov` cohort. Baseline revision tokens, evidence and reference associations were checked in the pinned release Explorer editor objects. All five objects have `object.references: []` and `reference_links: null`; their evidence records are authored definitions with no Lean declaration binding, so there are no inherited declaration citations. No inline bibliographic strings occur in these bodies. No citation associations were moved or added.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `2fbe0187-6658-5dd5-8d09-3908e5df46fd` | `explore/content/statements/full-orthogonalization-method-2fbe0187.md` | `a2a695cc4cc1d29c1452505d12c9c518dc9f90b3b8cdbe7a229fddeaa609806a` | `already-consistent` |
| `7d1681b7-7670-532a-98d3-4e7886e4adcc` | `explore/content/statements/gmres-7d1681b7.md` | `95743be599019760311e778c41a936e72fa78ecd436a641d57c7a7180338beb1` | `proposed` |
| `0368af89-f05c-573a-9e87-1799faf5909b` | `explore/content/statements/lsqr-0368af89.md` | `bc31d7990b235e039e968ea1ce9a94db3a1acff7f91413d85c807fff2e037137` | `proposed` |
| `d881b1fc-87da-5f4f-a75d-8d11c09f6fbf` | `explore/content/statements/cgls-d881b1fc.md` | `0046cc07eafd777fce2afca8722dd5844cdb3dd4f5ce0b3826b4b29e979ef26f` | `already-consistent` |
| `be6e71b0-40da-513f-9790-9c44f41a3a31` | `explore/content/statements/landweber-iteration-be6e71b0.md` | `1b25e3d5418f09e31baac8a4851ef7bfe5e8e1a12c0a2aafe86756032a59af16` | `already-consistent` |

## Changes and scope decisions

- **Full orthogonalization method**: already consistent for this scope. Explicit Latin matrix/vector notation and the residual formula are preserved. The readily available Krylov-space-and-grade definition is real-only, while this authored method states no scalar field; no link was added across that unresolved field scope.
- **GMRES**: linked the existing “Arnoldi” mention to the Arnoldi process definition, UUID `1ebd9712-579d-596a-966f-9119a353806b`. Its formal declaration supports `[RCLike 𝕜]`, including real and complex scalars. The minimization formula and restart distinction are unchanged. No Krylov-space link was placed inside the existing mathematical expression.
- **LSQR**: linked the existing “CGLS” mention to the CGLS definition, UUID `d881b1fc-87da-5f4f-a75d-8d11c09f6fbf`. The target uses the adjoint and imposes no real-only restriction, matching the source's complex-capable notation. No link was added to the block Golub–Kahan process because that definition is a block extension relation, not a direct definition of scalar Golub–Kahan bidiagonalization.
- **CGLS**: already consistent for this scope. Its adjoint-based normal equations, full-column-rank condition, and rank-deficient caveat are explicit. No standalone canonical CG definition was identified; the existing CG optimality page is a theorem, not a definition, and was not substituted as one.
- **Landweber iteration**: already consistent for this scope. Matrix/vector bolding, real scalar step size, adjoint, objective and finite-step/convergence distinction are explicit. No directly matching standalone definition target for its spectral-filter identity was found.

All five editor objects have empty authored `object.references` and no declaration metadata; there are no inherited citations. No inline bibliographic strings were found. No statement was assigned a missing hypothesis, and no formulas, field conditions, norms, dimensions or scalar domains were changed. No proof sources, relocations or duplicate identities were proposed.

## Link verification and checks

Read and verified both linked targets and their front-matter UUIDs. Arnoldi process is defined for square matrices with `[RCLike 𝕜]`; CGLS uses the adjoint formulation without restricting the field to real scalars. The real-only Krylov-space definition was checked and intentionally not linked from the field-unspecified FOM definition.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

No notation roles needed correction or proposal in this part. The existing explicit bolding is consistent; no global registry change was made.
