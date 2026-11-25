---
uid: 2e0370c5-dfb6-5566-a7d4-1cd0e423a125
kind: algorithm
id: lanczos-matrix-function
title: Lanczos matrix-function approximation
summary: Run Lanczos, evaluate $f$ on the small tridiagonal matrix, and lift the result to approximate
  $f(A)b$.
status: outline
order: 2
theory:
- matrix-polynomials
- polynomial-approximation
uses:
- lanczos
library_results: false
result_ids:
- lanczos-fa-exactness
- lanczos-fa-formula
- lanczos-fa-interpolation
- lanczos-fa-kernel-near-optimality
- lanczos-fa-near-optimality
- lanczos-fa-near-optimality-lower-bound
- lanczos-fa-uniform-bound
- lanczos-fa-recurrence
- lanczos-fa-cg
---

Run Lanczos, evaluate $f$ on the small tridiagonal matrix, and lift the result to approximate $f(A)b$.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:nlalib-lanczosfa-bc762b7b }}



## Components

{{ generated:components }}

## Mathematical guarantees

{{ statement:lanczos-fa-uniform-bound }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
