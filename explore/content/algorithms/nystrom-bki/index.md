---
kind: algorithm
id: nystrom-bki
title: Nyström block Krylov iteration
summary: Use a block Krylov test matrix in a Nyström approximation of a positive-semidefinite matrix.
status: outline
order: 16
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
library_algorithm: nystrom-bki
uses:
- nystrom
search_aliases:
- NysBKI
- block Krylov Nyström
library_results: false
result_ids:
- nysbki-gapless-error
- nysbki-gapped-error
- nystrom-bki-simulated-block
---

Use a block Krylov test matrix in a Nyström approximation of a positive-semidefinite matrix. This page concerns the untruncated approximation. Its rank-$r$ truncation is on the [late-truncated Nyström block Krylov iteration](/explore/algorithms/late-truncated-nystrom-bki/) page.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.nystromBKI name="Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf A$, a start block $\mathbf\Omega$ with $\ell$ columns, and $q$ blocks, build the test matrix $[\mathbf\Omega,\mathbf A\mathbf\Omega,\ldots,\mathbf A^{q-1}\mathbf\Omega]$ and apply the Nyström construction to it:

$$\mathsf{nysbki}(\mathbf A,\mathbf\Omega,q)=\mathsf{nystrom}\bigl(\mathbf A,[\mathbf\Omega,\mathbf A\mathbf\Omega,\ldots,\mathbf A^{q-1}\mathbf\Omega]\bigr).$$

The powers are retained together rather than keeping only the last one.
:::

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $[\mathbf A]_r$ denotes the rank-$r$ truncated singular-value decomposition and $\|\cdot\|_*$ the nuclear norm. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

The two expectation bounds are upper bounds on the expected spectral error, not its square, for a real positive-semidefinite $\mathbf A$ of order $n$ and an $n\times\ell$ start block $\mathbf X$ with independent standard normal entries.

::: theorem result:nysbki-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $q\ge1$, let $r=h+1$ be the number of head eigenvalues, and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf A-\mathsf{nysbki}(\mathbf A,\mathbf X,q)\|_2\le\sigma_r+4e^{-4\sqrt2\,(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_*,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::

::: theorem result:nysbki-gapless-error name="Expected spectral error without a gap" id=gapless
Let $q\ge2$ and let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf A-\mathsf{nysbki}(\mathbf A,\mathbf X,q)\|_2\le\sigma_r\exp\!\biggl(\frac{\log^2(4\rho)}{16(q-1)^2}\biggr),\qquad\rho=1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf A^{1/2}-[\mathbf A^{1/2}]_r\|_{\mathrm F}^2}{\sigma_r(\mathbf A^{1/2})^2}.$$

The library also proves $\rho=1+\dfrac{r}{\ell-r-1}\,\dfrac{\|\mathbf A-[\mathbf A]_r\|_*}{\sigma_r}$. No gap between eigenvalues is assumed.
:::

::: theorem result:nystrom-bki-simulated-block name="The simulated block" id=simulated-block
Let $\mathbf A$ be a real or complex Hermitian positive-semidefinite matrix and $\mathbf\Omega$ a start block. For all integers $s,q\ge0$,

$$\mathsf{nysbki}\bigl(\mathbf A,\ [\mathbf\Omega,\mathbf A\mathbf\Omega,\ldots,\mathbf A^{s}\mathbf\Omega],\ q+1\bigr)=\mathsf{nysbki}(\mathbf A,\mathbf\Omega,\ s+q+1).$$

Running $s+q+1$ blocks from $\mathbf\Omega$ gives the same approximation as running $q+1$ blocks from the wider block formed by the first $s+1$ Krylov blocks of $\mathbf\Omega$. Positive semidefiniteness is a hypothesis of the statement.
:::

The same result groups contain a relative form of the gapless bound with a factor $(1+\varepsilon)^2$ and forms that give a sufficient depth; they are in the Library.

## Further results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
