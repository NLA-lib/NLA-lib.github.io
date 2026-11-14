---
kind: algorithm
id: sketch-and-solve
title: Sketch-and-solve least squares
summary: Solve a compressed least-squares problem produced by a sketch.
status: outline
order: 20
theory:
- subspaces
- pseudoinverses
- random-matrices
- sketching-theory
library_algorithm: sketch-and-solve
search_aliases:
- sketched least squares
---

Solve a compressed least-squares problem produced by a sketch.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.sketchAndSolve name="Sketch-and-solve least squares"
Replace the original problem by $\min_{\mathbf x}\|\mathbf S\mathbf A\mathbf x-\mathbf S\mathbf b\|_2$ and return the minimum-norm solution

$$\widehat{\mathbf x}=(\mathbf S\mathbf A)^{\dagger}\mathbf S\mathbf b.$$

The solution minimizes the sketched residual. Relating it to the original residual requires assumptions on the sketch.
:::



## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
