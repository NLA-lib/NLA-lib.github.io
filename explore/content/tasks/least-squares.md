---
kind: task
id: least-squares
title: Solve least-squares problems
summary: Minimize $\|A x-b\|_2$, exactly or using a sketch.
status: ready
order: 2
theory:
- matrix-analysis
- pseudoinverses
- subspaces
groups:
- id: krylov
  title: Krylov least-squares methods
  summary: Use matrix-vector products with the matrix and its adjoint to solve the least-squares problem
    iteratively.
  algorithms:
  - lsqr
  - cgls
  family: residual-minimization-methods
- id: sketched
  title: Sketch-based solvers
  summary: Either solve a compressed problem or use a sketch to precondition a solve of the original problem.
  algorithms:
  - sketch-and-solve
  - sketch-and-precondition
  - iterative-sketching
- id: factorizations
  title: Factorization-based solvers
  summary: Use orthogonal factors or singular values to solve the least-squares problem; rank deficiency
    changes the solution characterization.
  algorithms:
  - qr
  - svd
  family: matrix-factorizations
  summaries:
    qr: Use the orthogonal and triangular factors for a least-squares solve.
    svd: Use singular values and singular vectors to characterize least-squares and minimum-norm solutions.
- id: gradient
  title: Gradient and row-action methods
  summary: Use adjoint residual steps or projections onto sampled equations.
  algorithms:
  - landweber-iteration
  - randomized-kaczmarz
---

Minimize $\|A x-b\|_2$, exactly or using a sketch.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
