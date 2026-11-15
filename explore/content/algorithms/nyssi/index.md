---
kind: algorithm
id: nyssi
title: Nyström subspace iteration
summary: Use subspace iteration in a Nyström approximation.
status: outline
order: 17
theory:
- matrix-polynomials
- random-matrices
library_algorithm: nyssi
uses:
- nystrom
---

Use subspace iteration in a Nyström approximation.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Nyström subspace iteration"
For Hermitian positive-semidefinite $\mathbf A$, replace the test matrix in the Nyström approximation by $\mathbf A^p\mathbf\Omega$, with $p\ge0$. The powers emphasize dominant spectral directions. The result is $\mathsf{nystrom}(\mathbf A,\mathbf A^p\mathbf\Omega)$; the choice of stable intermediate bases belongs to a concrete implementation.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
