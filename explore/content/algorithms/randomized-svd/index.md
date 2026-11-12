---
kind: algorithm
id: randomized-svd
title: Range-finder approximation (RSVD)
summary: Project the matrix onto the full range of its sketch.
status: outline
order: 10
tasks:
- low-rank-approximation
theory:
- singular-values
- random-matrices
- best-rank-approximation
library_algorithm: randomized-svd
families:
- rsvd-type-methods
library_results: false
result_ids:
- range-finder-structural-bound
- randomized-svd-expected-error
- randomized-svd-tail
- randomized-svd-lower-bound
---
Let $\mathbf Y=\mathbf A\mathbf\Omega$ and let $\mathbf P_{\mathbf Y}$ be the orthogonal projector onto its range.

::: definition decl:NLAlib.rsvd name="Range-finder approximation"
The untruncated approximation is $\mathbf B=\mathbf P_{\mathbf Y}\mathbf A$. Its rank is at most the sketch width; a target rank $k$ is not imposed at this stage.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

The range approximation is the common starting point for late truncation. Early truncation instead selects a smaller subspace from the sketch before projecting the matrix.

{{ generated:results }}



## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}
