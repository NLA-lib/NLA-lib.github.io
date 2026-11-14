---
kind: algorithm
id: preconditioned-minres
title: Preconditioned MINRES
summary: Minimize a preconditioned residual norm for a Hermitian system.
status: outline
result_ids:
- pminres-optimality
- pminres-polynomial-bound
- pminres-chebyshev-bound
- pminres-finite-termination
- pminres-lanczos
- pminres-split-system
- preconditioned-lanczos-recurrence
theory:
- krylov-spaces
- spectral-theory
- projection-methods
families:
- residual-minimization-methods
---

::: definition name="Preconditioned MINRES"
For Hermitian $\mathbf A$ and a positive-definite inverse preconditioner $\mathbf M$, apply mathematical MINRES to $\mathbf M^{1/2}\mathbf A\mathbf M^{1/2}\mathbf y=\mathbf M^{1/2}\mathbf b$ and recover $\mathbf x=\mathbf M^{1/2}\mathbf y$. The corresponding original residual is measured in the $\mathbf M$-norm. The transformed spectrum, rather than the original spectrum alone, enters convergence bounds.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
