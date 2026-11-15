---
kind: task
id: matrix-functions
title: Matrix functions
summary: Approximate $f(A)b$ or evaluate a matrix function.
status: ready
order: 4
theory:
- matrix-polynomials
- polynomial-approximation
- spectral-theory
groups:
- id: krylov-actions
  title: Krylov approximation of matrix-function actions
  summary: Approximate the action on a starting vector through a small compression.
  algorithms:
  - lanczos-matrix-function
- id: matrix-iterations
  title: Matrix iterations
  summary: Evaluate a matrix function through repeated matrix transformations.
  algorithms:
  - newton-schulz-sign
  - matrix-sign-newton
- id: compressions
  title: Shared Krylov constructions
  summary: Build the compression used by the action approximation. The Lanczos process has one shared
    page across tasks.
  algorithms:
  - lanczos
  summaries:
    lanczos: Build the tridiagonal matrix on which the function will be evaluated.
---

Approximate $f(A)b$ or evaluate a matrix function.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
