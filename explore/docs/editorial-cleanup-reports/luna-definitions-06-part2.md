# Luna matrix definitions cohort 06, part 2

This report covers only the second five assigned definitions. Baseline revisions and editor metadata were read from the pinned Explorer editor objects. Each authored `object.references` is empty and `reference_links` is null; inherited declaration references were read from the corresponding pinned declaration records.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `0dbb2cc9-a263-552d-99ab-3c821230325b` | `explore/content/statements/nlalib-shiftedqr-stepalgorithm-0dbb2cc9.md` | `16b88ba9c44e9b4bdf7f627a2d7c8a4652a6b840d0d00027def8703eb2f1dd98` | `already-consistent` |
| `ccee634c-02eb-5769-8d49-3bf04e99f8af` | `explore/content/statements/nlalib-signnewtoniterate-ccee634c.md` | `a79635042e2d5124a73cb011befeaef3d809f0f7d005d2b4db5c12fdcddb2cc2` | `already-consistent` |
| `9af30d5f-52d8-5a0a-af57-e2b4820cfa0a` | `explore/content/statements/nlalib-sketchandsolve-9af30d5f.md` | `b89389e1372d2917c8f229c923b8b5586c0b92d224f7e0940e84d656c3ae1398` | `already-consistent` |
| `cf55d814-21be-5b57-b8ce-33a3917607de` | `explore/content/statements/nlalib-smalleig-smalleigalgorithm-cf55d814.md` | `7beff6ede936df529956340a24fffa7562896d4c1cdbefe35ea49482fc2e5368` | `already-consistent` |
| `c1b568f6-4bc5-5e42-91e7-8b77a20c9e57` | `explore/content/statements/nlalib-spectralbisection-bisectionprogram-c1b568f6.md` | `9713ae3ff117d12813200cd4cc9c26e23e1eb8175a95ad7078e4e2c04c4bf7e2` | `proposed` |

## Findings, links, and citations

- **Shifted-QR step interface**: already consistent for this scope. No direct matching definition link target or inline citation was identified; the exact operation model and singular-shift allowance remain unchanged. Declaration references: none.
- **Newton matrix-sign iteration**: already consistent. Its inverse-averaging recurrence and stated difference from the Newton–Schulz update remain unchanged. Inherited declaration reference: `Higham2008`, §5.3. No inline citation string is present.
- **Sketch-and-solve least squares**: already consistent. The minimum-norm formula and sketch caveat remain unchanged. Inherited declaration reference: `EpperlyWebber2026`, §2. No inline citation string is present.
- **Small-eigenvalue solver certificate**: already consistent. The success, resource and write claims and full work/span expression are unchanged. Declaration references: none.
- **Stored spectral bisection**: linked the existing phrase “Newton–Schulz sign iteration” to its definition, UUID `33cd8a3d-4740-5cbd-82aa-7e67e7c152da`, and existing “QR” to QR factorization, UUID `adb72f11-3503-58f9-89c4-98a60c4f7a40`. The sign-iteration target applies to Hermitian matrices with adjoint notation; QR's complex matrix domain matches the stored complex samples. No step, claim, parameter, formula, or procedure was changed. Declaration references: none.

Every editor object has empty authored `object.references`; `reference_links` is null. The only inherited citations are those listed above, checked in the actual declarations. No inline bibliographic strings occur, so nothing was relocated. No citations were copied from related declarations. IDs, UUIDs, formulas, titles, field assumptions, identities, and metadata were preserved.

## Validation and limitations

Verified the two target definitions and their UUIDs and scopes. No additional claims or procedural explanation were introduced. `node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.
