---
kind: algorithm
id: qr
title: QR factorization
summary: Factor a matrix into an orthogonal basis and a triangular factor.
status: outline
order: 23
theory:
- subspaces
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- givens-qr
- least-squares-qr
---

Factor a matrix into an orthogonal basis and a triangular factor.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="QR factorization"
For $\mathbf A\in\mathbb C^{m\times n}$ with $m\ge n$, a thin QR factorization is $\mathbf A=\mathbf Q\mathbf R$, where $\mathbf Q^{\mathsf{H}}\mathbf Q=\mathbf I$ and $\mathbf R$ is upper triangular. Full QR extends $\mathbf Q$ to a unitary basis. Rank deficiency permits zero diagonal entries of $\mathbf R$. Householder transformations, Givens rotations, and Gram–Schmidt are different ways to compute factors; QR eigenvalue iteration is a separate algorithm.
:::



## Results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
