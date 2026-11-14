---
kind: algorithm
id: gram-schmidt
title: Gram–Schmidt orthogonalization
summary: Construct an orthonormal basis from input vectors.
status: outline
order: 22
theory:
- subspaces
- matrix-factorization-theory
library_algorithm: gram-schmidt
search_aliases:
- Gram-Schmidt
- modified Gram–Schmidt
- MGS
- QR factorization
source_guides:
- docs/algorithms/Gram-Schmidt.md
result_ids:
- gram-schmidt
---

Construct an orthonormal basis from input vectors.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.gramSchmidtQ name="Gram–Schmidt orthogonalization"
Process the input columns in order. Remove from each column its components along the earlier nonzero orthonormal columns, then normalize a nonzero residual. A zero residual represents a dependent column and remains zero in the library's rank-revealing convention. Classical Gram–Schmidt forms projection coefficients from a common input residual; modified Gram–Schmidt updates that residual after each projection. Repeated passes are separate implementation choices.
:::



## Results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
