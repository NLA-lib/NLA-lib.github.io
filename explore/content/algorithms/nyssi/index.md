---
uid: fbc8acf9-c22f-58cd-85bf-aa71cdc6cfb7
kind: algorithm
id: nyssi
title: Nyström subspace iteration (NysSI)
summary: Use a powered test matrix in a Nyström approximation of a positive-semidefinite matrix.
status: outline
order: 17
families:
- subspace-iteration-methods
theory:
- matrix-polynomials
- random-matrices
library_algorithm: nyssi
uses:
- nystrom
search_aliases:
- NysSI
- Nyström power iteration
library_results: false
result_ids:
- nyssi-gapped-error
- nyssi-gapless-error
---

Use a powered test matrix in a Nyström approximation of a positive-semidefinite matrix. This page concerns the untruncated approximation. Its rank-$r$ truncation is on the [late-truncated Nyström subspace iteration](/explore/algorithms/late-truncated-nyssi/) page.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:nystr-m-subspace-iteration-a2eae5c1 }}

The library states its results for the Nyström approximation with the powered test matrix; $\mathsf{nyssi}$ is this page's name for that matrix. Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $[\mathbf{A}]_r$ denotes the rank-$r$ truncated singular-value decomposition and $\|\cdot\|_*$ the nuclear norm. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

These are upper bounds on the expected spectral error, not its square, for a real positive-semidefinite $\mathbf{A}$ of order $n$, an $n\times\ell$ test matrix $\mathbf{X}$ with independent standard normal entries, and every number of power steps $p\ge0$.

{{ statement:nyssi-gapped-error }}

{{ statement:nyssi-gapless-error }}

The same result groups contain a relative form of the gapless bound with a factor $(1+\varepsilon)^2$ and forms that give a sufficient number of power steps; they are in the Library.

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
