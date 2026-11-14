---
kind: algorithm
id: polar-newton-schulz
title: Newton–Schulz polar iteration
summary: Use an inverse-free cubic iteration for the polar factor.
status: outline
library_algorithm: polar-newton-schulz
library_results: false
result_ids:
- polar-newton-schulz-iteration
theory:
- matrix-functions
- singular-values
search_aliases:
- Newton-Schulz polar iteration
families:
- polar-iterations
---

::: definition decl:NLAlib.polarSchulzIterate name="Newton–Schulz polar iteration"
Apply $\mathbf X_{j+1}=\tfrac12\mathbf X_j(3\mathbf I-\mathbf X_j^{\mathsf{H}}\mathbf X_j)$. This is the rectangular polar update and does not require a pseudoinverse. Initial scaling and the admissible singular-value interval are part of its convergence hypotheses.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
