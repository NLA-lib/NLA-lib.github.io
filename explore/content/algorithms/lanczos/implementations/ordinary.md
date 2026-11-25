---
uid: 3e7d27af-bd22-5270-936a-7b40d902c55a
kind: implementation
id: ordinary
algorithm: lanczos
title: Ordinary Lanczos
summary: The guarded three-term recurrence with a matrix-free operator and exact vector operations.
status: ready
order: 3
library_algorithm: lanczos
library_results: false
arithmetic_models:
- id: exact
  arithmetic: exact
  program: blas-matvec
- id: standard
  arithmetic: standard
  program: blas-matvec
- id: stored-scalar
  arithmetic: standard
  program: stored-scalar
source_guides:
- docs/algorithms/Lanczos.md
---

This page describes the real, matrix-free three-term program. It stores a basis and tridiagonal coefficients; extracting eigenvalues or evaluating a matrix function is a subsequent algorithm.

{{ generated:source-guides }}

## Algorithm

{{ statement:nlalib-krylov-lanczos-solve-8a730a7c }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The first two models are for the program of the listing, in which the matrix–vector product is an abstract operator call with its own work and workspace costs and the matrix is not a resident buffer. They differ in what the operations may return. The third model is for a program lowered from it: the matrix is stored entry by entry, and every matrix–vector product and vector operation is written out as scalar loops, so its only primitives are scalar operations and comparisons.

::: model exact
The result below uses exact real scalar arithmetic, exact dot products, vector updates, copies and normalization, and an exact application of $\mathbf{A}$. Matvec is an abstract operator call with its own work and workspace costs. The matrix itself is not supplied as a resident dense buffer in this program.
::: end-model

::: model standard
The operations form a standard operation model (`Ops.Standard.Model`): a scalar machine in the standard model with unit roundoff $u$, level-one vector operations whose dot products are [summed sequentially](/explore/arithmetic-models/#sequential), and a matrix–vector product with a normwise error allowance. The program is the same as in exact arithmetic. The Lean certificate is stated for any scheme of the standard profiles.
::: end-model

::: model stored-scalar
Scalar arithmetic is any machine in the standard model with unit roundoff $u$, and comparisons of stored numbers are exact. The certified program is `Krylov.Lanczos.Stored.Rounded.scalarProgram`: the listing with each vector operation and each matrix–vector product replaced by scalar loops over the stored entries. Its work is a count of instructions.
::: end-model

## Operations and Storage

These budgets are at the level of vector operations and hold for the two models built from BLAS and matvec calls. The stored scalar program has its own instruction count, stated with its theorem.

{{ statement:nlalib-krylov-lanczos-stmtcost-solve }}

{{ statement:nlalib-krylov-lanczos-stmtpeak-solve-le }}

## Accuracy

::: model exact
{{ statement:nlalib-krylov-lanczos-runs-solve }}
::: end-model

::: model standard
{{ statement:nlalib-krylov-lanczos-certification-algorithm-bdfac892 }}

{{ statement:nlalib-krylov-lanczos-certification-ritzalgorithm-78fee89f }}
::: end-model

::: model stored-scalar
{{ statement:lanczos-scalar-rounded-operation-count-ritz-residual }}
::: end-model

## Not yet presented

- The explicit Ritz residual bound of the rounded certificate; it is stated here only for the stored scalar program.
- The exact and the BLAS-level rounded certificates of the stored program, in which the matrix is stored and the vector operations remain primitives, and the certificate of the program linked with sequential BLAS.
- The finite-precision results about the Lanczos run model are on the theory page [finite-precision Krylov methods](/explore/theory/finite-precision-krylov/), not on this page.

## Mathematical method

{{ generated:mathematical-method }}
