---
kind: algorithm
id: srht
title: Subsampled randomized Hadamard transform
summary: Combine randomized signs, a structured orthogonal transform, and sampling.
status: outline
order: 30
theory:
- random-matrices
- concentration
- sketching-theory
library_results: false
result_ids:
- srht-flattening
- srht-ose
- srht-osi
- srht-pcp
- jl-srht
- amm-srht-spectral
---

Combine randomized signs, a structured orthogonal transform, and sampling.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.srhtMatrix name="Subsampled randomized Hadamard transform"
For a dimension admitting a normalized Hadamard matrix $\mathbf H$, form $\mathbf S=\sqrt{n/s}\,\mathbf R\mathbf H\mathbf D$, where $\mathbf D$ contains independent random signs and $\mathbf R$ selects $s$ rows. Sampling without replacement requires $1\le s\le n$. The library's more general structured-transform definition also accepts a supplied orthogonal transform; sampling with replacement is a separate law.
:::



## Mathematical guarantees

::: theorem result:srht-flattening name="Flattening the leverage scores"
Let $\mathbf F$ be an $n\times n$ unitary transform satisfying $n|\mathbf F_{ij}|^2\le\beta$, and let $\mathbf D$ contain independent Rademacher signs. For an input subspace of dimension $d$ and $t\ge0$, with failure probability at most $ne^{-t}$, every leverage score after applying $\mathbf F\mathbf D$ is at most

$$\frac{\beta(d+2\sqrt{dt}+2t)}{n}.$$

Random signs and the bounded orthogonal transform spread the subspace across coordinates before row sampling.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
