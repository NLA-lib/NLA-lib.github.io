---
kind: algorithm
id: filtered-randomized-svd
title: Filtered randomized SVD
summary: Apply a polynomial filter before constructing a randomized range approximation.
status: outline
order: 13
theory:
- polynomial-approximation
- random-matrices
library_algorithm: filtered-rsvd
uses:
- randomized-svd
library_results: false
result_ids:
- filtered-range-finder-bound
---

Apply a polynomial filter before constructing a randomized range approximation.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Filtered range-finder approximation"
Choose a spectral filter $g$ and a test matrix $\mathbf\Omega$. Form $\mathbf Y=\mathbf A g(\mathbf A^{\mathsf{H}}\mathbf A)\mathbf\Omega$ and return $\mathbf P_{\mathbf Y}\mathbf A$. Polynomial filters can be evaluated through matrix applications; the mathematical analysis also permits more general spectral filters. Power iteration is the special choice $g(t)=t^p$. Final rank truncation is a further choice.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
