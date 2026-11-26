# Luna matrix definitions cohort 04, part 3

This report covers only the final five files in the assigned matrix cohort. Baseline revisions and evidence were checked in the pinned release Explorer editor objects. Each object's authored `object.references` is empty and `reference_links` is null. For declaration-bound entries, I read the corresponding pinned declaration's `record.references` and report inherited associations below. No body contains a bibliographic citation string requiring relocation.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `33cd8a3d-4740-5cbd-82aa-7e67e7c152da` | `explore/content/statements/newton-schulz-sign-iteration-33cd8a3d.md` | `f55ea43e3a3fd3543c37c7cb4e66434f2586d327c7c69a1dca6454391a5b4710` | `proposed` |
| `cdd691bb-6aef-5d59-b7e9-615785a98d27` | `explore/content/statements/nlalib-earlytruncatedgeneralizednystrom-cdd691bb.md` | `5166146074d8853c6b2e1b968d9ae6549299566e5c49b7015d7022673683b945` | `proposed` |
| `d1ee9b33-de78-5b4f-8a2d-d80147ea5587` | `explore/content/statements/nlalib-girardhutchinson-d1ee9b33.md` | `84fb40c9183a2762085e89aa50dc0f75334173be131566052b039c4ab1df90b2` | `proposed` |
| `21c93d07-2c81-555f-80b2-eff7e5316a67` | `explore/content/statements/nlalib-hessenbergreduction-21c93d07.md` | `939dc6bc58f7fd886ddf04e8547300df0722548679067dcc5c39dd84a9aa5dbd` | `already-consistent` |
| `b6d6ec43-d148-5545-bb84-195688281b33` | `explore/content/statements/nlalib-hutchpp-b6d6ec43.md` | `d87997d384e7924ffead08a37e767f1d6c2c6bca2041908dc65516d109a51927` | `proposed` |

## Notation and links

- **Newton–Schulz sign iteration**: linked the existing term “Hermitian” to the Hermitian spectral-decomposition definition, UUID `49f5c3f6-f926-5bc6-b401-16993ec1e357`. Its text defines the Hermitian condition using the adjoint and has no real-only field restriction. The matrix recurrence and scale/gap caveat remain unchanged.
- **Early-truncated GN**: changed the Greek matrix symbols `\mathbf\Omega` and `\mathbf\Psi` to `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}`. Linked the existing “singular values” term to UUID `581c9098-24f3-55b6-bd36-a47af48b21ff`; its definition applies to general real/complex matrices with adjoints. The declaration signature `NLAlib.earlyTruncatedGeneralizedNystrom` is `[RCLike 𝕜]`, consistent with that target. The formula and tie convention are otherwise unchanged.
- **Girard–Hutchinson estimator**: linked “isotropic probes” to UUID `cb5e0fa7-3425-5848-83bd-fd73b4aa314e`. That definition gives the second-moment condition with the Hermitian adjoint and does not impose a real-only field. The linked estimator declaration is `[RCLike 𝕜]`. The estimator and probability caveat are unchanged.
- **Hessenberg reduction**: already consistent for this scope. Matrix bolding and Hermitian transpose are explicit. No direct Householder-transformation definition target was found; no related algorithm was substituted. Its inherited citation is retained as recorded below.
- **Hutch++**: linked “orthogonal projector” to UUID `2fa76a05-ce3c-5a1c-9aee-625c01bfd829` and “Girard–Hutchinson estimate” to UUID `d1ee9b33-de78-5b4f-8a2d-d80147ea5587`. The projector definition directly matches `\mathbf{P}`; the estimator definition matches the residual trace estimate. Both targets use adjoint-compatible notation and do not restrict the source's `[RCLike 𝕜]` domain. The formulas, fresh-probe wording, and probability caveat are unchanged.

## Citation associations

The assigned objects have empty authored `object.references`; no inline citation strings occur in the prose. Inherited declaration references, checked at the pinned declaration records, are:

- `NLAlib.earlyTruncatedGeneralizedNystrom`: `TroppYurtseverUdellCevher2017`, §7.3.1 and equation (7.3).
- `NLAlib.girardHutchinson`: `Epperly2023`, “Girard–Hutchinson Estimator: The Basics.”
- `NLAlib.hessenbergReduction`: `GolubVanLoan2013`, edition 4, Algorithm 7.4.2.
- `NLAlib.hutchpp`: `MeyerMuscoMuscoWoodruff2021`, Algorithms 1 and 3; `EpperlyTroppWebber2024`, equation (1.3).
- Newton–Schulz sign iteration is authored without a declaration, so it has no inherited declaration citation.

These associations remain on their own declarations and were not copied to related entries. No references needed moving or new associations. IDs, UUIDs, formal bindings, formulas, domains, assumptions, metadata and math segmentation were preserved; no additional claims or helper expansions were introduced.

## Validation and unresolved items

Verified exact UUIDs and read each linked target definition. No field mismatch was found. The Hessenberg definition has no direct Householder transformation target; that link remains absent pending a dedicated definition. `node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; notation checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.

## Registry note

The early-truncated GN correction uses `\Omega` as a matrix, matching the declaration signature. No global notation registry edit was made.
