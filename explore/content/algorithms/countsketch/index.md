---
kind: algorithm
id: countsketch
title: CountSketch
summary: Use a sparse randomized embedding to compress a vector or matrix.
status: outline
order: 29
theory:
- random-matrices
- concentration
- sketching-theory
library_results: false
result_ids:
- countsketch-second-moment
- countsketch-jl-moment
- countsketch-osi
- amm-countsketch
---

Use a sparse randomized embedding to compress a vector or matrix.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.countSketchMatrix name="CountSketch"
Choose a hash $h:\{1,\ldots,n\}\to\{1,\ldots,s\}$ and signs $\sigma_i\in\{-1,1\}$. Define $\mathbf S_{a,i}=\sigma_i$ when $h(i)=a$, and zero otherwise. Each input coordinate contributes to one output bucket. The standard law uses uniform independent hash values and independent Rademacher signs; embedding guarantees specify the required output dimension.
:::



## Mathematical guarantees

::: theorem result:countsketch-second-moment name="Exact squared Gram error"
Let $\mathbf U\in\mathbb R^{n\times d}$ have orthonormal columns, and let $\mathbf S$ be a standard CountSketch with $s\ge1$ rows. Write $\ell_i=\|\mathbf U_{i,:}\|_2^2$ for its leverage scores. Then

$$\mathbb E\|(\mathbf S\mathbf U)^{\mathsf T}\mathbf S\mathbf U-\mathbf I\|_{\mathrm F}^2=\frac{d^2+d-2\sum_i\ell_i^2}{s}.$$

This is the real specialization of the checked real-or-complex identity. It gives the exact mean squared distortion of the subspace Gram matrix.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
