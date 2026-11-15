---
kind: algorithm
id: nystrom
title: Nyström approximation
summary: Approximate a positive-semidefinite matrix using sampled or sketched columns.
status: outline
order: 14
theory:
- pseudoinverses
- random-matrices
- randomized-low-rank-theory
library_algorithm: nystrom
library_results: false
result_ids:
- nystrom-structural-bound
- nystrom-helps
- randomized-nystrom-expected-error
- randomized-nystrom-tail
- randomized-nystrom-lower-bound
- nystrom-two-eigenvalue-instance
---

Approximate a positive-semidefinite matrix using sampled or sketched columns.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.nystrom name="Nyström approximation"
For a Hermitian positive-semidefinite matrix $\mathbf A$ and test matrix $\mathbf\Omega$, form

$$\widehat{\mathbf A}=\mathbf A\mathbf\Omega(\mathbf\Omega^{\mathsf{H}}\mathbf A\mathbf\Omega)^{\dagger}\mathbf\Omega^{\mathsf{H}}\mathbf A.$$

The symbol $\dagger$ denotes the Moore–Penrose pseudoinverse, allowing a rank-deficient middle matrix. Sampling columns is a special choice of the test matrix.
:::



## Mathematical guarantees

::: theorem result:randomized-nystrom-expected-error name="Expected nuclear-norm error"
For real positive-semidefinite $\mathbf A$, standard Gaussian $\mathbf\Omega\in\mathbb R^{n\times\ell}$, and $k+2\le\ell$,

$$\mathbb E\|\mathbf A-\mathsf{nystrom}(\mathbf A,\mathbf\Omega)\|_*\le\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf A-[\mathbf A]_k\|_*.$$

The residual is positive semidefinite, so its nuclear norm is also its trace. The bound compares the expected residual trace with the optimal rank-$k$ tail.
:::

## Further results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
