---
kind: algorithm
id: randomized-kaczmarz
title: Randomized Kaczmarz
summary: Project onto sampled row equations using squared-row-norm sampling.
status: outline
result_ids:
- randomized-kaczmarz
- kaczmarz-inconsistent
- kaczmarz-rank-deficient
theory:
- subspaces
- probability
- pseudoinverses
---

::: definition name="Randomized Kaczmarz"
For a real linear system, choose row $i$ independently with probability proportional to its squared norm. Project the current iterate onto $(\mathbf A\mathbf x)_i=b_i$. If $\mathbf a_i$ is the transpose of row $i$, the update is $\mathbf x\leftarrow\mathbf x+\frac{b_i-(\mathbf A\mathbf x)_i}{\|\mathbf a_i\|_2^2}\mathbf a_i$. A zero row leaves the iterate unchanged. Consistent, inconsistent, and rank-deficient systems have different guarantees.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
