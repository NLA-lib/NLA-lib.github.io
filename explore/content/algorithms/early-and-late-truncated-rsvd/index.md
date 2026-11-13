---
kind: algorithm
id: early-and-late-truncated-rsvd
title: Early-and-late-truncated RSVD
summary: Select a reduced sketch range, then truncate the projected matrix to the
  target rank.
status: outline
tasks:
- low-rank-approximation
families:
- rsvd-type-methods
theory:
- singular-values
- random-matrices
- best-rank-approximation
---

::: definition name="Early and late truncation"
Choose an intermediate rank $s\ge k$. First retain $[\mathbf A\mathbf\Omega]_s$, then form $\mathbf B_s=\mathbf P_{[\mathbf A\mathbf\Omega]_s}\mathbf A$ and return $[\mathbf B_s]_k$. The intermediate rank $s$ and output rank $k$ are separate parameters.
:::

When $s=k$, the projected matrix already has rank at most $k$, so the final truncation does not change it. With $s>k$, the two truncations serve distinct purposes.

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

A reviewed analysis combining subspace selection and final truncation will be curated here. This outline does not assert a new checked guarantee for the combined method.




## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}
