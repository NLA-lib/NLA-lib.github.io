---
uid: 7245c6e6-d6bd-5538-9a33-1ce3d67af879
kind: task
id: krylov-factorizations
title: Krylov factorizations
summary: Construct orthonormal Krylov bases and Hessenberg, tridiagonal, or bidiagonal factorizations.
status: ready
order: 9
theory:
- krylov-spaces
- subspaces
- matrix-polynomials
groups:
- id: factorizations
  title: Arnoldi, Lanczos, and Golub–Kahan
  summary: Factor the action of a matrix on a growing Krylov basis. The coefficient matrix is upper Hessenberg in general and tridiagonal in the Hermitian case. For a rectangular matrix, products with the matrix and its adjoint give a pair of bases and a bidiagonal coefficient matrix, banded in the block form.
  algorithms:
  - arnoldi
  - lanczos
  - golub-kahan
---

Arnoldi, Lanczos, and Golub–Kahan construct Krylov factorizations. Linear-system methods, eigenvalue approximations, matrix-function actions, quadrature, and low-rank approximation can use these shared constructions. A factorization is not by itself a complete method for each of those tasks.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
