---
kind: task
id: matrix-factorizations
title: Matrix factorizations and bases
summary: Construct orthogonal bases, triangular factors, or spectral factorizations.
status: ready
order: 8
theory:
- matrix-analysis
- subspaces
- singular-values
groups:
- id: triangular
  title: Triangular factorizations
  summary: Use matrix structure or row pivoting to obtain triangular factors.
  algorithms:
  - cholesky
  - lu
  - plu
  - pivoted-cholesky
  family: matrix-factorizations
- id: orthogonal
  title: Orthogonal factors and bases
  summary: Construct orthonormal columns and the corresponding triangular coefficients.
  algorithms:
  - qr
  - gram-schmidt
  - block-golub-kahan
  summaries:
    qr: Specify orthogonal and triangular factors of a matrix.
    gram-schmidt: Construct a basis by successive orthogonal projections; classical and modified orderings
      are implementations.
    block-golub-kahan: Build left and right block Krylov bases and banded coefficients from products with
      a matrix and its adjoint.
- id: singular-values
  title: Singular-value decompositions
  summary: Expose singular values, singular vectors, rank, and low-rank truncations.
  algorithms:
  - svd
- id: polar
  title: Polar decomposition methods
  summary: Construct the partial-isometry factor with inverse averaging or polynomial singular-value updates.
  algorithms:
  - polar-newton
  - polar-newton-schulz
  - polar-minimax-polynomial
  family: polar-iterations
---

Construct orthogonal bases, triangular factors, or spectral factorizations.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
