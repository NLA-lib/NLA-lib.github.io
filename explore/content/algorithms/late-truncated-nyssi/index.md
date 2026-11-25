---
uid: 1d9144e5-9bd3-5d13-8cd3-752d49b044b0
kind: algorithm
id: late-truncated-nyssi
title: Late-truncated NysSI
summary: Complete Nyström subspace iteration, then truncate the output to the target rank.
status: outline
order: 17.5
families:
- subspace-iteration-methods
theory:
- matrix-polynomials
- random-matrices
- best-rank-approximation
search_aliases:
- truncated NysSI
- truncated Nyström subspace iteration
uses:
- nyssi
---

{{ statement:late-truncated-nystr-m-subspace-iteration-21bd0b0f }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $\|\cdot\|_*$ denotes the nuclear norm. Statements about the untruncated approximation are on the [Nyström subspace iteration](/explore/algorithms/nyssi/) page.

## Mathematical guarantees

The library states the truncated output in the nuclear norm, with a gap. These are upper bounds for a real positive-semidefinite $\mathbf{A}$ of order $n$, an $n\times\ell$ test matrix $\mathbf{X}$ with independent standard normal entries, and every number of power steps $p\ge0$.

{{ statement:matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix }}

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
