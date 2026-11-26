# Luna generated CG pilot 01

This report covers only the three assigned generated result objects. Each Markdown
source was materialized from its pinned `source_markdown` template at the same
`source_path`, preserving its UUID, generated-entry ID and `result:` binding. The
baseline revisions below are from `/tmp/nlalib-release-explorer/api/v1/editor/generated/`.
No API proposal was submitted. No other shared files were changed.

## `5ea3fa86-65cd-584d-affa-921f27e54280` — `cg-galerkin-formula`

- Baseline revision: `4fa1df14233f216500e5e46dc5ec2f04032992fe94d1f2938608a90244820467`.
- Source: `explore/content/statements/entry-5ea3fa86-65cd-584d-affa-921f27e54280.md`.
- Outcome: `proposed`.
- Changed the opening fragment to a sentence and formatted the formula as display math. Kept vectors and matrices bold with indices outside the bold arguments; kept `q` scalar and the operator spelling `\mathsf{cgIterate}`. The inverse and Hermitian transpose remain as stated. Removed the body citation `[Saad2003, §6.7]`; `reference_links.inherited` contains exactly `Saad2003`, locator `§6.7`, so the structured reference is retained from the linked declaration. No extra reference field was needed.
- No definition link added. The statement is about a Krylov basis over the generic `RCLike` scalar field in the Lean signature. The available authored Krylov-space definition is real-only and is not a scope-safe target.
- Review issue: the prose title says `Q` is an orthonormal basis of the Krylov space, but the body relies on that condition without stating its range equality. The linked Lean signature supplies both `HasOrthonormalCols Q` and `range Q = krylovSpace A (b - A*x₀) q`; this is represented in the title but not fully spelled out in the readable body. Preserve as source wording for review rather than adding a new hypothesis clause in this pass.

## `54393ec6-774c-510b-8e5d-df4f4f7b7a0d` — `cg-galerkin-condition`

- Baseline revision: `879ba8234e6c7f1717301560048b3e39c829b27e7296c71e681ce307b721d9bf`.
- Source: `explore/content/statements/entry-54393ec6-774c-510b-8e5d-df4f4f7b7a0d.md`.
- Outcome: `proposed`.
- Made the opening a sentence and the Galerkin residual identity a display equation. Preserved `\mathcal{K}_q` as the subspace and `\mathbf{K}_q` as the Krylov matrix, with `\mathbf{K}_q^{\mathsf{H}}` as its Hermitian transpose. Kept all vectors and matrices bold and indices scalar. Removed inline Saad citation strings. The inherited structured links retain `Saad2003`, locator `§6.7`, and `Saad2003`, locator `(5.3)`, respectively. Preserved the real-symmetric qualification for the orthogonal-projection description and rewrote its dangling “there” reference as a self-contained sentence.
- No definition link added. The theorem is valid over the `RCLike` field in its Lean signature; the available Krylov-space definition is real-only.
- Review issue: the natural-language statement says the residual is orthogonal to the Krylov subspace, while the displayed identity uses the conjugate transpose of the Krylov matrix. This equivalence is consistent with the linked source’s `krylovMatrix` formulation, but the readable entry does not define that matrix or its column-space relation. The Lean signature states the matrix identity directly. Review whether to add a precise definition link or explanatory definition after a field-compatible target is available.

## `b5d079e2-0c06-547d-bf97-8c505409106b` — `cg-orthogonality`

- Baseline revision: `204875d23c2a69e3a92fed4bc267a8755b058d75927bf9a7b2d1ee7ae4d1afda`.
- Source: `explore/content/statements/entry-b5d079e2-0c06-547d-bf97-8c505409106b.md`.
- Outcome: `proposed`.
- Made the opening sentence self-contained and set the orthogonality identity as display math. Preserved the Hermitian transpose, bold vector/matrix roles and scalar indices. Removed the inline citations to Hestenes–Stiefel and Trefethen–Bau. `reference_links.inherited` preserves `HestenesStiefel1952`, locator `Theorem 5:1`, and `TrefethenBau1997`, locator `Theorem 38.1`. The original prose also identified relation `(5:3b)`, which was not an inherited locator. Added the exact structured association `HestenesStiefel1952`, locator `(5:3b)` to this statement's front matter. The citation key exists in the frontend bibliography; the locator is verified against the Hestenes–Stiefel paper, section 5, Theorem 5:1 relation (5:3b) ([NIST-hosted paper](https://math.nist.gov/mcsd/Reports/2002/hestenes-steifel-52.pdf)).
- No definition link added; no field-compatible standalone definition of the CG direction vectors was verified.
- Review issue: the preserved title mentions orthogonal residuals and conjugate directions, but this result’s body and linked Lean declaration state only conjugacy of search directions. The assigned source body made the same narrower claim. Preserve the library title and report the mismatch for review; do not broaden the theorem prose.

## Shared checks and evidence

- The three snapshots report `references: []` for authored associations but have nonempty `reference_links.inherited`; the citation edits above rely on the inherited records, not the empty authored list. No citations were copied from related entries.
- All three formal evidence records link to the assigned results and report `admission_reported: false`. The pinned Lean source has proof terms for the declarations in `NLAlib/Krylov/LinearSystems/CG.lean` (lines 112–125 and 128–146) and `NLAlib/Krylov/LinearSystems/CGRecurrence.lean` (lines 385–393). No external proof URL was needed.
- No symbol-role registry change is proposed. In particular, the `\mathcal{K}` subspace and `\mathbf{K}` Krylov matrix are distinct roles; the latter is file-local and already explicitly bold.
- No rendered-page preview or full content build was run. `node explore/tests/check_notation.cjs` passed: 2,303 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 245 statement sources; direct checks confirmed each assigned UUID, `entry-<uuid>` ID, `result:` binding, and the one added reference association. All checks passed. These checks do not verify theorem truth or full natural-language/formal equivalence.
