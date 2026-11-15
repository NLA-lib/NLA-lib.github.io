---
kind: algorithm
id: rsi
title: Randomized subspace iteration (RSI)
summary: Apply power iterations to the sketch, then project the matrix onto its range.
status: outline
order: 11
families:
- subspace-iteration-methods
theory:
- matrix-polynomials
- random-matrices
- randomized-low-rank-theory
library_algorithm: rsi
uses:
- randomized-svd
search_aliases:
- RSI
- power iteration range finder
- randomized power iteration
library_results: false
result_ids:
- rsi-gapped-error
- rsi-gapless-error
---

Apply power iterations to the sketch, then project the matrix onto its range. This page concerns the untruncated projection. Its rank-$r$ truncation is a different output with its own statements, on the [late-truncated RSI](/explore/algorithms/late-truncated-rsi/) page.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Randomized subspace iteration"
Choose a test matrix $\mathbf\Omega$ with $\ell$ columns and a nonnegative power count $p$. Form

$$\mathbf Y=\mathbf A(\mathbf A^{\mathsf{H}}\mathbf A)^p\mathbf\Omega,\qquad\mathsf{rsi}(\mathbf A,\mathbf\Omega,p)=\mathbf P_{\mathbf Y}\mathbf A=\mathsf{rsvd}\bigl(\mathbf A,(\mathbf A^{\mathsf{H}}\mathbf A)^p\mathbf\Omega\bigr).$$

Here $\mathbf P_{\mathbf Y}$ is the orthogonal projector onto the sampled range. With $p=0$ this is the ordinary range-finder approximation. Only the last power is kept; block Krylov iteration keeps all of them. Intermediate orthogonalization controls the numerical loss of directions and belongs to an implementation. For Hermitian positive-semidefinite matrices, the range also approximates a dominant invariant subspace.
:::

The library states its results for the range finder applied to the powered test matrix; $\mathsf{rsi}$ is this page's name for that matrix. Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$, and $[\mathbf A]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

These are upper bounds on the expected squared error for a real matrix $\mathbf A$ with $n$ columns, an $n\times\ell$ test matrix $\mathbf X$ with independent standard normal entries, and every number of power steps $p\ge0$.

::: theorem result:rsi-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head singular values and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf A-\mathsf{rsi}(\mathbf A,\mathbf X,p)\|_2^2\le\sigma_r^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$

No positivity of the gap is assumed. At $p=0$ this is the range-finder bound at rank $t$ with $\sigma_t$ replaced by the larger $\sigma_r$.
:::

::: theorem decl:NLAlib.integral_frobNorm_sub_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Under the same hypotheses ($r=h+1\le t$, $t+2\le\ell$),

$$\mathbb E\|\mathbf A-\mathsf{rsi}(\mathbf A,\mathbf X,p)\|_{\mathrm F}^2\le\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2.$$
:::

::: theorem result:rsi-gapless-error name="Expected spectral error without a gap" id=gapless
Let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf A-\mathsf{rsi}(\mathbf A,\mathbf X,p)\|_2^2\le\sigma_r^2\Bigl(1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2}{\sigma_r^2}\Bigr)^{1/(2p+1)}.$$

No gap between singular values is assumed. At $p=0$ the right side is the range-finder bound.
:::

::: theorem decl:NLAlib.integral_specNorm_sub_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap, relative form" id=gapless-relative
Let $r$ be a target rank with $r+2\le\ell$ and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf A-\mathsf{rsi}(\mathbf A,\mathbf X,p)\|_2^2\le(1+\varepsilon)^2\sigma_r^2+e^{-8p\varepsilon/(2+\varepsilon)}\,\frac{r}{\ell-r-1}\,\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2.$$

No gap is assumed and $\sigma_r>0$ is not required. This bound and the preceding one are alternative regimes for the same error.
:::

The same result groups contain a form in every unitarily invariant norm for the Gram residual and forms that give a sufficient number of power steps for a relative accuracy $\varepsilon$; they are in the Library. The gapped bounds are proved through the [filtered range finder](/explore/algorithms/filtered-randomized-svd/) with the monomial filter $\lambda^p$.

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
