---
kind: algorithm
id: late-truncated-generalized-nystrom
title: Late-truncated generalized Nyström (TGN)
summary: Complete generalized Nyström, then truncate the output to the target rank.
status: outline
families:
- generalized-nystrom-methods
theory:
- pseudoinverses
- random-matrices
- best-rank-approximation
- sketching-theory
- randomized-low-rank-theory
search_aliases:
- TGN
- truncated GN
- late truncated GN
- truncated generalized Nystrom
result_ids:
- tgn-expected-error
- truncated-gn-lower-bound
uses:
- generalized-nystrom
---

::: definition name="Late-truncated GN"
First form the generalized Nyström approximation $\mathbf B=\mathsf{gn}(\mathbf A,\mathbf\Omega,\mathbf\Psi)$. Return $\widehat{\mathbf A}=[\mathbf B]_k$, a best rank-at-most-$k$ approximation to the completed matrix. This truncation selects a subspace from the output rather than from the original range sketch.
:::

## Mathematical guarantees

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_generalizedNystrom_sq_le_one_add_of_hasLaw_gaussianMatrix_of_truncatedGeneralizedNystromRangeDim_le name="Expected relative error" id=expected-error
For a real input $\mathbf A$, independent standard Gaussian sketches of widths $\ell,p$, and $0<\varepsilon\le1$, suppose

$$\ell\ge\frac{200k}{\varepsilon},\qquad p\ge14\ell.$$

Then

$$\mathbb E\|\mathbf A-[\mathsf{gn}(\mathbf A,\mathbf\Omega,\mathbf\Psi)]_k\|_{\mathrm F}^2\le(1+\varepsilon)\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}^2.$$

Both sketch widths can be chosen of order $k/\varepsilon$. This is a sufficient upper bound on the expected squared approximation error, valid for every real input matrix. The source also retains alternative bounds with different sufficient sketch sizes.
:::

::: theorem result:truncated-gn-lower-bound name="An unavoidable error on hard inputs" id=lower-bound
Let $\mathbf A_a=\operatorname{diag}(a\mathbf I_k,\mathbf I_{n-k})$, and use independent standard Gaussian sketches with $k+2\le\ell<n$ and $p\ge\ell+2$. For every $\eta>0$, all sufficiently large $a$ satisfy

$$\mathbb E\|\mathbf A_a-[\mathsf{gn}(\mathbf A_a,\mathbf\Omega,\mathbf\Psi)]_k\|_{\mathrm F}^2\ge(n-k)+\frac{k(n-\ell)}{p-\ell-1}-\eta.$$

The optimal rank-$k$ squared Frobenius error is $n-k$ when $a\ge1$. The extra term shows noise that late truncation can retain even when the leading singular values become arbitrarily large. This is a lower bound for a particular family of inputs, rather than an upper guarantee for every input.
:::

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
