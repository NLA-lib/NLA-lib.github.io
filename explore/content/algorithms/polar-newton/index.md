---
kind: algorithm
id: polar-newton
title: Newton polar iteration
summary: Use pseudoinverse averaging to approach a polar factor.
status: outline
library_algorithm: polar-newton
library_results: false
result_ids:
- polar-newton-iteration
theory:
- matrix-functions
- singular-values
search_aliases:
- Newton polar iteration
families:
- polar-iterations
---

::: definition decl:NLAlib.polarNewtonIterate name="Newton polar iteration"
For a rectangular real or complex matrix, start at $\mathbf X_0=\mathbf A$ and set $\mathbf X_{j+1}=\tfrac12(\mathbf X_j+(\mathbf X_j^{\dagger})^{\mathsf{H}})$. The adjoint pseudoinverse gives the fixed-rank extension of inverse averaging. The target is the partial-isometry factor in the polar decomposition; the result below states the singular-value assumptions and quantitative behavior.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
