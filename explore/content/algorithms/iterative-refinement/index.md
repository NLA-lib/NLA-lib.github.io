---
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

Iterative refinement improves an approximate solution of $\mathbf A\mathbf x=\mathbf b$ by repeatedly computing its residual, solving for a correction, and adding it. Its three operations need different accuracy, so they can run in different precisions: a cheap low-precision factorization can drive the iteration while the residual is computed more accurately. Carson and Higham's analysis of refinement in three precisions is the standard reference.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Iterative refinement"
For an invertible $\mathbf A$, a right-hand side $\mathbf b$ and a start $\mathbf x_0$, repeat for $j=0,1,\dots$:

$$\mathbf r_j\approx\mathbf b-\mathbf A\mathbf x_j,\qquad\mathbf d_j\approx\mathbf A^{-1}\mathbf r_j,\qquad\mathbf x_{j+1}\approx\mathbf x_j+\mathbf d_j.$$

In exact arithmetic the first correction gives the solution. The method is of interest because each $\approx$ is a different computation with a different error.
:::

In refinement in three precisions the residual is computed at unit roundoff $u_r$ and stored at the working unit roundoff $u$, the correction is solved with factors computed at unit roundoff $u_f$, and the update is at $u$.

## A run with bounded local errors

The library analyses a run through four accuracy parameters, one for each source of error. They are not unit roundoffs, so the same theorem applies to any way of computing the three operations.

::: definition decl:NLAlib.RefinementRun name="Refinement run" id=run
A run of $k$ steps for an invertible $\mathbf A$ consists of iterates, residuals and corrections with, for every $j<k$,

$$\|\mathbf b-\mathbf A\mathbf x_j-\mathbf r_j\|\le\zeta\|\mathbf b-\mathbf A\mathbf x_j\|+\eta\bigl(\|\mathbf b\|+\|\mathbf A\|_2\|\mathbf x_j\|\bigr),$$

$$\|\mathbf A^{-1}\mathbf r_j-\mathbf d_j\|\le\theta\|\mathbf A^{-1}\mathbf r_j\|,\qquad\|\mathbf x_j+\mathbf d_j-\mathbf x_{j+1}\|\le\varepsilon\|\mathbf x_j+\mathbf d_j\|,$$

with $\theta,\eta,\zeta,\varepsilon\ge0$. The start is unrestricted, and no smallness of the parameters is assumed.
:::

The residual has two parameters because it has two errors: $\eta$ is the error of computing it, relative to the size of its operands, and $\zeta$ is the error of rounding the result to the working precision, relative to the residual itself.

::: theorem result:iterative-refinement-forward-error name="Forward error of iterative refinement" id=forward-error
Let $\mathbf A\mathbf x_\star=\mathbf b$, $\kappa=\kappa_2(\mathbf A)$, and

$$\varphi=(1+\varepsilon)\bigl(\theta+(1+\theta)\kappa(\zeta+\eta)\bigr),\qquad\xi=(1+\varepsilon)(1+\theta)\,2\kappa\eta+\varepsilon.$$

If $\varphi<1$, every iterate $j\le k$ of a run satisfies

$$\|\mathbf x_\star-\mathbf x_j\|\le\varphi^j\|\mathbf x_\star-\mathbf x_0\|+\frac{\xi}{1-\varphi}\|\mathbf x_\star\|.$$
:::

::: theorem decl:NLAlib.RefinementRun.norm_sub_x_succ_le name="One step" id=one-step
For $\mathbf A\mathbf x_\star=\mathbf b$ and every $j<k$, with $\varphi$ and $\xi$ as above and no condition on their size,

$$\|\mathbf x_\star-\mathbf x_{j+1}\|\le\varphi\|\mathbf x_\star-\mathbf x_j\|+\xi\|\mathbf x_\star\|.$$
:::

The solve accuracy comes from the backward error of the solver:

::: theorem decl:NLAlib.norm_inv_mulVec_sub_le_of_add_mulVec_eq name="A backward stable solve has a small relative error" id=solve-accuracy
If $\mathbf A$ is invertible, $(\mathbf A+\mathbf E)\mathbf d=\mathbf r$ and $\|\mathbf A^{-1}\mathbf E\|_2\le\omega<1$, then

$$\|\mathbf A^{-1}\mathbf r-\mathbf d\|\le\frac{\omega}{1-\omega}\|\mathbf A^{-1}\mathbf r\|.$$

So $\theta=\omega/(1-\omega)$, and $\|\mathbf E\|_2\le c\,u_f\|\mathbf A\|_2$ allows $\omega=c\,\kappa_2(\mathbf A)u_f$.
:::

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

Carson and Higham (*Accelerating the solution of linear systems by iterative refinement in three precisions*, SIAM J. Sci. Comput. 40, 2018, Theorem 3.2 and Corollary 3.3) work in the $\infty$-norm with componentwise residual bounds and reach the limiting accuracy $4pu_r\operatorname{cond}(\mathbf A,\mathbf x)+u$, with $p$ the largest number of nonzeros in a row of $[\mathbf A\ \mathbf b]$. The theorem above differs in three ways:

- It is normwise in the 2-norm, so $\kappa_2(\mathbf A)$ replaces $\operatorname{cond}(\mathbf A,\mathbf x)$. This is weaker for badly scaled systems.
- Its rate $\varphi$ contains $\kappa(\zeta+\eta)$. Their rate depends only on the solve, through a quantity $\mu_i$ that this analysis does not track.
- Their normwise and componentwise backward-error results are not covered.

## Appears under these tasks

{{ generated:task-membership }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}
