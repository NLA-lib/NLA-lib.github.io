---
uid: 5577bd65-7224-5044-8cfc-227cf0b78ffc
kind: algorithm
id: hutchpp
title: Hutch++
summary: Combine a low-rank approximation with residual trace estimation.
status: outline
order: 19
theory:
- random-matrices
- concentration
library_algorithm: hutchpp
uses:
- girard-hutchinson
- qr
search_aliases:
- Hutch plus plus
- trace estimation
source_guides:
- docs/algorithms/HutchPlusPlus.md
result_ids:
- hutchpp-unbiased
---

Combine a low-rank approximation with residual trace estimation.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:nlalib-hutchpp-b6d6ec43 }}



## Components

{{ generated:components }}

## Mathematical guarantees

{{ statement:hutchpp-unbiased }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
