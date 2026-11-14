---
kind: algorithm
id: plu
title: PLU factorization
summary: Use row permutations in a lower–upper triangular factorization.
status: outline
theory:
- subspaces
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- partial-pivoting-growth
- partial-pivoting-success
- partial-pivoting-growth-sharp
library_algorithm: partial-pivoting
search_aliases:
- partial pivoting
- Gaussian elimination with partial pivoting
- GEPP
---

::: definition name="PLU factorization"
With the row-permutation convention used here, $\mathbf P\mathbf A=\mathbf L\mathbf U$, where $\mathbf P$ is a permutation matrix, $\mathbf L$ is unit lower triangular, and $\mathbf U$ is upper triangular. Pivot-selection rules are implementation choices.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

Permutation conventions, existence conditions, and solve guarantees will be curated here.

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
