# Luna Krylov cohort 03, part 1

This report covers only the first five files in the assigned `krylov` cohort. Baseline revision tokens, evidence and reference associations were inspected in `/tmp/nlalib-release-explorer/api/v1/editor/objects/{uuid}.json`; declaration references were checked in the corresponding pinned declaration records where applicable. Every object has `reference_links: null` and `object.references: []`. All five linked declaration records also have empty `record.references`. No inline bibliographic strings appear in the five bodies. No citation association was moved or added.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `94212462-4541-5bf1-96ea-38d5e791525e` | `explore/content/statements/loewner-order-and-majorization-94212462.md` | `7051dc907cdba8f584b357e739f0da870a4a2a1ab3f943d9daaabeb21c153c8f` | `proposed` |
| `47fa9a99-bf7f-54d6-ad4e-a307c2efa85a` | `explore/content/statements/nlalib-gramschmidtq-47fa9a99.md` | `17d8c9ad9e656d71fdd036cc92a37f36461f5233764d385789250c436104387c` | `already-consistent` |
| `af080b3b-42f5-5b70-adba-76b80f20b48b` | `explore/content/statements/nlalib-cgs2-cgs2extendroutine-af080b3b.md` | `1f6f204f04a9161be4240d124c0354e1128b25c43c7a4c424972e633e024c013` | `already-consistent` |
| `12a7ec72-6c64-59e6-b7de-7aff8d055ba2` | `explore/content/statements/nlalib-isbasisextension-12a7ec72.md` | `01a812673213738c1368cba45d87f00060bbc7e5578e5cec97a245c018cf2b52` | `already-consistent` |
| `fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393` | `explore/content/statements/nlalib-isbasisextensionerr-fb78aa8d.md` | `fc73e8b1495e39878204d13d5a471ba87e309f696b6394a9a5f8efe509ff9cd9` | `already-consistent` |

## Changes and checks by statement

- **Loewner order and majorization**: added a link on “Hermitian matrices” to Hermitian spectral decomposition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`; its definition begins with the Hermitian condition and uses the adjoint convention. Linked “singular values” to their definition, UUID `581c9098-24f3-55b6-bd36-a47af48b21ff`, which defines them from `\mathbf{A}^{\mathsf{H}}\mathbf{A}`. Both targets permit complex matrices and are scope-compatible with the source's adjoint formula. The prose, inequality and majorization claim are unchanged.
- **Gram–Schmidt orthogonalization**: already consistent for this batch. Explicit matrix/vector bolding is used. Its pinned `NLAlib.gramSchmidtQ` declaration is `[RCLike 𝕜]` and has no inherited references. No specific additional definition link was needed.
- **CGS2 extension routine**: already consistent for this batch. Explicit matrix/vector bolding, scalar threshold notation and column indices are preserved. The linked `NLAlib.CGS2.cgs2ExtendRoutine` declaration has no inherited references. Its generic operation signature does not supply a field-specific definition target for adding a link.
- **Exact basis extension**: already consistent for this batch. The exact block relation, zero-column conditions, and conditional orthonormality claim retain their existing wording and formulas. The linked `NLAlib.IsBasisExtension` declaration supports `[RCLike 𝕜]` and has no inherited references. No broader prose or new conditions were added.
- **Rounded basis extension error**: already consistent for this batch. The definition is explicitly real-valued in its linked `NLAlib.IsBasisExtensionErr` signature; the transpose `\mathbf{Q}^{\mathsf{T}}` is retained. Its declaration record has no inherited references. No complex-valued exact-extension link was added because it would not match this real-only scope.

All five pinned objects have empty authored `object.references`; `reference_links` is null. Each formal declaration record referenced by the four declaration-bound objects has an empty `record.references` list. No body contains a bibliographic citation string. Thus no references needed relocation or reuse. IDs, UUIDs, kinds, formal bindings, formulas, conditions, provenance and review metadata were preserved. No proof source, relocation or duplicate was proposed.

## Link verification and validation

Read the exact target sources and checked their front matter UUIDs. The Hermitian spectral definition uses `\mathbf{A}^{\mathsf{H}}=\mathbf{A}` and a real diagonal in its Hermitian spectral decomposition, without restricting the matrix field to `\mathbb{R}`. The singular-values definition uses the adjoint of a general matrix. The link targets are therefore compatible with the complex-capable Loewner definition.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

The existing explicit bolding already identifies the Latin matrices and vectors in these files. No symbol-role proposal was needed for this part. No global notation registry change was made.
