---
kind: algorithm
id: sketch-and-project
title: Sketch-and-project
summary: Project an iterate onto a sketched system of equations.
status: outline
result_ids:
- sketch-and-project
theory:
- subspaces
- sketching-theory
- pseudoinverses
---

::: definition name="Sketch-and-project"
For a sequence of sketches $\mathbf S_j$, set $\mathbf x_{j+1}=\mathbf x_j+(\mathbf S_j\mathbf A)^\dagger\mathbf S_j(\mathbf b-\mathbf A\mathbf x_j)$. This is a minimum-norm correction for the sketched residual. Convergence results specify consistency, the starting error, independence, and a lower bound on the mean projected row-space operator.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
