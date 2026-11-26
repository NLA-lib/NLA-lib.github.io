---
uid: 3167e31e-d610-5fd2-a00b-a65764d0904b
kind: task
id: matrix-factorizations
title: Matrix factorizations and bases
summary: Construct orthogonal bases, triangular factors, or spectral factorizations.
status: ready
sections_collapsed: true
order: 8
theory:
- matrix-analysis
- subspaces
- singular-values
groups:
- id: triangular
  title: Dense triangular factorizations
  summary: Cholesky, LDL and LU implementations, including blocked execution, singular positive-semidefinite inputs, and row or two-sided pivoting.
  algorithms:
  - cholesky
  - ldl
  - lu
  - plu
  - pluq
  - pivoted-cholesky
  family: matrix-factorizations
- id: orthogonal
  title: Orthogonal factors and bases
  summary: Construct orthonormal columns and the corresponding triangular coefficients.
  algorithms:
  - qr
  - gram-schmidt
  summaries:
    qr: Specify orthogonal and triangular factors of a matrix.
    gram-schmidt: Construct a basis by successive orthogonal projections; classical and modified orderings
      are implementations.
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

The dense triangular factorization pages below lead to the actual scalar and blocked
implementations, their arithmetic models, input conditions, and certified work and storage.
Cholesky uses positive-definite or positive-semidefinite structure; LDL uses one-by-one
diagonal pivots; the LU family provides unpivoted, partial, threshold, scaled, complete
and rook pivoting choices.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
