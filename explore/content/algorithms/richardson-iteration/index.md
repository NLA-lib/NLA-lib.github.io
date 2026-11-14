---
kind: algorithm
id: richardson-iteration
title: Richardson iteration
summary: Update an iterate with a preconditioned residual.
status: outline
result_ids:
- richardson-iteration
theory:
- spectral-theory
- matrix-equations
---

::: definition name="Richardson iteration"
For $\mathbf A\mathbf x=\mathbf b$ and a fixed correction map $\mathbf M$, set $\mathbf x_{j+1}=\mathbf x_j+\mathbf M(\mathbf b-\mathbf A\mathbf x_j)$. A step size can be absorbed into $\mathbf M$. Defining the recurrence requires no convergence claim; the spectral hypotheses of the result below determine when the error decreases.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
