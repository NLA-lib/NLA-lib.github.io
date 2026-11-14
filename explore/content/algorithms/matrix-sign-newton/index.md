---
kind: algorithm
id: matrix-sign-newton
title: Newton matrix-sign iteration
summary: Use inverse averaging to compute a matrix sign.
status: outline
library_algorithm: matrix-sign-newton
library_results: false
result_ids:
- matrix-sign-newton
theory:
- matrix-functions
- singular-values
search_aliases:
- Newton matrix-sign iteration
---

::: definition decl:NLAlib.signNewtonIterate name="Newton matrix-sign iteration"
Start from $\mathbf X_0=\mathbf A$ and set $\mathbf X_{j+1}=\tfrac12(\mathbf X_j+\mathbf X_j^{-1})$. The convergence theorem requires spectral separation from the imaginary axis and establishes invertibility of the relevant iterates. This inverse-averaging method differs from the inverse-free Newton–Schulz sign update.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
