---
kind: algorithm
id: deflation
title: Randomized subspace extraction (deflation)
summary: Project a random sample through a matrix and extract a basis using QR.
status: outline
order: 28
theory:
- subspaces
- spectral-theory
library_algorithm: deflate
search_aliases:
- DEFLATE
- Gaussian range finder
- randomized range finder without oversampling
source_guides:
- docs/algorithms/Sign-Deflation.md
uses:
- qr
---

The deflation component used by spectral bisection extracts a basis from a sampled matrix image. It is distinct from locking already converged eigenvectors in an iterative eigensolver.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Randomized subspace extraction"
For a square input $\mathbf P$, draw a complex sample matrix $\mathbf G$, form $\mathbf Y=\mathbf P\mathbf G$, compute a full QR factorization, and retain the requested number of columns of its orthonormal factor. Accuracy as a subspace basis requires assumptions on the matrix, sampling, and arithmetic.
:::



## Results

{{ generated:results }}

## Components

{{ generated:components }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
