---
uid: 65aaffc2-6f63-5832-99f3-38c03a0e1763
kind: algorithm
id: pivoted-cholesky
title: Pivoted Cholesky
summary: Factor a positive-semidefinite matrix by selecting residual diagonal pivots.
status: ready
result_ids:
- pivoted-cholesky-rank
theory:
- spectral-theory
- matrix-factorization-theory
- best-rank-approximation
families:
- matrix-factorizations
---

Pivoted Cholesky selects residual diagonal pivots and applies symmetric row and column exchanges. The stored scalar implementation below computes a full exact factor for every real PSD matrix, including singular input, and returns its actual exchange log.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:pivoted-cholesky-7ba672b5 }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
