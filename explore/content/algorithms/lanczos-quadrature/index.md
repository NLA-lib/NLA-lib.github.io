---
kind: algorithm
id: lanczos-quadrature
title: Lanczos quadrature
summary: Use the Lanczos compression to approximate a quadratic form $b^{\mathsf T}f(A)b$.
status: outline
order: 3
theory:
- orthogonal-polynomials
- spectral-theory
uses:
- lanczos
library_results: false
result_ids:
- lanczos-gauss-quadrature
---

Use the Lanczos compression to approximate a quadratic form $b^{\mathsf T}f(A)b$.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.lanczosQuadrature name="Lanczos quadrature"
For Hermitian $\mathbf A$ and nonzero $\mathbf b$, approximate the quadratic form by

$$\mathbf b^{\mathsf{H}}f(\mathbf A)\mathbf b\approx\|\mathbf b\|_2^2\mathbf e_1^{\mathsf{H}}f(\mathbf T_k)\mathbf e_1.$$

The eigenvalues of the Lanczos compression $\mathbf T_k$ provide quadrature nodes; the squared first components of its normalized eigenvectors provide weights. The function, interval, and derivative assumptions determine which error bounds apply.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
