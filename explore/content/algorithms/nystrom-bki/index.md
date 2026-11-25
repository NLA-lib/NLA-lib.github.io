---
uid: 208ba417-3ce5-525f-bf9f-c6f147101723
kind: algorithm
id: nystrom-bki
title: Nyström block Krylov iteration (NysBKI)
summary: Use a block Krylov test matrix in a Nyström approximation of a positive-semidefinite matrix.
status: outline
order: 16
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
library_algorithm: nystrom-bki
uses:
- nystrom
search_aliases:
- NysBKI
- block Krylov Nyström
library_results: false
result_ids:
- nysbki-gapless-error
- nysbki-gapped-error
- nystrom-bki-simulated-block
---

Use a block Krylov test matrix in a Nyström approximation of a positive-semidefinite matrix. This page concerns the untruncated approximation. Its rank-$r$ truncation is on the [late-truncated Nyström block Krylov iteration](/explore/algorithms/late-truncated-nystrom-bki/) page.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:nlalib-nystrombki-8647f4e3 }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $[\mathbf{A}]_r$ denotes the rank-$r$ truncated singular-value decomposition and $\|\cdot\|_*$ the nuclear norm. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both vanish.

## Components

{{ generated:components }}

## Mathematical guarantees

The two expectation bounds are upper bounds on the expected spectral error, not its square, for a real positive-semidefinite $\mathbf{A}$ of order $n$ and an $n\times\ell$ start block $\mathbf{X}$ with independent standard normal entries.

{{ statement:nysbki-gapped-error }}

{{ statement:nysbki-gapless-error }}

{{ statement:nystrom-bki-simulated-block }}

The same result groups contain a relative form of the gapless bound with a factor $(1+\varepsilon)^2$ and forms that give a sufficient depth; they are in the Library.

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
