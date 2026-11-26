---
uid: e7cd95aa-3e85-5653-99bc-9be0b33f2682
kind: algorithm
id: plu
title: PLU factorization
summary: Use row permutations in a lower–upper triangular factorization.
status: ready
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

{{ statement:plu-factorization-a6e9180a }}

Row-pivoted LU selects rows during elimination and returns factors of the row-permuted original matrix. The implementations below distinguish first-maximum partial pivoting, a fixed rational threshold policy, and partial pivoting scaled by fixed original row norms. Their current-position pivot logs compose into the final row permutation.

Partial pivoting has both exact and standard-rounding guarantees for the same stored scalar tree. Threshold and scaled policies currently present exact arithmetic. For independent row and column choices, see [PLUQ factorization](/explore/algorithms/pluq/).

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

The results below retain the mathematical partial-pivoting success and growth guarantees. Each implementation page specifies its own actual pivot policy, original-input domain, arithmetic assumptions, and stored execution bounds.

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
