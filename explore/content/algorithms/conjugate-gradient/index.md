---
uid: 862c8ba9-521b-5555-955e-1d6459e64017
kind: algorithm
id: conjugate-gradient
title: Conjugate gradient (CG)
summary: Solve a symmetric positive-definite system $\mathbf{A}\mathbf{x}=\mathbf{b}$ using a short Krylov recurrence.
status: ready
order: 0
theory:
- krylov-spaces
- polynomial-approximation
- spectral-theory
- chebyshev-polynomials
- finite-precision-krylov
library_algorithm: cg
families:
- galerkin-methods
search_aliases:
- Hestenes–Stiefel
- HSCG
- conjugate gradients
- matrix-free CG
- finite precision CG
source_guides:
- docs/algorithms/Conjugate-Gradient.md
library_results: false
result_ids:
- cg-optimality
- cg-chebyshev-bound
- cg-chebyshev-sharp
- cg-polynomial-bound
- cg-finite-termination
- cg-galerkin-condition
- cg-galerkin-formula
- cg-near-optimality
- cg-near-optimality-lower-bound
- cg-orthogonality
- cg-outlier-bound
- cg-recurrence
- cg-spectrum-minimax-bound
- cg-spectrum-minimax-sharp
- cg-lanczos
- cg-error-gauss-quadrature
- cg-error-gauss-radau-bounds
---

Solve a symmetric positive-definite system $\mathbf{A}\mathbf{x}=\mathbf{b}$ using a short Krylov recurrence.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Mathematical CG in exact arithmetic

Let $\mathbf{A}$ be symmetric positive definite, let $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$, and write $\mathbf{x}_k$ for the mathematical CG iterate from $\mathbf{x}_0$. The energy norm is $\|\mathbf{v}\|_\mathbf{A}^2=\mathbf{v}^{\mathsf{T}}\mathbf{A}\mathbf{v}$.

{{ statement:cg-optimality }}

{{ statement:cg-chebyshev-bound }}

{{ statement:cg-polynomial-bound }}

{{ statement:cg-finite-termination }}

## Used by other algorithms

{{ generated:applications }}

## Further mathematical results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}



## Family

{{ generated:families }}
