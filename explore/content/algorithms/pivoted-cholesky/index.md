---
kind: algorithm
id: pivoted-cholesky
title: Pivoted Cholesky
summary: Factor a positive-semidefinite matrix by selecting residual diagonal pivots.
status: outline
result_ids:
- pivoted-cholesky-rank
theory:
- spectral-theory
- matrix-factorization-theory
- best-rank-approximation
families:
- matrix-factorizations
---

::: definition name="Pivoted Cholesky"
At each step, select a remaining diagonal entry of maximal residual value, permute it into the pivot position, and use it to form the next Cholesky column. Zero residual pivots detect exhausted rank in exact arithmetic. This semidefinite, rank-revealing construction is distinct from unpivoted positive-definite Cholesky.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
