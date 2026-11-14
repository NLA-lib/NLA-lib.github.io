---
kind: algorithm
id: late-truncated-rsvd
title: Late-truncated RSVD
summary: Project onto the sketch range, then truncate the resulting approximation.
status: outline
families:
- rsvd-type-methods
theory:
- singular-values
- random-matrices
- best-rank-approximation
- randomized-low-rank-theory
uses:
- randomized-svd
---

::: definition name="Late-truncated RSVD"
Form $\mathbf B=\mathbf P_{\mathbf A\mathbf\Omega}\mathbf A$, then return $[\mathbf B]_k$, a best rank-at-most-$k$ approximation to $\mathbf B$. Here $[\cdot]_k$ denotes truncated SVD.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

::: theorem decl:NLAlib.frobNorm_sub_truncatedSVD_rsvd_sq name="Orthogonal error decomposition"
For every matrix $\mathbf A$, sketch $\mathbf\Omega$, and target rank $k$,

$$\|\mathbf A-[\mathbf B]_k\|_{\mathrm F}^2=\|\mathbf A-\mathbf B\|_{\mathrm F}^2+\|\mathbf B-[\mathbf B]_k\|_{\mathrm F}^2,\qquad\mathbf B=\mathbf P_{\mathbf A\mathbf\Omega}\mathbf A.$$

The squared error separates into the range-finding error and the error from truncating within that range.
:::




## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
