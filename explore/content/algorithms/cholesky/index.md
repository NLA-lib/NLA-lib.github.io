---
uid: c70cbd4f-5c0e-5366-9a6a-add845b7cc9f
kind: algorithm
id: cholesky
title: Cholesky factorization
summary: Construct a triangular Gram factor of a positive-definite or positive-semidefinite matrix.
status: ready
order: 24
theory:
- spectral-theory
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- cholesky-existence
- cholesky-backward-error
---

Cholesky factorization writes $\mathbf A=\mathbf L\mathbf L^{\mathsf T}$ with a lower triangular factor. Positive-definite input has a positive factor diagonal; the zero-guarded semidefinite implementation also handles singular PSD input with nonnegative diagonal. The ordinary scalar implementation exposes exact, relative-rounding and guarded finite-range guarantees; the blocked implementation uses an actual LU-to-Cholesky adapter.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:cholesky-factorization-d00946c1 }}



## Mathematical guarantees

{{ statement:cholesky-existence }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
