---
kind: algorithm
id: early-truncated-rsvd
title: Early-truncated RSVD
summary: Truncate the sketch first, then project the matrix onto that smaller range.
status: outline
families:
- rsvd-type-methods
theory:
- singular-values
- random-matrices
- best-rank-approximation
- sketching-theory
- randomized-low-rank-theory
result_ids:
- early-truncation-structural-bound
- early-truncation-pcp-bound
- early-truncated-rsvd-lower-bound
- etrsvd
library_results: false
---

::: definition decl:NLAlib.earlyTruncatedRSVD name="Early-truncated RSVD"
Form the sketch $\mathbf Y=\mathbf A\mathbf\Omega$, retain its best rank-at-most-$k$ approximation $[\mathbf Y]_k$, then return $\mathbf P_{[\mathbf Y]_k}\mathbf A$. The retained subspace is chosen from the sketch, rather than from the full projected matrix.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

Early truncation needs control of how the sketch preserves useful subspaces and projection costs. Its bounds belong here, separately from late truncation's error decomposition. The existing structural and projection-cost results are linked below.

{{ generated:results }}




## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
