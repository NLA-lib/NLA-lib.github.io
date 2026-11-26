# Luna factorization definitions cleanup 01

Batch scope: the five assigned authored definitions only. Baseline revision tokens and evidence were checked in the pinned release Explorer editor objects under `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`. Every object has `object.references: []` and `reference_links: null`; each evidence record is `authored` with no Lean declaration binding, so there are no linked-declaration inherited citations. No inline bibliographic strings were present in the five statement bodies. No proposal/draft was submitted; this commit contains only the assigned statement edits and this report.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `2fa76a05-ce3c-5a1c-9aee-625c01bfd829` | `explore/content/statements/orthogonal-projection-2fa76a05.md` | `bd869a150736db441e40392dc0f788cec604e971646ea2e37edafed2cdcc4ac8` | `proposed` |
| `adb72f11-3503-58f9-89c4-98a60c4f7a40` | `explore/content/statements/qr-factorization-adb72f11.md` | `4240c6695a842f8fccd1610ecd51360b2f1a1c90e17cb739ba71bc25c7d82a2b` | `proposed` |
| `d00946c1-7d12-50e4-a6da-635456a9fca7` | `explore/content/statements/cholesky-factorization-d00946c1.md` | `ddf9df09b5f3542c3322f4330be3fd4126cda9440efe85c2cd7851fd3128e4a3` | `already-consistent` |
| `a7033c37-8e44-526f-893d-3d63c52090f1` | `explore/content/statements/lu-factorization-a7033c37.md` | `98927781007345bdad0ea3e29fd30ef467a0ff1b094f76590a3b5c5c42e40553` | `already-consistent` |
| `a6e9180a-1bfe-574e-aacb-b0a161333177` | `explore/content/statements/plu-factorization-a6e9180a.md` | `13e88164da1cce1a711a4e2233681494e729fc94ff6230ebe74ec41ae5eba566` | `already-consistent` |

## Changes, links, and source associations

- **Orthogonal projection**: linked the existing phrase “orthonormal columns” to the QR factorization definition, UUID `adb72f11-3503-58f9-89c4-98a60c4f7a40`. The target states the matching condition `\mathbf{Q}^{\mathsf{H}}\mathbf{Q}=\mathbf{I}` for a complex thin factor with `m\ge n`; this matches the source's adjoint-based orthogonality. The source does not state dimensions, and none were added. The phrase about principal angles remains unlinked because no standalone matching definition target was found.
- **QR factorization**: linked the existing term “Gram–Schmidt” to the dedicated Gram–Schmidt orthogonalization definition, UUID `47fa9a99-bf7f-54d6-ad4e-a307c2efa85a`. Its pinned declaration `NLAlib.gramSchmidtQ` has signature over `[RCLike 𝕜]`, compatible with real and complex scalars, and describes columnwise orthogonalization. No link was added for Householder transformations or Givens rotations because no specific corresponding definition page exists in this content set. QR eigenvalue iteration remains distinct and unlinked.
- **Cholesky factorization**: already consistent for this scope. Matrix/vector bolding, adjoint convention, and factor forms are explicit. The Hermitian positive-definite hypothesis and triangular-factor conditions are unchanged. No matching standalone definition target for positive definiteness was found.
- **LU factorization**: already consistent for this scope. Matrix bolding is explicit, and the text preserves the warning that unpivoted elimination needs conditions. No link was added to PLU because that could blur pivoted and unpivoted conventions; no definition target for triangularity was found.
- **PLU factorization**: already consistent for this scope. Matrix bolding and the row-permutation convention `\mathbf{P}\mathbf{A}=\mathbf{L}\mathbf{U}` are explicit. Pivot-selection wording is unchanged. No link was added to LU because the shared triangular-factor terms do not establish that a pivoted factorization is the same unpivoted method.

**References across all five:** the pinned objects have empty authored `object.references`, `reference_links` is null, and all evidence records are authored definitions rather than Lean declaration-backed entries. Thus there are no inherited declaration references to reuse. No inline bibliography citations occurred in these bodies, so no citation association was moved or added. No proof sources, relocations, or duplicate identities were proposed. IDs, UUIDs, kinds, formulas, hypotheses, conventions, provenance, and review metadata were preserved.

## Validation and unresolved issues

Verified the exact front-matter UUIDs and definitions of both link targets. The QR target is complex-valued, with the same Hermitian orthogonality condition used in the projection definition; the Gram–Schmidt target supports `[RCLike 𝕜]`. No real-only target was used. Cholesky, LU and PLU were left unchanged; their prose does not specify extra dimensions or pivot conditions, and none were inferred.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. Rendered preview was not run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence. Missing standalone targets noted above can be handled in a separate definition-curation pass if desired.

## Registry proposal

No new roles were introduced in this batch. The files already use explicit Latin matrix bolding (`A`, `Q`, `R`, `L`, `U`, `P`) and scalar/dimension indices in ordinary type. Consider role declarations for those symbols only if the notation registry owner finds it useful; this batch did not modify `explore/notation.json`.
