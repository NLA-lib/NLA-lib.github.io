---
kind: algorithm
id: nystrom-bki
title: Nyström block Krylov iteration
summary: Use a block Krylov construction in a Nyström approximation.
status: outline
order: 16
theory:
- krylov-spaces
- random-matrices
library_algorithm: nystrom-bki
uses:
- nystrom
library_results: false
result_ids:
- nysbki-gapless-error
- nysbki-gapped-error
---

Use a block Krylov construction in a Nyström approximation.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.nystromBKI name="Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf A$, build the test matrix $[\mathbf\Omega,\mathbf A\mathbf\Omega,\ldots,\mathbf A^{q-1}\mathbf\Omega]$ with $q$ blocks, then apply the Nyström construction using this entire block Krylov range. The powers are retained together rather than keeping only the last one.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
