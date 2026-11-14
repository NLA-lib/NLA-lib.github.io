---
kind: algorithm
id: iterative-sketching
title: Iterative sketching
summary: Use a fixed sketched Gram matrix to precondition repeated least-squares corrections.
status: outline
result_ids:
- iterative-sketching-convergence
theory:
- sketching-theory
- pseudoinverses
---

::: definition name="Iterative sketching"
Fix a sketch $\mathbf S$, form $\mathbf G=(\mathbf S\mathbf A)^{\mathsf{H}}\mathbf S\mathbf A$, and update $\mathbf x_{j+1}=\mathbf x_j+\omega\mathbf G^\dagger\mathbf A^{\mathsf{H}}(\mathbf b-\mathbf A\mathbf x_j)$. The same sketch is reused in every step. A positive step alone does not ensure convergence; the embedding bounds and damping parameter must give a contraction.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
