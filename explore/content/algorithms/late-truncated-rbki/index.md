---
kind: algorithm
id: late-truncated-rbki
title: Late-truncated RBKI
summary: Complete randomized block Krylov iteration, then truncate the output to the target rank.
status: outline
order: 12.5
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
search_aliases:
- truncated RBKI
- truncated block Krylov iteration
- rank-r block Krylov approximation
result_ids:
- rbki-single-vector-gapless-error
- rbki-any-block-gapless-error
uses:
- rbki
---

::: definition name="Late-truncated RBKI"
First form the block Krylov approximation $\mathbf B=\mathsf{rbki}(\mathbf A,\mathbf\Omega,q)$. Return $[\mathbf B]_r$, a best rank-at-most-$r$ approximation to $\mathbf B$; here $[\cdot]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a start block of $\ell$ columns the rank of $\mathbf B$ is at most $q\ell$; the truncated output has rank at most $r$.
:::

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish. Statements about the untruncated projection are on the [randomized block Krylov iteration](/explore/algorithms/rbki/) page.

## Mathematical guarantees

These are upper bounds for a real matrix $\mathbf A$ with $n$ columns and a start block with independent standard normal entries. Where the library also states a bound for the untruncated projection, the truncated output satisfies it with the same right side.

### Blocks wider than the target rank

Here $\mathbf X$ is $n\times\ell$ with $t+2\le\ell$ or $r+2\le\ell$, and the bounds are in expectation.

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected spectral error with a gap" id=gapped-spectral
Let $q\ge1$, let $r=h+1$ be the number of head singular values, and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_2^2\le\sigma_r^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Under the same hypotheses ($q\ge1$, $r=h+1\le t$, $t+2\le\ell$),

$$\mathbb E\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_{\mathrm F}^2\le\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2.$$
:::

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap" id=gapless
Let $q\ge1$, let $r$ be the target rank with $r+2\le\ell$, and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_2^2\le(1+\varepsilon)^2\sigma_r^2+4e^{-8(q-1)\sqrt{\varepsilon/(2+\varepsilon)}}\,\frac{r}{\ell-r-1}\,\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2.$$

No gap between singular values is assumed.
:::

::: theorem decl:NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rbki_sq_le_of_hasLaw_gaussianMatrix name="Sufficient depth without a gap" id=gapless-depth
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for every real matrix $\mathbf A$ with $n$ columns, every target rank $r$ with $r+2\le\ell$, every $0<\varepsilon\le\varepsilon_0$, and every depth

$$q\ge\frac{C\log(n/\varepsilon)}{\sqrt{\varepsilon}},$$

the truncated output satisfies

$$\mathbb E\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_2^2\le(1+\varepsilon)\,\sigma_r^2.$$

The statement asserts the existence of the constants. With a positive gap $\gamma$, the same result group as the gapped bounds contains the corresponding forms with $q\ge C\log(n/\varepsilon)/\sqrt{\gamma}$, in the spectral and Frobenius norms; they are in the Library.
:::

### Block sizes below the target rank

These are tail bounds for narrow start blocks, down to a single start vector. They assume a relative gap $\Delta$ among the leading singular values and a depth at least the number of those singular values.

::: theorem decl:NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianVector name="Single start vector with a gap" id=single-vector-gapped
Let $\mathbf x\in\mathbb R^n$ have independent standard normal entries. Fix a head of $r=h+1$ singular values, a tail index $t\ge r$, a depth $q\ge t$, and $\delta>0$. Suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<t$, and let $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$. Then

$$\mathbb P\Bigl[\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf x,q)]_r\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The start block is the single column $\mathbf x$. No positivity of $\sigma_{t-1}$ is assumed.
:::

::: theorem result:rbki-single-vector-gapless-error name="Single start vector, relative form" id=single-vector-gapless
Let $\mathbf x\in\mathbb R^n$ have independent standard normal entries. Fix a target rank $r$, a depth $q\ge r$, $\delta>0$, and $\varepsilon>0$. Suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<r$. Then

$$\mathbb P\Bigl[\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf x,q)]_r\|_2^2>(1+\varepsilon)^2\sigma_r^2+32\,e^{-8(q-r)\sqrt{\varepsilon/(2+\varepsilon)}}\,\Delta^{-2(r-1)}\,\frac{r^3}{\delta^3}\,\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2\Bigr]\le\delta.$$

No gap between $\sigma_{r-1}$ and $\sigma_r$ is assumed. The gap $\Delta$ among the first $r$ singular values is still required.
:::

::: theorem decl:NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianMatrix name="Any block size with a gap" id=any-block-gapped
Let $\mathbf X$ be an $n\times\ell$ matrix with independent standard normal entries, $\ell\ge1$. With $r=h+1\le t\le q$, $\delta>0$, $\Delta>0$ satisfying $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<t$, and $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$,

$$\mathbb P\Bigl[\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The right-hand side does not depend on $\ell$. The truncated error is not monotone in the start block, so this is not obtained by comparing the outputs of two blocks.
:::

::: theorem result:rbki-any-block-gapless-error name="Any block size, relative form" id=any-block-gapless
Let $\mathbf X$ be an $n\times\ell$ matrix with independent standard normal entries, $\ell\ge1$. Fix a target rank $r$, a depth $q\ge r$, $\delta>0$, and $\varepsilon>0$, and suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<r$. Then

$$\mathbb P\Bigl[\|\mathbf A-[\mathsf{rbki}(\mathbf A,\mathbf X,q)]_r\|_2^2>(1+\varepsilon)^2\sigma_r^2+32\,e^{-8(q-r)\sqrt{\varepsilon/(2+\varepsilon)}}\,\Delta^{-2(r-1)}\,\frac{r^3}{\delta^3}\,\|\mathbf A-[\mathbf A]_r\|_{\mathrm F}^2\Bigr]\le\delta.$$

The bound does not depend on $\ell$. For $r+2\le\ell$ the expectation bound above needs no gap $\Delta$.
:::

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
