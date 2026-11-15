---
kind: algorithm
id: late-truncated-nystrom-bki
title: Late-truncated NysBKI
summary: Complete Nyström block Krylov iteration, then truncate the output to the target rank.
status: outline
order: 16.5
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- best-rank-approximation
search_aliases:
- truncated NysBKI
- truncated block Krylov Nyström
uses:
- nystrom-bki
---

::: definition name="Late-truncated Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf A$, first form $\mathbf B=\mathsf{nysbki}(\mathbf A,\mathbf\Omega,q)$. Return $[\mathbf B]_r$, a best rank-at-most-$r$ approximation to $\mathbf B$; here $[\cdot]_r$ denotes the rank-$r$ truncated singular-value decomposition.
:::

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $\|\cdot\|_*$ denotes the nuclear norm. Statements about the untruncated approximation are on the [Nyström block Krylov iteration](/explore/algorithms/nystrom-bki/) page.

## Mathematical guarantees

The library states the truncated output in the nuclear norm, with a gap. These are upper bounds for a real positive-semidefinite $\mathbf A$ of order $n$ and an $n\times\ell$ start block $\mathbf X$ with independent standard normal entries.

::: theorem decl:Matrix.PosSemidef.integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected nuclear-norm error with a gap" id=gapped-nuclear
Let $q\ge1$, let $r=h+1$ be the number of head eigenvalues, and let $t\ge r$ be a tail index with $t+2\le\ell$. With $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, and $\gamma=0$ when both vanish,

$$\mathbb E\|\mathbf A-[\mathsf{nysbki}(\mathbf A,\mathbf X,q)]_r\|_*\le\|\mathbf A-[\mathbf A]_r\|_*+4e^{-4\sqrt2\,(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_*.$$
:::

::: theorem decl:NLAlib.exists_forall_integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_of_singularGapRatio_pos_of_hasLaw_gaussianMatrix name="Sufficient depth with a gap" id=gapped-depth
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for $r=h+1\le t$ with $t+2\le\ell$, a positive gap $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, every $0<\varepsilon\le\varepsilon_0$, and every depth

$$q\ge\frac{C\log(n/\varepsilon)}{\sqrt{\gamma}},$$

the truncated output satisfies

$$\mathbb E\|\mathbf A-[\mathsf{nysbki}(\mathbf A,\mathbf X,q)]_r\|_*\le(1+\varepsilon)\,\|\mathbf A-[\mathbf A]_r\|_*.$$

The statement asserts the existence of the constants.
:::

## Scope

The library has no gapless statement and no spectral-norm statement for this truncated output.

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
