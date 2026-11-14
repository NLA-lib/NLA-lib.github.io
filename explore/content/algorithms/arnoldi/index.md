---
kind: algorithm
id: arnoldi
title: Arnoldi process
summary: Build an orthonormal Krylov basis and an upper-Hessenberg compression.
status: outline
order: 7
theory:
- krylov-spaces
- subspaces
uses:
- gram-schmidt
library_results: false
result_ids:
- arnoldi-basis
- arnoldi-breakdown
- arnoldi-hessenberg
- arnoldi-relation
- arnoldi-recurrence
- unreduced-hessenberg-krylov-basis
---

Build an orthonormal Krylov basis and an upper-Hessenberg compression.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.arnoldiMatrix name="Arnoldi process"
For a square matrix $\mathbf A$ and starting vector $\mathbf b$, construct a graded orthonormal basis $\mathbf Q_k$ of $\mathcal K_k(\mathbf A,\mathbf b)$. Orthogonalize $\mathbf A\mathbf q_j$ against the current basis to obtain the next column. The compression $\mathbf H_k=\mathbf Q_k^{\mathsf{H}}\mathbf A\mathbf Q_k$ is upper Hessenberg. A zero residual signals that the Krylov space has stopped growing; no further nonzero basis column is available.
:::



## Mathematical guarantees

::: theorem result:arnoldi-relation name="Arnoldi relation"
For the library's canonical Krylov bases $\mathbf Q_j$, including their zero-column convention after breakdown,

$$\mathbf A\mathbf Q_k=\mathbf Q_{k+1}(\mathbf Q_{k+1}^{\mathsf{H}}\mathbf A\mathbf Q_k).$$

Thus applying the full operator to the current basis is represented in the next Krylov space by a small coefficient matrix.
:::

## Further results

{{ generated:results }}

## Components

{{ generated:components }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
