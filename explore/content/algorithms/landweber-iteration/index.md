---
kind: algorithm
id: landweber-iteration
title: Landweber iteration
summary: Apply gradient steps to a linear least-squares objective.
status: outline
result_ids:
- landweber-spectral-filter
theory:
- singular-values
- matrix-polynomials
---

::: definition name="Landweber iteration"
For $\min_{\mathbf x}\|\mathbf A\mathbf x-\mathbf b\|_2^2$, choose a real step $\eta$ and set $\mathbf x_{j+1}=\mathbf x_j+\eta\mathbf A^{\mathsf{H}}(\mathbf b-\mathbf A\mathbf x_j)$. The finite-step spectral-filter identity holds without asserting stability of the chosen step; convergence needs an appropriate step-size condition.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
