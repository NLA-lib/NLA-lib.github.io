---
kind: algorithm
id: late-truncated-rsi
title: Late-truncated RSI
summary: Complete randomized subspace iteration, then truncate the output to the target rank.
status: outline
order: 11.5
families:
- subspace-iteration-methods
theory:
- matrix-polynomials
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
search_aliases:
- truncated RSI
- truncated subspace iteration
- rank-r subspace iteration approximation
uses:
- rsi
---

::: definition name="Late-truncated RSI"
First form the subspace-iteration approximation $\mathbf B=\mathsf{rsi}(\mathbf A,\mathbf\Omega,p)=\mathsf{rsvd}\bigl(\mathbf A,(\mathbf A^{\mathsf{H}}\mathbf A)^p\mathbf\Omega\bigr)$. Return $[\mathbf B]_r$, a best rank-at-most-$r$ approximation to $\mathbf B$; here $[\cdot]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a test matrix of $\ell$ columns the rank of $\mathbf B$ is at most $\ell$; the truncated output has rank at most $r$.
:::

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish. Statements about the untruncated projection are on the [randomized subspace iteration](/explore/algorithms/rsi/) page.

## Mathematical guarantees

These are upper bounds on the expected squared error for a real matrix $\mathbf A$ with $n$ columns, an $n\times\ell$ test matrix $\mathbf X$ with independent standard normal entries, and every number of power steps $p\ge0$. The truncated output satisfies each bound with the same right side as the untruncated projection.

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head singular values and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf A-[\mathsf{rsi}(\mathbf A,\mathbf X,p)]_r\|_2^2\le\sigma_r^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Under the same hypotheses ($r=h+1\le t$, $t+2\le\ell$),

$$\mathbb E\|\mathbf A-[\mathsf{rsi}(\mathbf A,\mathbf X,p)]_r\|_{\mathrm F}^2\le\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2.$$
:::

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap" id=gapless
Let $r$ be the target rank with $r+2\le\ell$ and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf A-[\mathsf{rsi}(\mathbf A,\mathbf X,p)]_r\|_2^2\le(1+\varepsilon)^2\sigma_r^2+e^{-8p\varepsilon/(2+\varepsilon)}\,\frac{r}{\ell-r-1}\,\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2.$$

No gap between singular values is assumed.
:::

::: theorem decl:NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_of_hasLaw_gaussianMatrix name="Sufficient number of power steps without a gap" id=gapless-steps
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for every real matrix $\mathbf A$ with $n$ columns, every target rank $r$ with $r+2\le\ell$, every $0<\varepsilon\le\varepsilon_0$, and every number of power steps

$$p\ge\frac{C\log(n/\varepsilon)}{\varepsilon},$$

the truncated output satisfies

$$\mathbb E\|\mathbf A-[\mathsf{rsi}(\mathbf A,\mathbf X,p)]_r\|_2^2\le(1+\varepsilon)\,\sigma_r^2.$$

The statement asserts the existence of the constants. With a positive gap $\gamma$, the same result group as the gapped bounds contains the corresponding forms with $p\ge C\log(n/\varepsilon)/\gamma$, in the spectral and Frobenius norms; they are in the Library.
:::

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
