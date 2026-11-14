---
kind: algorithm
id: jacobi-eigenvalue
title: Jacobi eigenvalue method
summary: Apply plane rotations to diagonalize a Hermitian matrix.
status: outline
theory:
- spectral-theory
---

::: definition name="Jacobi eigenvalue method"
For a Hermitian matrix $\mathbf A_j$, choose an off-diagonal entry and a unitary plane rotation $\mathbf J_j$ that diagonalizes the associated two-by-two principal block. Set $\mathbf A_{j+1}=\mathbf J_j^{\mathsf{H}}\mathbf A_j\mathbf J_j$ and accumulate the rotations into an eigenvector basis. Cyclic and magnitude-based pivot schedules are concrete variants. This is distinct from Jacobi iteration for linear systems.
:::

## Implementations

{{ generated:implementations }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
