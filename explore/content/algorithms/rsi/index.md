---
uid: 548bc2ae-2bb8-53e8-a891-e1a81aa3c73f
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

{{ statement:randomized-subspace-iteration-90f9c5f5 }}

The library states its results for the range finder applied to the powered test matrix; $\mathsf{rsi}$ is this page's name for that matrix. Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$, and $[\mathbf{A}]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

These are upper bounds on the expected squared error for a real matrix $\mathbf{A}$ with $n$ columns, an $n\times\ell$ test matrix $\mathbf{X}$ with independent standard normal entries, and every number of power steps $p\ge0$.

{{ statement:rsi-gapped-error }}

{{ statement:nlalib-integral-frobnorm-sub-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:rsi-gapless-error }}

{{ statement:nlalib-integral-specnorm-sub-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix }}

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
