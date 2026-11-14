---
kind: algorithm
id: polar-minimax-polynomial
title: Polynomial polar iteration
summary: Apply a sequence of odd polynomial singular-value filters.
status: outline
library_algorithm: polar-minimax-polynomial
library_results: false
result_ids:
- polar-minimax-polynomial-iteration
theory:
- matrix-functions
- singular-values
search_aliases:
- Polynomial polar iteration
families:
- polar-iterations
---

::: definition decl:NLAlib.oddMatrixIterate name="Polynomial polar iteration"
Choose a sequence of odd polynomial updates, evaluated in Gram form as $\mathbf X\,p_j(\mathbf X^{\mathsf{H}}\mathbf X)$. This applies the corresponding odd scalar polynomial to the singular values while retaining their singular-vector directions. Coefficient choices and the initial singular-value interval determine the certified approximation to the polar factor.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
