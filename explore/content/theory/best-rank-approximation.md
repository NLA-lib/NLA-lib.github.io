---
kind: theory
id: best-rank-approximation
title: Best-rank approximation and truncation
summary: Truncated SVD, Eckart–Young optimality, and error bounds for projection and truncation.
status: outline
parents:
- matrix-analysis
prerequisites:
- singular-values
- subspaces
module_prefixes:
- NLAlib.Matrix.Spectral.BestRankApprox
- NLAlib.Matrix.Spectral.ProjectedLowRank
- NLAlib.Matrix.Perturbation.BestRankApprox
result_ids:
- eckart-young-frobenius
---

This topic contains reusable approximation theory. The choices of when to truncate a sketch or an approximation belong to the individual RSVD method pages.

::: definition decl:NLAlib.truncatedSVD name="Truncated SVD"
Write $[\mathbf A]_k$ for the matrix obtained by retaining the $k$ largest singular values and their singular vectors. It has rank at most $k$. Ties can make the best approximation nonunique; the library fixes a choice.
:::

## Background

{{ generated:prerequisites }}

## Mathematical guarantees

::: theorem result:eckart-young-frobenius name="Eckart–Young optimality"
If $\operatorname{rank}(\mathbf B)\le k$, then

$$\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}\le\|\mathbf A-\mathbf B\|_{\mathrm F}.$$

This reusable comparison separates the mathematical optimum from the error of a particular randomized or iterative algorithm.
:::

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
