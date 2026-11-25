---
uid: 90de437f-ae63-5ccf-beb3-17d345efa4c7
kind: algorithm
id: filtered-randomized-svd
title: Filtered RSVD
summary: Apply a polynomial filter before constructing a randomized range approximation.
status: outline
order: 13
families:
- subspace-iteration-methods
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

Apply a polynomial filter before constructing a randomized range approximation. Subspace iteration is the monomial case. The bound for a general filter is also the comparison through which the gapped block Krylov bounds are proved: singular value by singular value, the error of randomized block Krylov iteration with $q$ blocks is at most that of the range finder at the test matrix $f(\mathbf{A}^{\mathsf{H}}\mathbf{A})\mathbf\Omega$, for every polynomial $f$ of degree less than $q$.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:filtered-range-finder-approximation-36be1f8d }}

## Components

{{ generated:components }}

## Mathematical guarantees

{{ statement:nlalib-integral-specnorm-sub-rsvd-aeval-sq-le-of-haslaw-gaussianmatrix }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
