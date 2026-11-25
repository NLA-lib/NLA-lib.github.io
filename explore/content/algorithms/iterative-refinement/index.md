---
uid: cee2d3e6-fb6a-5d40-93ea-d6555a192c6f
kind: algorithm
id: iterative-refinement
title: Iterative refinement
summary: Improve a computed solution by solving for its residual, with each operation in its own precision.
status: ready
order: 28
theory:
- finite-precision
- perturbation-theory
- matrix-factorization-theory
library_algorithm: iterative-refinement
library_results: false
result_ids:
- iterative-refinement-forward-error
search_aliases:
- iterative refinement in three precisions
- three-precision iterative refinement
- mixed-precision iterative refinement
- multi-precision iterative refinement
- IR3
---

Iterative refinement improves an approximate solution of $\mathbf{A}\mathbf{x}=\mathbf{b}$ by repeatedly computing its residual, solving for a correction, and adding it. Its three operations need different accuracy, so they can run in different precisions: a cheap low-precision factorization can drive the iteration while the residual is computed more accurately. Carson and Higham's analysis of refinement in three precisions is the standard reference.

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:iterative-refinement-acb8b8c2 }}

In refinement in three precisions the residual is computed at unit roundoff $u_r$ and stored at the working unit roundoff $u$, the correction is solved with factors computed at unit roundoff $u_f$, and the update is at $u$.

## A run with bounded local errors

The library analyses a run through four accuracy parameters, one for each source of error. They are not unit roundoffs, so the same theorem applies to any way of computing the three operations.

{{ statement:nlalib-refinementrun-c07e970e }}

The residual has two parameters because it has two errors: $\eta$ is the error of computing it, relative to the size of its operands, and $\zeta$ is the error of rounding the result to the working precision, relative to the residual itself.

{{ statement:iterative-refinement-forward-error }}

{{ statement:nlalib-refinementrun-norm-sub-x-succ-le }}

The solve accuracy comes from the backward error of the solver:

{{ statement:nlalib-norm-inv-mulvec-sub-le-of-add-mulvec-eq }}

## What the bound says for three precisions

With parameters of the orders $\theta\sim\kappa u_f$, $\eta\sim u_r$ and $\zeta,\varepsilon\sim u$, then, dropping constants and dimension factors:

| Setting | $(u_f,u,u_r)$ | Convergence needs | Limiting relative error |
| --- | --- | --- | --- |
| Fixed precision | $(u,u,u)$ | $\kappa u\ll1$ | $\kappa u$ |
| Traditional, extended residual | $(u,u,u^2)$ | $\kappa u\ll1$ | $u$ |
| Low-precision factorization | $(u_f,u,u)$ | $\kappa u_f\ll1$ | $\kappa u$ |
| Three precisions | $(u_f,u,u^2)$ | $\kappa u_f\ll1$ | $u$ |

The table drops constants and dimension factors, so it is a reading of the theorem and not a library statement. The [certified three-precision program](/explore/algorithms/iterative-refinement/implementations/three-precision/) proves the parameters with their factors: $\theta=48(n+1)^2\kappa u_f$, $\eta=(1+u)(n+1)\gamma_{n+1}(u_r)$ and $\zeta=\varepsilon=u$.

The factorization precision sets the rate. It enters the limiting term only through $1+\theta$ and $1-\varphi$, so for $\varphi$ bounded away from one a less accurate solve changes that term by a constant factor.

### Relation to Carson and Higham

Carson and Higham (*Accelerating the solution of linear systems by iterative refinement in three precisions*, SIAM J. Sci. Comput. 40, 2018, Theorem 3.2 and Corollary 3.3) work in the $\infty$-norm with componentwise residual bounds and reach the limiting accuracy $4pu_r\operatorname{cond}(\mathbf{A},\mathbf{x})+u$, with $p$ the largest number of nonzeros in a row of $[\mathbf{A}\ \mathbf{b}]$. The theorem above differs in three ways:

- It is normwise in the 2-norm, so $\kappa_2(\mathbf{A})$ replaces $\operatorname{cond}(\mathbf{A},\mathbf{x})$. This is weaker for badly scaled systems.
- Its rate $\varphi$ contains $\kappa(\zeta+\eta)$. Their rate depends only on the solve, through a quantity $\mu_i$ that this analysis does not track.
- Their normwise and componentwise backward-error results are not covered.

## Appears under these tasks

{{ generated:task-membership }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}
