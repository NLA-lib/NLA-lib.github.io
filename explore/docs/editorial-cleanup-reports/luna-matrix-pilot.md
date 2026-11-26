# Luna matrix pilot cleanup report

Scope: the four assigned shared statements only. Baseline revisions are from the pinned release Explorer editor snapshot under `/tmp/nlalib-release-explorer/api/v1/editor/objects/`. Each editor object has an empty `object.references` field. The linked declaration record for `NLAlib.mul_arnoldiMatrix` supplies inherited Saad2003 references at §6.3 and Proposition 6.5, already rendered for the Arnoldi relation. No proposal/draft was submitted; this is a bounded source and report commit for coordinator review. Presentation checks do not validate mathematical truth or the correspondence between prose and Lean.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `19646f49-e8db-5918-a0df-83eaf8db1648` | `explore/content/statements/matrix-norms-19646f49.md` | `996c3fa99f99916b88e8440aeea035a06690a3023d793928ad3a6d3b76b5f2a1` | `proposed` |
| `dfe0f5c1-7607-5831-98c2-83dedb7248da` | `explore/content/statements/arnoldi-relation.md` | `04d6913c26495fcb4c9ded65574804a19a18348b950ceff5d0fd5ebf25524694` | `proposed` |
| `1ebd9712-579d-596a-966f-9119a353806b` | `explore/content/statements/nlalib-arnoldimatrix-1ebd9712.md` | `86efe630d83391ed4967f07a9f87facc11955c862cfe92517201e19ae6f79afa` | `proposed` |
| `5979b536-df6b-57bf-932a-0f2b0dec440d` | `explore/content/statements/residuals-and-spectral-separation-5979b536.md` | `3e63e371d6e7b34b46dd720397e5ad48c450ffadf2b15b1b04f8415ef3d177dc` | `proposed` |

## Changes and sources

- **Matrix norms**: retained the existing vector/matrix bolding and norm types. Linked the first mention of singular values to the existing singular-value-decomposition definition, UUID `d5bca832-63a1-5043-ab6e-03b8402a2a55`, whose prose defines the singular values and their ordering. No bibliography strings or inherited references were present to move/reuse. The statement's comparison with best low-rank approximation remains broad; no sharper claim was inferred.
- **Arnoldi relation**: retained the existing phrase “canonical Krylov bases,” bold matrix/vector notation, and Hermitian transpose. Linked that existing phrase to the Arnoldi process definition, UUID `1ebd9712-579d-596a-966f-9119a353806b`, without adding an explanatory clause. Its declaration record supplies the already-rendered Saad2003 citations at §6.3 and Proposition 6.5; no statement-body citation string or additional reference association was needed. Its zero-column breakdown convention and equation are unchanged.
- **Arnoldi process definition**: retained explicit bolding and `\mathsf{H}`. No definition link was added: the available Krylov-space-and-grade definition, UUID `615008ca-f5db-5cff-ab6b-b07f178cbd05`, states a real-only scope, whereas the bound definition `NLAlib.arnoldiMatrix` has a formal signature over `[RCLike 𝕜]`, including complex scalars. No compatible, verified general target was identified. The formal binding and readable prose otherwise remain intact.
- **Residuals and spectral separation**: changed the Greek matrix symbol from `\mathbf\Lambda` to `\boldsymbol{\Lambda}`; retained `\mathsf{H}` conventions elsewhere. No bibliography strings or inherited references were present to move/reuse. The statement does not identify a particular spectral-separation theorem or subspace, so none was added. This remains a general explanatory definition, not a quantitative residual-to-distance bound.

**Reference association check across all four:** Matrix norms and residuals/spectral separation are authored definitions without declaration citations; `NLAlib.arnoldiMatrix` has no declaration references. The Arnoldi relation (`NLAlib.mul_arnoldiMatrix`) inherits Saad2003, edition 2, §6.3 and Proposition 6.5 from its pinned declaration record. These inherited references are rendered; the statement-level editor object has no explicit references. No statement-body bibliographic strings needed removal and no additional `references` metadata was added. No relocations or duplicate identities were proposed. UUIDs, IDs, kinds, formal bindings, hypotheses, norm types, constants, provenance and review metadata were preserved. No proof URLs were added; these are definitions or an existing checked result and no new proof claim was made.

## Link verification and checks

Read and verified the exact target Markdown sources for the definition links retained: Arnoldi process (`1ebd9712-579d-596a-966f-9119a353806b`) and singular-value decomposition (`d5bca832-63a1-5043-ab6e-03b8402a2a55`). Their front matter UUIDs match the linked routes. Inspected Krylov space and grade (`615008ca-f5db-5cff-ab6b-b07f178cbd05`); its real-only scope is incompatible with the complex-capable formal signature of `NLAlib.arnoldiMatrix`, so that link was removed.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. Rendered page preview was not run in this bounded source pass; the notation check does not validate mathematical correctness, link hover behavior, bibliography rendering, or formalization correspondence. No statement-level structured references were needed: the Arnoldi relation already receives its Saad citations from its declaration metadata.

## Registry proposal

Consider reviewed role declarations for the symbols appearing in these files if the notation registry is expanded: `A`, `Q`, `H`, `U`, `\Lambda`, `x`, `b`, and `r` as matrix/vector roles require document-specific classification; `\Sigma` is a matrix in the linked SVD definition, while `\lambda` is scalar. This batch did not modify `explore/notation.json`; classify only after a registry owner reviews each source context.
