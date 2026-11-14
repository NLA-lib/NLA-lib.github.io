---
kind: algorithm
id: lu
title: LU factorization
summary: Factor a matrix into lower- and upper-triangular factors without row permutations.
status: outline
theory:
- subspaces
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- lu-existence
- lu-row-inclusion
---

::: definition name="LU factorization"
An LU factorization has the form $\mathbf A=\mathbf L\mathbf U$, with $\mathbf L$ unit lower triangular and $\mathbf U$ upper triangular. The unpivoted method needs conditions ensuring elimination can proceed; such a factorization is not available for every matrix with a fixed row order.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

Existence conditions, factorization identities, and solve guarantees will be curated here.

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
