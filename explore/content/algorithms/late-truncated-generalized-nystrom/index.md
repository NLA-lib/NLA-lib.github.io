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
First form the generalized Nyström approximation $\mathbf B=\operatorname{GN}(\mathbf A,\mathbf\Omega,\mathbf\Psi)$. Return $\widehat{\mathbf A}=[\mathbf B]_k$, a best rank-at-most-$k$ approximation to the completed matrix. This truncation selects a subspace from the output rather than from the original range sketch.
:::

## Mathematical guarantees

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_generalizedNystrom_sq_le_one_add_of_hasLaw_gaussianMatrix name="Relative error with linear sample dependence"
For a real input $\mathbf A$, independent standard Gaussian sketches of widths $\ell,p$, and $0<\varepsilon\le1$, suppose

$$\ell\ge\frac{3500004k}{\varepsilon},\qquad p\ge4\ell.$$

Then

$$\mathbb E\|\mathbf A-[\operatorname{GN}(\mathbf A,\mathbf\Omega,\mathbf\Psi)]_k\|_{\mathrm F}^2\le(1+\varepsilon)\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}^2.$$

Both sketch widths can be chosen of order $k/\varepsilon$. The explicit sufficient constant above is large. The additional result below gives another proven regime with a smaller first-sketch constant and a larger second-sketch requirement.
:::

## Further results

{{ generated:results }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
