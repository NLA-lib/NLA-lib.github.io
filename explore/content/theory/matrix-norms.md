---
kind: theory
id: matrix-norms
title: Matrix norms
summary: Spectral, Frobenius, nuclear, and Schatten norms.
status: outline
order: 1
parents:
- matrix-analysis
module_prefixes:
- NLAlib.Matrix.Norms
---

A norm specifies what it means for a matrix approximation to be accurate. Spectral norm measures the worst error on a unit vector; Frobenius norm measures the combined entrywise error; nuclear norm sums the singular values. Different algorithms and applications naturally control different norms.

::: definition name="Matrix norms"
For $\mathbf A\in\mathbb C^{m\times n}$,

$$\|\mathbf A\|_2=\sup_{\|\mathbf x\|_2=1}\|\mathbf A\mathbf x\|_2,\qquad\|\mathbf A\|_{\mathrm F}=\left(\sum_{i,j}|\mathbf A_{ij}|^2\right)^{1/2},\qquad\|\mathbf A\|_*=\sum_j\sigma_j(\mathbf A).$$

For $1\le p<\infty$, the Schatten $p$-norm is $(\sum_j\sigma_j(\mathbf A)^p)^{1/p}$. These norms provide different comparisons with a best low-rank approximation.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
