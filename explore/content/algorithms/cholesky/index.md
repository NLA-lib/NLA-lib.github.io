---
kind: algorithm
id: cholesky
title: Cholesky factorization
summary: Construct a triangular factor of a positive-definite matrix.
status: outline
order: 24
theory:
- spectral-theory
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- cholesky-existence
---

Construct a triangular factor of a positive-definite matrix.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Cholesky factorization"
For Hermitian positive-definite $\mathbf A$, a Cholesky factorization has the form $\mathbf A=\mathbf L\mathbf L^{\mathsf{H}}$, where $\mathbf L$ is lower triangular with positive real diagonal. The upper-triangular convention uses $\mathbf A=\mathbf R^{\mathsf{H}}\mathbf R$. Solving with these factors requires two triangular solves.
:::



## Mathematical guarantees

::: theorem result:cholesky-existence name="Existence of Cholesky factors"
A square matrix admits a Cholesky factor with positive real diagonal exactly when it is positive definite. This characterizes existence of the mathematical factorization; a rounded implementation needs a separate execution and accuracy result.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
