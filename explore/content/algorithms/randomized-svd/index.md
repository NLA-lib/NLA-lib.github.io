---
uid: 0eae966e-5653-5752-9afb-1a4bd29f3029
kind: algorithm
id: randomized-svd
title: Range-finder approximation (RSVD)
summary: Project the matrix onto the full range of its sketch.
status: outline
order: 10
theory:
- singular-values
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
library_algorithm: randomized-svd
families:
- rsvd-type-methods
library_results: false
result_ids:
- range-finder-structural-bound
- randomized-svd-expected-error
- randomized-svd-tail
- randomized-svd-lower-bound
search_aliases:
- randomized range finder
- RSVD
---

Let $\mathbf{Y}=\mathbf{A}\mathbf\Omega$ and let $\mathbf{P}_{\mathbf{Y}}$ be the orthogonal projector onto its range.

{{ statement:nlalib-rsvd-15e6c9dc }}

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

{{ statement:randomized-svd-expected-error }}

The range approximation is the common starting point for late truncation. Early truncation instead selects a smaller subspace from the sketch before projecting the matrix.

{{ generated:results }}



## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
