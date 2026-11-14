---
kind: algorithm
id: newton-schulz-sign
title: Newton–Schulz sign iteration
summary: Use a polynomial iteration to approximate a matrix sign function.
status: outline
order: 27
theory:
- matrix-polynomials
- polynomial-approximation
library_algorithm: newton-schulz-sign
search_aliases:
- matrix sign function
- SIGN
- inverse-free sign iteration
- Newton–Schulz
source_guides:
- docs/algorithms/Sign-Deflation.md
---

Use a polynomial iteration to approximate a matrix sign function.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Newton–Schulz sign iteration"
Scale a Hermitian matrix to obtain an initial iterate $\mathbf X_0$, then apply

$$\mathbf X_{j+1}=\tfrac12\mathbf X_j(3\mathbf I-\mathbf X_j^2).$$

The scalar polynomial has fixed points at $-1$, $0$, and $1$. Approximating the matrix sign requires a suitable initial scale and a spectral gap away from zero. A capped implementation returns a defined iterate even when its numerical convergence conditions have not been established.
:::



## Results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
