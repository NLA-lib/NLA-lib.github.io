---
kind: algorithm
id: cgls
title: CGLS
summary: Apply a conjugate-gradient recurrence to a least-squares problem.
status: outline
order: 8
theory:
- krylov-spaces
- singular-values
uses:
- conjugate-gradient
families:
- residual-minimization-methods
library_results: false
result_ids:
- cgls
---

Apply a conjugate-gradient recurrence to a least-squares problem.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="CGLS"
For $\min_{\mathbf x}\|\mathbf A\mathbf x-\mathbf b\|_2$, apply the mathematical CG iteration to the normal equations $\mathbf A^{\mathsf{H}}\mathbf A\mathbf x=\mathbf A^{\mathsf{H}}\mathbf b$. Compute products through $\mathbf A$ and its adjoint rather than explicitly forming their Gram matrix. Full column rank makes the normal-equation matrix positive definite. Rank-deficient inputs require the corresponding breakdown and solution-selection conventions.
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
