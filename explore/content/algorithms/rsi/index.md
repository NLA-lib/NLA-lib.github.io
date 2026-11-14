---
kind: algorithm
id: rsi
title: Randomized subspace iteration
summary: Apply power iterations to improve a randomized range approximation.
status: outline
order: 11
theory:
- matrix-polynomials
- random-matrices
- randomized-low-rank-theory
library_algorithm: rsi
uses:
- randomized-svd
---

Apply power iterations to improve a randomized range approximation.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Randomized subspace iteration"
Choose a test matrix $\mathbf\Omega$ and a nonnegative power count $p$. Form

$$\mathbf Y=\mathbf A(\mathbf A^{\mathsf{H}}\mathbf A)^p\mathbf\Omega,\qquad\mathbf B=\mathbf P_{\mathbf Y}\mathbf A.$$

Here $\mathbf P_{\mathbf Y}$ is the orthogonal projector onto the sampled range. With $p=0$ this is the ordinary range-finder approximation. Intermediate orthogonalization controls the numerical loss of directions and belongs to the implementation. For Hermitian positive-semidefinite matrices, the range also approximates a dominant invariant subspace.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
