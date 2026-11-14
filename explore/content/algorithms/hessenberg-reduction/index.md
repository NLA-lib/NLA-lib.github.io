---
kind: algorithm
id: hessenberg-reduction
title: Hessenberg reduction
summary: Reduce a square matrix by Householder similarities before a QR eigensolve.
status: outline
library_algorithm: hessenberg-reduction
library_results: false
result_ids:
- hessenberg-reduction
theory:
- spectral-theory
- matrix-factorization-theory
search_aliases:
- Hessenberg reduction
---

::: definition decl:NLAlib.hessenbergReduction name="Hessenberg reduction"
For a square $\mathbf A$, accumulate Householder similarities to obtain a unitary $\mathbf Q$ and upper-Hessenberg $\mathbf H=\mathbf Q^{\mathsf{H}}\mathbf A\mathbf Q$. The mathematical construction uses $n-2$ similarities; for $n\le2$ it returns $(\mathbf I,\mathbf A)$. It changes the representation of the eigenproblem, not its eigenvalues.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
