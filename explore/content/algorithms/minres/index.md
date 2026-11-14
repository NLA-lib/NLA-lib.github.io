---
kind: algorithm
id: minres
title: MINRES
summary: Minimize the residual over a Krylov space for a symmetric system.
status: outline
order: 5
theory:
- krylov-spaces
- spectral-theory
uses:
- lanczos
families:
- residual-minimization-methods
library_results: false
result_ids:
- minres-chebyshev-bound
- minres-outlier-bound
- minres-polynomial-bound
- minres-spectrum-minimax-bound
- minres-two-interval-bound
- minres-lanczos
- minres-residual-estimate
- minres-recurrence
- minres-chebyshev-sharp
- minres-spectrum-minimax-sharp
- minres-two-interval-sharp
---

Minimize the residual over a Krylov space for a symmetric system.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="MINRES"
For a real symmetric system $\mathbf A\mathbf x=\mathbf b$, choose the iterate that minimizes the Euclidean residual norm over $\mathbf x_0+\mathcal K_k(\mathbf A,\mathbf r_0)$, where $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$. Symmetry permits a Lanczos-based short recurrence. Positive definiteness is not required for this minimization; solvability and termination claims need their own hypotheses.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
