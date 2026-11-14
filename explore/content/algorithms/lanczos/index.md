---
kind: algorithm
id: lanczos
title: Lanczos process
summary: Build a Krylov basis and a tridiagonal compression of a symmetric operator.
status: outline
order: 1
theory:
- krylov-spaces
- spectral-theory
- orthogonal-polynomials
- finite-precision-krylov
library_algorithm: lanczos
search_aliases:
- Lanczos recurrence
- Lanczos tridiagonalization
- finite precision Lanczos
- matrix-free Lanczos
source_guides:
- docs/algorithms/Lanczos.md
library_results: false
result_ids:
- lanczos-breakdown
- lanczos-recurrence
- lanczos-tridiagonal
- lanczos-orthogonal-polynomials
- lanczos-jacobi-matrix
- random-start-lanczos
- kaniel-paige-saad
- ritz-value-gap-free
---

Build a Krylov basis and a tridiagonal compression of a symmetric operator.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Lanczos process"
For a Hermitian matrix $\mathbf A$ and starting vector $\mathbf b$, build a graded orthonormal basis $\mathbf Q_k$ of $\mathcal K_k(\mathbf A,\mathbf b)$. The compression $\mathbf T_k=\mathbf Q_k^{\mathsf{H}}\mathbf A\mathbf Q_k$ is Hermitian tridiagonal. In exact arithmetic, each new basis vector can be generated with a three-term recurrence. Breakdown means the next Krylov direction is zero; the generated space is then invariant. Reorthogonalization changes the concrete recurrence and its rounded behavior.
:::



## Mathematical guarantees

::: theorem result:lanczos-tridiagonal name="Tridiagonal compression"
Let $\mathbf A$ be Hermitian and let $\mathbf Q_k$ be a graded Krylov basis. Then $\mathbf Q_k^{\mathsf{H}}\mathbf A\mathbf Q_k$ is tridiagonal. This structure is the mathematical reason that Lanczos can use a short recurrence.
:::

## Uses and composed algorithms

Lanczos is a shared process. Its compression supports several tasks; evaluating a function or averaging random probes adds further algorithmic steps, represented by their own pages.

{{ generated:applications }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
