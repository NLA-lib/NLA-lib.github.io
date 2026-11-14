---
kind: algorithm
id: fom
title: Full orthogonalization method (FOM)
summary: Enforce Galerkin orthogonality using a full Krylov basis.
status: outline
theory:
- krylov-spaces
- subspaces
families:
- galerkin-methods
uses:
- arnoldi
---

::: definition name="Full orthogonalization method"
For a square system $\mathbf A\mathbf x=\mathbf b$, choose $\mathbf x_k\in\mathbf x_0+\mathcal K_k(\mathbf A,\mathbf r_0)$ so that $\mathbf r_k=\mathbf b-\mathbf A\mathbf x_k$ is orthogonal to $\mathcal K_k(\mathbf A,\mathbf r_0)$. Here $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$. The projected equations must be solvable for the iterate to be defined.
:::

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

Existence, breakdown conditions, and the relation to CG for positive-definite systems will be curated here. This outline does not assert a checked FOM theorem.

## Components

{{ generated:components }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
