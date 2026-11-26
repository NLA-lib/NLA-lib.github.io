# Luna matrix definitions cohort 05, part 1

This report covers only the first five assigned definitions. Baseline revisions, editor evidence, and reference associations were checked in the pinned Explorer objects under `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`; declaration-bound references were verified in each pinned declaration record.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `23f709a3-92ab-5cef-ab62-2b33870d9605` | `explore/content/statements/nlalib-krylov-golubkahan-band-solve-23f709a3.md` | `2785b5700079e1428bc02c9a758b420d05e5b13bb0d9a58e186965c650f4b7d5` | `already-consistent` |
| `bdfac892-aa5e-5014-991c-ef2499ca3d72` | `explore/content/statements/nlalib-krylov-lanczos-certification-algorithm-bdfac892.md` | `bdb16af646b18906a5051832ee580a29c307856432bd0857e544663d1b38e3bc` | `already-consistent` |
| `78fee89f-9f4d-5baa-8101-b32c183c88b6` | `explore/content/statements/nlalib-krylov-lanczos-certification-ritzalgorithm-78fee89f.md` | `1534e16f136681dc380d04be9705e11ed03c9c64c302fff8716ca3c6e89fe513` | `already-consistent` |
| `8a730a7c-e552-5641-bd95-fa635dcebc98` | `explore/content/statements/nlalib-krylov-lanczos-solve-8a730a7c.md` | `fbbba7f9aad1d6f8495437df1d02e7dc612d1b67cab8ea27727b88333c9bac86` | `already-consistent` |
| `bc762b7b-4199-51cc-b90c-187c41dc3af9` | `explore/content/statements/nlalib-lanczosfa-bc762b7b.md` | `de156b03115ace850069c74ec32a4f373773b802653e99d5d3bd0925d3b3f329` | `proposed` |

## Edits and scope

- **Block Golub–Kahan band solve**: already consistent for this scope. The declaration is a generic operator routine and the source's transpose notation, dimensions and procedural steps are unchanged. Its declaration has no references.
- **Lanczos certificate algorithm**: already consistent for this scope. Its symmetric-matrix condition, accuracy envelope, static-budget claim, output relation and stopping conditions are unchanged. The declaration has no references.
- **Lanczos Ritz certificate**: already consistent for this scope. The additional condition `kE\le1/100` and output claims are unchanged. The declaration has no references.
- **Guarded Lanczos solve**: already consistent for this scope. It explicitly supplies a real starting vector and preserves all guards and zero-output behavior. The declaration's inherited citation is `Paige1972`, §2; no inline citation string or duplicate association was present.
- **Lanczos matrix-function approximation**: linked the existing term “Hermitian” to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`, and “Lanczos process” to its direct process definition, UUID `d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239`. Both targets match the Hermitian/Lanczos concepts and do not impose a real-only field restriction. The declaration `NLAlib.lanczosFA` is `[RCLike 𝕜]`. Its inherited citations remain `Saad1992`, §2, and `ChenPersson2026`, equation (1); there are no inline citation strings or added references.

## Citation audit and validation

The two declarations with inherited citations are `NLAlib.Krylov.Lanczos.solve` (`Paige1972`, §2) and `NLAlib.lanczosFA` (`Saad1992`, §2; `ChenPersson2026`, (1)). The other three declaration records have empty `record.references`. All five editor objects have empty authored `object.references`; their `reference_links` fields are null. No citation associations were borrowed from related declarations.

Verified both definition targets and their UUIDs. No formulas, math-environment segmentation, field restrictions, hypotheses, procedure steps, titles, formal bindings, IDs, or metadata changed. No additional prose or helper expansion was added.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

No notation registry change is proposed. Existing matrix/vector typography is explicit.
