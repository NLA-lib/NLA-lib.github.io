---
kind: algorithm
id: early-truncated-generalized-nystrom
title: Early-truncated generalized Nyström (ETGN)
summary: Truncate the range sketch before completing the two-sided approximation.
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
- ETGN
- early truncated GN
- early truncated generalized Nystrom
result_ids:
- etgn
---

::: definition decl:NLAlib.earlyTruncatedGeneralizedNystrom name="Early-truncated GN"
Form $\mathbf Y_k=[\mathbf A\mathbf\Omega]_k$, then return

$$\widehat{\mathbf A}=\mathbf Y_k(\mathbf\Psi^{\mathsf H}\mathbf Y_k)^{\dagger}\mathbf\Psi^{\mathsf H}\mathbf A.$$

The rank-$k$ subspace is selected from the range sketch before the second sketch completes the approximation. The output has rank at most $k$; the library fixes a choice when singular values are tied.
:::

## Mathematical guarantees

::: theorem result:etgn name="Gaussian relative-error guarantee"
For a real input $\mathbf A$, independent standard Gaussian sketches of widths $\ell,p$, and $0<\varepsilon\le1$, suppose

$$\ell\ge\frac{1600k}{\varepsilon^2},\qquad p\ge k+1+\frac{(2+\varepsilon)k}{\varepsilon}.$$

Then the mathematical early-truncated output satisfies

$$\mathbb E\|\mathbf A-\widehat{\mathbf A}\|_{\mathrm F}^2\le(1+\varepsilon)\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}^2.$$

Thus the expected squared error is within a factor $1+\varepsilon$ of the optimal rank-$k$ squared Frobenius error. The two sketch sizes have different accuracy dependence.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
