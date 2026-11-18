---
kind: algorithm
id: inverse-iteration
title: Inverse iteration
summary: Use shifted linear solves to target an eigenvector near a chosen shift.
status: outline
theory:
- spectral-theory
- perturbation-theory
- pseudospectral-shattering
---

::: definition name="Inverse iteration"
Choose a shift $\mu$ such that $\mathbf A-\mu\mathbf I$ is invertible. At each step solve $(\mathbf A-\mu\mathbf I)\mathbf y_{j+1}=\mathbf x_j$ and normalize $\mathbf y_{j+1}$. Fixed-shift inverse iteration and a changing Rayleigh-quotient shift have different convergence hypotheses. The factorization or inner solver is an implementation choice.
:::

Shifted QR steps with one shift $\mu$ carry out inverse iteration on the last row: if $\mathbf Q$ is the product of the unitary factors of $m$ steps, the last row of $\mathbf Q^{\mathsf H}$ is a multiple of $\mathbf e_n^{\mathsf T}(\mathbf A-\mu\mathbf I)^{-m}$. The [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/) uses this to estimate the distance from a shift to the spectrum and to decouple one eigenvalue at a time, in rounded arithmetic.

## Implementations

{{ generated:implementations }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
