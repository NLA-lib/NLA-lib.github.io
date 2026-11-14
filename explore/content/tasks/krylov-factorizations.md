---
kind: task
id: krylov-factorizations
title: Krylov factorizations
summary: Construct orthonormal Krylov bases and Hessenberg or tridiagonal factorizations.
status: ready
order: 9
theory:
- krylov-spaces
- subspaces
- matrix-polynomials
groups:
- id: factorizations
  title: Arnoldi and Lanczos
  summary: Factor the action of a matrix on a growing Krylov basis. The coefficient matrix is upper Hessenberg in general and tridiagonal in the Hermitian case.
  algorithms:
  - arnoldi
  - lanczos
---

Arnoldi and Lanczos construct Krylov factorizations. Linear-system methods, eigenvalue approximations, matrix-function actions, and quadrature can use these shared constructions. A factorization is not by itself a complete method for each of those tasks.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
