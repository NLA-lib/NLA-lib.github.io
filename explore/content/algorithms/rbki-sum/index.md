---
uid: 288eeff9-85fd-43d3-96cb-76142dcf479d
kind: algorithm
id: rbki-sum
title: Two-space block Krylov (BCW)
summary: Combine a narrow, deep Krylov sketch with a wide, shallow sketch for cube-root accuracy dependence.
status: ready
order: 12.75
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
library_algorithm: rbki-sum
library_results: false
result_ids:
- rbki-sum-frobenius-error
- rbki-sum-schatten-error
- rbki-sum-schatten-tail
- rbki-sum-schatten-large-p-error
- rbki-sum-schatten-large-p-tail
uses:
- rbki
search_aliases:
- BCW
- BKW
- Bakshi Clarkson Woodruff
- two-space block Krylov
- two-block Krylov
- rbkiSum
- cube-root low-rank approximation
---

Two-space block Krylov combines a narrow, deep Krylov sketch with a wider, shallower one. Its relative-error bounds have cube-root dependence on the accuracy parameter. BCW refers to Bakshi, Clarkson and Woodruff, whose [low-rank approximation method](/explore/references/#reference-BakshiClarksonWoodruff2022) motivates this construction.

The library analyzes a variant that projects onto the **sum of the two spaces**, represented by `NLAlib.rbkiSum`. The paper selects one of two runs using estimated singular values. The guarantees below concern the combined-space output.

## Definition and outputs

{{ statement:bcw-definition }}

The untruncated projection can have rank larger than the target $k$. The Frobenius and large-$p$ bounds below concern its rank-$k$ truncation; the small-$p$ bound uses the two-sided output defined above. Each has rank at most $k$.

## Gaussian starts

Let $\mathbf{A}$ be a real $m\times n$ matrix. Each start block $\mathbf{X}_i$ has independent standard normal entries; the two blocks need not be independent of one another. Write $\operatorname{OPT}_p=\|\mathbf{A}-[\mathbf{A}]_k\|_{S_p}$, with $\operatorname{OPT}_2$ the optimal Frobenius error. All explicit relative-error statements below assume $k\ge1$ and $0<\varepsilon\le1$.

## Frobenius and small Schatten exponents

{{ statement:bcw-frobenius-error }}

Choosing the smallest admissible $j$ and depths, the two runs require $O(k\varepsilon^{-1/3}\log(k/\varepsilon))$ products with $\mathbf{A}$ or $\mathbf{A}^{\mathsf{H}}$; forming the small final truncation is a separate computation. The bound has no spectral-gap assumption.

{{ statement:bcw-small-p-error }}

## Dimension-free large Schatten exponents

These bounds hold for every finite $p\ge2$. No matrix dimension occurs in the block-size or depth thresholds. Define $r=\lceil(p-2)/4\rceil$.

{{ statement:bcw-large-p-error }}

{{ statement:bcw-large-p-tail }}

{{ statement:bcw-asymptotic-depths }}

These guarantees bound the $p$-th power of the error. Their norm factor is $(1+\varepsilon)^{1/p}$. Setting $\varepsilon=p\eta$ gives a norm factor at most $e^\eta$ for $0<\eta\le1/p$; the depths retain the additive $p$ term from the filter degree.

The Library also contains a different large-$p$ tail bound for the norm threshold $(1+\varepsilon)\operatorname{OPT}_p$, with a matrix dimension inside its logarithms. It is included under Further results with its own hypotheses.

## Further results

{{ generated:results }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
