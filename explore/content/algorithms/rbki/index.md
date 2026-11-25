---
uid: e23fd3b4-c660-5a30-87c5-0d2d00a7e80e
kind: algorithm
id: rbki
title: Randomized block Krylov iteration (RBKI)
summary: Project the matrix onto a block Krylov space generated from its sketch.
status: outline
order: 12
families:
- block-krylov-methods
theory:
- krylov-spaces
- random-matrices
- randomized-low-rank-theory
- complexity-lower-bounds
library_algorithm: rbki
uses:
- golub-kahan
search_aliases:
- RBKI
- block Krylov iteration
library_results: false
result_ids:
- rbki-gapped-error
- rbki-gapless-error
- rbki-simulated-block
- rbki-block-monotonicity
- rbki-single-vector-structural-error
- rbki-single-vector-gapped-error
- rbki-any-block-gapped-error
- rbki-multiplicity-lower-bound
---

Project the matrix onto a block Krylov space generated from its sketch. This page concerns the untruncated projection. Its rank-$r$ truncation is a different output with its own statements, on the [late-truncated RBKI](/explore/algorithms/late-truncated-rbki/) page.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:nlalib-rbki-ce25720b }}

Singular values are indexed from zero, $\sigma_0\ge\sigma_1\ge\cdots$, so the best rank-$r$ spectral error is $\sigma_r$, and $[\mathbf{A}]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a head index $h$ and a tail index $t$, the relative gap is

$$\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t},$$

with $\gamma=0$ when both singular values vanish.

## Components

The definition is a projection and prescribes no computation. The Golub–Kahan process computes factors whose product, in exact arithmetic, equals $\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)$; that identity is stated on the process page and the scope of its program on the implementation page.

{{ generated:components }}

## Mathematical guarantees

These are upper bounds on the expected squared error for a real matrix $\mathbf{A}$ with $n$ columns and an $n\times\ell$ start block $\mathbf{X}$ with independent standard normal entries. They require a block wider than the tail index, $t+2\le\ell$ or $r+2\le\ell$. The gapped bounds are proved by comparing the block Krylov range with the range of a polynomially [filtered sketch](/explore/algorithms/filtered-randomized-svd/).

{{ statement:rbki-gapped-error }}

{{ statement:nlalib-integral-frobnorm-sub-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix }}

{{ statement:rbki-gapless-error }}

{{ statement:nlalib-integral-specnorm-sub-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix }}

The same result groups contain a form in every unitarily invariant norm for the Gram residual and forms that give a sufficient depth $q$ for a relative accuracy $\varepsilon$; they are in the Library.

## Block sizes below the target rank

The statements in this section hold for narrow start blocks, down to a single start vector. The tail bounds assume a relative gap $\Delta$ among the leading singular values and a depth $q$ at least the number of those singular values; the expectation bounds above need no gap $\Delta$ but a block of at least $t+2$ or $r+2$ columns.

{{ statement:rbki-simulated-block }}

{{ statement:rbki-block-monotonicity }}

{{ statement:nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianvector }}

{{ statement:nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianmatrix }}

The deterministic bounds for a given start vector and a polynomial filter, in the spectral and Frobenius norms, and the exactness of the single-vector iteration at depth $q\ge t$ for a matrix of rank at most $t$ with $\sigma_0>\sigma_1>\cdots>\sigma_{t-1}$, are listed under Further results with their complete hypotheses.

## Lower bound

The following is a lower bound on the error of this particular method, not an upper guarantee. It holds for every start block of a given width, so it is not a statement about a random block.

{{ statement:rbki-multiplicity-lower-bound }}

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
