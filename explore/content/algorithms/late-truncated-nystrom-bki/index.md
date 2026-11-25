---
uid: 78c91b06-806e-51b7-8dfe-64e542775bdb
kind: algorithm
id: late-truncated-nystrom-bki
title: Late-truncated NysBKI
summary: Complete Nyström block Krylov iteration, then truncate the output to the target rank.
status: outline
order: 16.5
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- best-rank-approximation
search_aliases:
- truncated NysBKI
- truncated block Krylov Nyström
uses:
- nystrom-bki
---

{{ statement:late-truncated-nystr-m-block-krylov-iteration-9762adf8 }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$; for a positive-semidefinite matrix they are its eigenvalues. $\|\cdot\|_*$ denotes the nuclear norm. Statements about the untruncated approximation are on the [Nyström block Krylov iteration](/explore/algorithms/nystrom-bki/) page.

## Mathematical guarantees

The library states the truncated output in the nuclear norm, with a gap. These are upper bounds for a real positive-semidefinite $\mathbf{A}$ of order $n$ and an $n\times\ell$ start block $\mathbf{X}$ with independent standard normal entries.

{{ statement:matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix }}

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
