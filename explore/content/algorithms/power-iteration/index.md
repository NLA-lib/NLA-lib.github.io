---
kind: algorithm
id: power-iteration
title: Power iteration
summary: Repeatedly apply an operator to approximate a dominant eigenvector.
status: outline
theory:
- spectral-theory
- matrix-norms
result_ids:
- power-iteration
- random-start-power
---

::: definition name="Power iteration"
For a square matrix $\mathbf A$ and a nonzero starting vector, repeatedly set $\mathbf y_{j+1}=\mathbf A\mathbf x_j$ and normalize $\mathbf x_{j+1}=\mathbf y_{j+1}/\|\mathbf y_{j+1}\|_2$ whenever the numerator is nonzero. A Rayleigh quotient supplies an eigenvalue estimate. Convergence requires spectral and starting-vector assumptions.
:::

## Implementations

{{ generated:implementations }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
