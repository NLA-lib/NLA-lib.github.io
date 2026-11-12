---
kind: algorithm
id: plu
title: PLU factorization
summary: Use row permutations in a lower–upper triangular factorization.
status: outline
tasks:
- matrix-factorizations
- linear-systems
theory:
- subspaces
families:
- matrix-factorizations
---

::: definition name="PLU factorization"
With the row-permutation convention used here, $\mathbf P\mathbf A=\mathbf L\mathbf U$, where $\mathbf P$ is a permutation matrix, $\mathbf L$ is unit lower triangular, and $\mathbf U$ is upper triangular. Pivot-selection rules are implementation choices.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

Permutation conventions, existence conditions, and solve guarantees will be curated here.

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
