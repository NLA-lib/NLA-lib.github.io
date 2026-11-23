---
kind: task
id: linear-systems
title: Linear systems
summary: Solve $A x=b$, including preconditioned and matrix-free methods.
status: ready
sections_collapsed: true
order: 0
theory:
- matrix-analysis
- krylov-spaces
- polynomial-approximation
groups:
- id: galerkin
  title: Galerkin methods
  summary: Choose the iterate by requiring the residual to be orthogonal to the trial space.
  algorithms:
  - conjugate-gradient
  - preconditioned-conjugate-gradient
  - block-conjugate-gradient
  - fom
  family: galerkin-methods
- id: residual-minimization
  title: Residual minimization
  summary: Minimize the residual norm over a growing Krylov search space.
  algorithms:
  - gmres
  - minres
  - preconditioned-minres
  family: residual-minimization-methods
- id: direct
  title: Direct factorization methods
  summary: Factor the coefficient matrix, then solve triangular systems. The matrix structure and pivoting
    conditions determine which factors are available.
  algorithms:
  - cholesky
  - plu
  - lu
  family: matrix-factorizations
- id: refinement
  title: Iterative refinement
  summary: Improve a computed solution through its residual, with the factorization, residual and update
    each in its own precision.
  algorithms:
  - iterative-refinement
- id: stationary
  title: Stationary iterations
  summary: Apply a fixed correction map to successive residuals.
  algorithms:
  - richardson-iteration
- id: random-projections
  title: Randomized projection methods
  summary: Correct iterates using sampled rows or sketched equations.
  algorithms:
  - randomized-kaczmarz
  - sketch-and-project
---

Solve $A x=b$, including preconditioned and matrix-free methods.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
