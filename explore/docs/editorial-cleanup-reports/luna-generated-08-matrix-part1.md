# Luna generated matrix cohort 08, part 1

Scope: the five assigned generated result entries below. Baseline revisions are from the pinned `/tmp/nlalib-release-explorer/api/v1/editor/generated/` records. Each entry was checked for an authored file with the same result/declaration binding before materialization; no authored aliases were found. Templates preserve the exported `kind`, `id`, `uid`, theorem result binding, title, and readable body. No structured reference field was added because the matching citations are already inherited from each exact declaration record.

| UUID / result | Baseline revision and source | Outcome | Changes and actual references |
|---|---|---|---|
| `c734cb04-fd47-5ab8-913b-0f2ad9488d91` / `cg-error-gauss-quadrature` | `cfd8d95710b17a186e05b52f215ff46de491f8712bca08635bad428b8f57c548`; `explore/content/statements/entry-c734cb04-fd47-5ab8-913b-0f2ad9488d91.md` | proposed | Removed trailing inline citation strings, reusing inherited `GolubMeurant2010` (Ch. 12) and `GolubStrakos1994` (§3). No notation or link changes. |
| `e34ae886-e86b-5a12-8d4b-4027073d4d2f` / `cg-error-gauss-radau-bounds` | `51f2cbeb857cf9c44b4d2006d0582bf75b19897f94ae3eaaf2880669ac49eb7e`; `explore/content/statements/entry-e34ae886-e86b-5a12-8d4b-4027073d4d2f.md` | proposed | Removed trailing inline citation strings, reusing inherited `GolubMeurant2010` (Ch. 12) and `GolubStrakos1994` (§3). Preserved the assertion and its math. No notation or link changes. |
| `39557fa9-2841-5d3e-911e-23bdfea4778f` / `cg-finite-precision-accuracy` | `85176ba02a89dca0c2eb4e35d74675bc698924f4f97e999360ed0526228e9c06`; `explore/content/statements/entry-39557fa9-2841-5d3e-911e-23bdfea4778f.md` | proposed | No inherited references (`reference_links.inherited` empty); retained “No printed source.” No citation or notation changes. |
| `38342b39-b8eb-5460-afbc-59fe3832654f` / `cg-lanczos` | `2e5f66b4b03f2a27030621486944982c5f055f9436e21bead8a16732f1850be8`; `explore/content/statements/entry-38342b39-b8eb-5460-afbc-59fe3832654f.md` | proposed | Removed trailing inline citation, reusing inherited `Saad2003` (§6.7.1). No notation or link changes. |
| `81978087-c08d-5057-811b-cd7c41d33d7d` / `cg-near-optimality` | `887167e9fdbd3088b59ad2b39a09b6d957e84169904f4761f82e4064d2aabe50`; `explore/content/statements/entry-81978087-c08d-5057-811b-cd7c41d33d7d.md` | proposed | Removed trailing inline citation, reusing inherited `ChenPersson2026` (Theorem 1 and (5)). Corrected doubled backslashes in the mathematical title to supported braced math `\mathbf{A}^\alpha`; no statement-body math changed. |

## Review notes

The first four inline citations exactly matched the corresponding inherited key/locator pairs. The fifth did as well. These pairs were read from each object's `reference_links.inherited`, not inferred from `object.references` or related declarations. There are no new semantic links: no link was needed to relocate citations, and no direct definition target was added solely as a substitute for a related concept. No source or theorem assertions were added or removed. The finite-precision entry's “No printed source.” note remains because its inherited reference list is empty.

All five exported templates were materialized at their assigned UUID paths with result bindings intact. No aliases were merged or overwritten. No role-registry addition is proposed.

## Checks and limitations

`git diff --check` passed. `node explore/tests/check_notation.cjs` checked 2,348 authored equations and now reports zero KaTeX errors (the pre-fix generated title had doubled backslashes and failed parsing). The notation check establishes parseability only; it does not verify the mathematical claims, source correspondence, or rendered inherited-reference display. No preview service was available in this bounded workspace.
