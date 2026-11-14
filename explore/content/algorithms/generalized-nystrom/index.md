---
kind: algorithm
id: generalized-nystrom
title: Generalized Nyström (GN)
summary: Use two sketches to construct a low-rank approximation of a general matrix.
status: outline
order: 15
theory:
- pseudoinverses
- random-matrices
- randomized-low-rank-theory
library_algorithm: generalized-nystrom
library_results: false
result_ids:
- generalized-nystrom-expected-error
- generalized-nystrom-tail
- generalized-nystrom-lower-bound
families:
- generalized-nystrom-methods
search_aliases:
- GN
- generalized Nystrom
- generalised Nystrom
- two-sided sketch approximation
---

Use two sketches to construct a low-rank approximation of a general matrix.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.generalizedNystrom name="Generalized Nyström approximation"
For a rectangular matrix $\mathbf A$ and two test matrices $\mathbf\Omega,\mathbf\Psi$, define

$$\widehat{\mathbf A}=\mathbf A\mathbf\Omega(\mathbf\Psi^{\mathsf{H}}\mathbf A\mathbf\Omega)^{\dagger}\mathbf\Psi^{\mathsf{H}}\mathbf A.$$

The two sketches capture column and row information. This is an oblique construction; it is generally different from orthogonally projecting onto the sampled range.
:::



## Mathematical guarantees

::: theorem result:generalized-nystrom-expected-error name="Expected Frobenius error"
Let $\mathbf A\in\mathbb R^{m\times n}$, with independent standard Gaussian test matrices $\mathbf\Omega\in\mathbb R^{n\times\ell}$ and $\mathbf\Psi\in\mathbb R^{m\times p}$. If $k+2\le\ell$ and $\ell+2\le p$, then

$$\mathbb E\|\mathbf A-\operatorname{GN}(\mathbf A,\mathbf\Omega,\mathbf\Psi)\|_{\mathrm F}^2\le\left(1+\frac{\ell}{p-\ell-1}\right)\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}^2.$$

The two factors measure the excess from the range sketch and the second sketch. Here $[\mathbf A]_k$ denotes a best rank-at-most-$k$ approximation.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
