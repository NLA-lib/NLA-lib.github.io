---
kind: algorithm
id: randomized-svd
title: Range-finder approximation (RSVD)
summary: Project the matrix onto the full range of its sketch.
status: outline
order: 10
theory:
- singular-values
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
library_algorithm: randomized-svd
families:
- rsvd-type-methods
library_results: false
result_ids:
- range-finder-structural-bound
- randomized-svd-expected-error
- randomized-svd-tail
- randomized-svd-lower-bound
search_aliases:
- randomized range finder
- RSVD
---

Let $\mathbf Y=\mathbf A\mathbf\Omega$ and let $\mathbf P_{\mathbf Y}$ be the orthogonal projector onto its range.

::: definition decl:NLAlib.rsvd name="Range-finder approximation"
The untruncated approximation is $\mathbf B=\mathbf P_{\mathbf Y}\mathbf A$. Its rank is at most the sketch width; a target rank $k$ is not imposed at this stage.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

::: theorem result:randomized-svd-expected-error name="Expected Frobenius error"
For a real matrix $\mathbf A$, a standard Gaussian test matrix $\mathbf\Omega\in\mathbb R^{n\times\ell}$, and $k+2\le\ell$,

$$\mathbb E\|\mathbf A-\mathbf P_{\mathbf A\mathbf\Omega}\mathbf A\|_{\mathrm F}^2\le\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}^2.$$

Here $[\mathbf A]_k$ is a best rank-at-most-$k$ approximation. Increasing the sketch width above $k$ reduces the multiplicative excess over the optimal squared error.
:::

The range approximation is the common starting point for late truncation. Early truncation instead selects a smaller subspace from the sketch before projecting the matrix.

{{ generated:results }}



## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
