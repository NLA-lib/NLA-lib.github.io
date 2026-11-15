---
kind: algorithm
id: nyssi
title: Nyström subspace iteration (NysSI)
summary: Use a powered test matrix in a Nyström approximation of a positive-semidefinite matrix.
status: outline
order: 17
families:
- subspace-iteration-methods
theory:
- matrix-polynomials
- random-matrices
library_algorithm: nyssi
uses:
- nystrom
search_aliases:
- NysSI
- Nyström power iteration
library_results: false
result_ids:
- nyssi-gapped-error
- nyssi-gapless-error
---

Use a powered test matrix in a Nyström approximation of a positive-semidefinite matrix. This page concerns the untruncated approximation. Its rank-$r$ truncation is on the [late-truncated Nyström subspace iteration](/explore/algorithms/late-truncated-nyssi/) page.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Nyström subspace iteration"
For Hermitian positive-semidefinite $\mathbf A$, replace the test matrix in the Nyström approximation by $\mathbf A^p\mathbf\Omega$, with $p\ge0$:

$$\mathsf{nyssi}(\mathbf A,\mathbf\Omega,p)=\mathsf{nystrom}(\mathbf A,\mathbf A^p\mathbf\Omega).$$

The powers emphasize dominant spectral directions. Only the last power is kept; the block Krylov variant keeps all of them. The choice of stable intermediate bases belongs to a concrete implementation.
:::

The library states its results for the Nyström approximation with the powered test matrix; $\mathsf{nyssi}$ is this page's name for that matrix. Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $[\mathbf A]_r$ denotes the rank-$r$ truncated singular-value decomposition and $\|\cdot\|_*$ the nuclear norm. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

These are upper bounds on the expected spectral error, not its square, for a real positive-semidefinite $\mathbf A$ of order $n$, an $n\times\ell$ test matrix $\mathbf X$ with independent standard normal entries, and every number of power steps $p\ge0$.

::: theorem result:nyssi-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head eigenvalues and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf A-\mathsf{nyssi}(\mathbf A,\mathbf X,p)\|_2\le\sigma_r+e^{-4p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_*,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::

::: theorem result:nyssi-gapless-error name="Expected spectral error without a gap" id=gapless
Let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf A-\mathsf{nyssi}(\mathbf A,\mathbf X,p)\|_2\le\sigma_r\,\rho^{1/(2p+1)},\qquad\rho=1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf A^{1/2}-[\mathbf A^{1/2}]_r\|_{\mathrm F}^2}{\sigma_r(\mathbf A^{1/2})^2}.$$

The library also proves $\rho=1+\dfrac{r}{\ell-r-1}\,\dfrac{\|\mathbf A-[\mathbf A]_r\|_*}{\sigma_r}$. No gap between eigenvalues is assumed.
:::

The same result groups contain a relative form of the gapless bound with a factor $(1+\varepsilon)^2$ and forms that give a sufficient number of power steps; they are in the Library.

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
