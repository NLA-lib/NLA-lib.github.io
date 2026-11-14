---
kind: algorithm
id: inverse-iteration
title: Inverse iteration
summary: Use shifted linear solves to target an eigenvector near a chosen shift.
status: outline
theory:
- spectral-theory
- perturbation-theory
---

::: definition name="Inverse iteration"
Choose a shift $\mu$ such that $\mathbf A-\mu\mathbf I$ is invertible. At each step solve $(\mathbf A-\mu\mathbf I)\mathbf y_{j+1}=\mathbf x_j$ and normalize $\mathbf y_{j+1}$. Fixed-shift inverse iteration and a changing Rayleigh-quotient shift have different convergence hypotheses. The factorization or inner solver is an implementation choice.
:::

## Implementations

{{ generated:implementations }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
