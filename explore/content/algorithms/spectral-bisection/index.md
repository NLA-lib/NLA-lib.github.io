---
kind: algorithm
id: spectral-bisection
title: Spectral bisection
summary: Use a spectral split to separate invariant subspaces.
status: ready
order: 26
theory:
- spectral-theory
- perturbation-theory
- random-sampling-models
library_algorithm: spectral-bisection
library_results: false
search_aliases:
- Hermitian diagonalization
- EIGH
- Shah diagonalization
- spectral divide and conquer
- Hermitian eigensolver in linear precision
- eigh
uses:
- newton-schulz-sign
- deflation
---

Recursively split the spectrum of a Hermitian matrix, solve the smaller eigenproblems, and assemble their invariant subspaces.

## Implementations

{{ generated:implementations }}

## Approach

Separate the spectrum of a Hermitian matrix, compress onto the resulting subspaces, solve the smaller problems, and assemble their bases. Choices of shifts, spectral splitting, randomization, arithmetic, and stopping rules specify different algorithms.

The implementations above own their numerical analysis. In particular, Shah's randomized finite-precision solver has its own precision requirements, failure probability, error guarantees, and resource bounds. This overview does not identify a single canonical exact-arithmetic recurrence.

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
