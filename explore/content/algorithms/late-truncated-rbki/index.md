---
uid: 5c9cf030-bc6c-595a-ba8b-faf1fb88d09b
kind: algorithm
id: late-truncated-rbki
title: Late-truncated RBKI
summary: Complete randomized block Krylov iteration, then truncate the output to the target rank.
status: outline
order: 12.5
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
search_aliases:
- truncated RBKI
- truncated block Krylov iteration
- rank-r block Krylov approximation
result_ids:
- rbki-single-vector-gapless-error
- rbki-any-block-gapless-error
uses:
- rbki
---

{{ statement:late-truncated-rbki-100d7ac0 }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$. For a head index $h$ and a tail index $t$, the relative gap is $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, with $\gamma=0$ when both singular values vanish. Statements about the untruncated projection are on the [randomized block Krylov iteration](/explore/algorithms/rbki/) page.

## Mathematical guarantees

These are upper bounds for a real matrix $\mathbf{A}$ with $n$ columns and a start block with independent standard normal entries. Where the library also states a bound for the untruncated projection, the truncated output satisfies it with the same right side.

### Blocks wider than the target rank

Here $\mathbf{X}$ is $n\times\ell$ with $t+2\le\ell$ or $r+2\le\ell$, and the bounds are in expectation.

{{ statement:nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-integral-frobnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix }}

{{ statement:nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rbki-sq-le-of-haslaw-gaussianmatrix }}

### Block sizes below the target rank

These are tail bounds for narrow start blocks, down to a single start vector. They assume a relative gap $\Delta$ among the leading singular values and a depth at least the number of those singular values.

{{ statement:nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianvector }}

{{ statement:rbki-single-vector-gapless-error }}

{{ statement:nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianmatrix }}

{{ statement:rbki-any-block-gapless-error }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
