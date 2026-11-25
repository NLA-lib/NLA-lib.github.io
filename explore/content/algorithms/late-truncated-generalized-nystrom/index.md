---
uid: bf33b271-6422-55ab-90ae-41f86be1d344
kind: algorithm
id: late-truncated-generalized-nystrom
title: Late-truncated GN
summary: Complete generalized Nyström, then truncate the output to the target rank.
status: outline
families:
- generalized-nystrom-methods
theory:
- pseudoinverses
- random-matrices
- best-rank-approximation
- sketching-theory
- randomized-low-rank-theory
search_aliases:
- TGN
- truncated GN
- late truncated GN
- truncated generalized Nystrom
result_ids:
- tgn-expected-error
- truncated-gn-lower-bound
uses:
- generalized-nystrom
---

Late-truncated generalized Nyström (TGN) truncates the completed GN approximation to the target rank.

{{ statement:late-truncated-gn-08c095ab }}

## Mathematical guarantees

{{ statement:nlalib-integral-frobnorm-sub-truncatedsvd-generalizednystrom-sq-le-one-add-of-haslaw-gaussianmatrix-of-truncatedgeneralizednystromrangedim-le }}

{{ statement:truncated-gn-lower-bound }}

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
