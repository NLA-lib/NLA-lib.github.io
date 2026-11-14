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
search_aliases:
- Hermitian diagonalization
- EIGH
- Shah diagonalization
- spectral divide and conquer
- Hermitian eigensolver in linear precision
- eigh
source_guides:
- docs/algorithms/Spectral-Bisection.md
uses:
- newton-schulz-sign
- deflation
---

Recursively split the spectrum of a Hermitian matrix, solve the smaller eigenproblems, and assemble their invariant subspaces.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Spectral bisection"
For a Hermitian matrix $\mathbf A$, a spectral split separates the invariant subspaces on either side of a shift. Compress $\mathbf A$ onto bases for these subspaces, diagonalize the compressed matrices, and lift their eigenvectors back to the original space. Recursion reduces diagonalization to smaller problems.

Randomized spectral bisection uses a matrix-sign approximation and randomized basis extraction to compute the split. The concrete implementation specifies rounding, stopping rules, and resource bounds.
:::



## Results

{{ generated:results }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
