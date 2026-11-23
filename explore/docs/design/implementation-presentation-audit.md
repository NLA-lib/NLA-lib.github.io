# Implementation presentation review

Reviewed against published core `f329b7ffe514ce49cea33c00eb9f265a76447497`.

This is a presentation review, separate from the mathematical coverage audit. Coverage means
that an actual statement is rendered somewhere in the explorer. It does not establish that
important guarantees have readable summaries on the relevant implementation page, or that
all existing execution models have been connected to the arithmetic selector.

## Confirmed gaps

- Spectral bisection: `spectral-bisection-diagonalization-simple` was rendered on the canonical
  method page, but the Shah implementation showed only execution correspondence and a
  conditional accuracy transfer. Added the explicit precision theorem, parameter choices,
  floor/range conditions and numerical guarantee to the implementation, with source details.
  Moved the three numerical result groups from the strategy overview to this implementation;
  a stable overview URL does not make this a canonical exact-arithmetic method.
  The precision requirement is not a total bit-operation complexity theorem. Existing
  bounded-format and realizability results still need their own readable presentation.
- PCG: the standard implementation exposes exact arithmetic only. The source also contains
  stored rounded certificates (`NLAlib/Krylov/CG/HSPCG/FinitePrecision/StoredCertificate.lean`);
  these are not yet presented as implementation/model choices. This is a missing presentation
  of existing certificates, not a claim of a new convergence or stability theorem.
- Ordinary Lanczos: the ready page presents exact matrix-free execution. Stored and rounded
  certificates exist and are acknowledged in prose, but their models and detailed guarantees
  are not curated on that page.
- Lanczos with full reorthogonalization: the implementation page renders generated results,
  including orthogonality, backward-model and Ritz guarantees. It still lacks readable
  pseudocode and operation/storage/accuracy summaries tied to its particular execution model.
- Two-pass classical Gram–Schmidt: `gram-schmidt-cgs2-twice-is-enough` is rendered on the
  canonical Gram–Schmidt page. It needs a distinct two-pass presentation; it must not be
  advertised as a guarantee of the exact modified Gram–Schmidt implementation.

### Changes against library `5f2caad95458ad99d8b0e1f377bdce6feeb63eca`

These three points were checked against that snapshot only; the rest of this review still
refers to the core named at the top.

- Ordinary CG, ordinary Lanczos and Shah's spectral bisection now state their rounded
  operation-count theorems in authored blocks: `cg-scalar-rounded-operation-count-energy-error`,
  `lanczos-scalar-rounded-operation-count-ritz-residual` and
  `spectral-bisection-operation-count-accuracy`. The CG and Lanczos theorems are for stored
  scalar programs, so they have their own section and are not choices of a model selector.
- PCG: the implementation page no longer says that the library has no rounded theorem. It
  links `HSPCG.Rounded.solve_writes`, `HSPCG.Rounded.Stored.algorithm` and `countedAlgorithm`.
  A readable statement of the stored certificate and of its closed count is still missing.
- The finite-precision run-model results (13 `cg-*` and 13 `lanczos-*` result groups) are on
  the theory page `finite-precision-krylov` and on no implementation page. Stating one on an
  implementation needs its bridge from that program's execution to the run model.

### Changes against library `cleanup/smalleig` at `2abd9136`

These points were checked against that snapshot only (the SMALLEIG stage, not yet on main).

- Finite-precision shifted QR (BGS II) is ready. The eigenvalue-only oracle program of that
  snapshot was later removed from the library; see the current state below.
- Randomized shifted inverse iteration (BGS III), a new implementation of inverse iteration:
  Theorem 1.1 (`small-eig-backward-error`, unconditional), Corollary 1.3
  (`small-eig-forward-error`), the certificate `smallEigAlgorithm` and its one-run theorem. The
  guarantees of its blocks (`RHess`, `OneEig`, `DistSpec`, `Decouple`) are not presented.
- Theory: `pseudospectral-shattering` (new) and Ostrowski–Elsner on `perturbation-theory`. The
  shattering ingredients carry no `Result:` ids in the library, so they are placed by declaration.

### Changes against library `main` at `0c19b744`

- BGS II has one program under two models: any small-block Schur solver
  (`shifted-qr-rounded-schur-any-leaf`) and the BGS III program (`shifted-qr-rounded-schur`, the
  unconditional eigenvalue corollary and `shqrSmallEigAlgorithm`). The output is a Schur pair.
- BGS III states the Schur output, the leaf contract and the current certificate numeral.
- New implementation page `dense-schur`, "BGS + Dense Schur (end-to-end)", with the same two
  models and the `dense-schur-*` results. It also states the verified single-shot solver
  (`verified-schur-*`) and the generic residual check.
- The shattering page and the BGS II and III pages use the gap tail record
  $(2048e, 11/3, 2/3, 2)$.

There are 26 implementation pages: 12 marked ready in their headers and 14 outline/placeholder pages. The latter
are not evidence of missing proofs by themselves: some have mathematical results without a
matching certified execution, and some have existing certificates awaiting presentation.
The review above identifies concrete gaps; it is not an assertion that every prose statement
or all execution-model combinations have been exhaustively reviewed.

- Late-truncated GN: the page highlighted an older sufficient sketch-size bound and mixed
  notation from authored and generated statements. The published snapshot already contains
  the stronger sufficient regime of range width at least 200k/epsilon and co-range width at
  least 14 times the range width. The page now leads with that theorem and distinguishes
  the hard-instance lower bound, using the same GN and rank-truncation notation throughout.

## Review criteria

For each implementation, review its actual source guarantees and ask whether the page explains:

1. The algorithm and the exact quantity or approximation returned.
2. Work and storage, with the arithmetic costs and representation explicit.
3. Accuracy or convergence, including precision, probability, range and stopping assumptions.
4. Which statements concern a mathematical run model and which certify stored execution.
5. Which proved arithmetic/representation alternatives are exposed, and which remain uncurated.

A generic result listing establishes discoverability, not completion of this checklist.
