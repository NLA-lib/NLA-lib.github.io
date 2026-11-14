---
kind: algorithm
id: sketch-and-precondition
title: Sketch-and-precondition least squares
summary: Build a preconditioner from a sketch before solving the original problem.
status: outline
order: 21
theory:
- subspaces
- random-matrices
- sketching-theory
library_results: false
result_ids:
- sketch-and-precondition
- sketch-and-precondition-ls
- sketch-and-precondition-convergence
- sketch-and-precondition-realisation
---

Build a preconditioner from a sketch before solving the original problem.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Sketch-and-precondition least squares"
Use a sketch to construct a preconditioner, then solve the original least-squares objective in transformed coordinates. For example, if a thin QR factorization $\mathbf S\mathbf A=\mathbf Q\mathbf R$ has invertible $\mathbf R$, solve $\min_{\mathbf y}\|\mathbf A\mathbf R^{-1}\mathbf y-\mathbf b\|_2$ and recover $\mathbf x=\mathbf R^{-1}\mathbf y$. The sketch improves the coordinates; it does not replace the original objective.
:::



## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
