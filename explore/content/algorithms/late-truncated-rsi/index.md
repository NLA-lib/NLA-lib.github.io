---
uid: 80eec251-c1bb-56de-a832-e85d41034ccc
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

{{ statement:late-truncated-rsi-c87bfc3a }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish. Statements about the untruncated projection are on the [randomized subspace iteration](/explore/algorithms/rsi/) page.

## Mathematical guarantees

These are upper bounds on the expected squared error for a real matrix $\mathbf{A}$ with $n$ columns, an $n\times\ell$ test matrix $\mathbf{X}$ with independent standard normal entries, and every number of power steps $p\ge0$. The truncated output satisfies each bound with the same right side as the untruncated projection.

{{ statement:nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-integral-frobnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-of-haslaw-gaussianmatrix }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
