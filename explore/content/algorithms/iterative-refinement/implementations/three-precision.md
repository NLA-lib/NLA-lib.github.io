---
kind: implementation
id: three-precision
algorithm: iterative-refinement
title: Cholesky refinement in three precisions
summary: A fixed scalar program that factors at one precision, computes residuals at a second and updates at a third, certified for stored positive definite matrices.
status: ready
order: 1
library_algorithm: iterative-refinement-three-precision
library_results: false
arithmetic_models:
- id: three-precisions
  title: Standard rounding at three precisions
search_aliases:
- mixed-precision Cholesky refinement
- three-precision program
- IR3 Cholesky
---

This is the library's mixed-precision program. Every arithmetic operation is a scalar operation at one of three precision tags, conversions between precisions are explicit operations, and the matrix is stored and read by the program. No operation is an oracle.

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

```text
input: A (n x n, positive definite), b, x, stored at the working precision
L := A narrowed to precision F
L := Cholesky(L), left-looking, in place, at precision F
A_R := A, b_R := b, widened to precision R
repeat k times:
    x_R := x widened to precision R
    r_R := b_R - A_R x_R, at precision R
    r   := r_R narrowed to precision W
    d   := r narrowed to precision F
    solve L y = d, then L^T d = y, in place, at precision F
    d_W := d widened to precision W
    x   := x + d_W, at precision W
output: x
```

The number of steps $k$ is fixed: the program has no stopping test. It is the routine `LinearSystems.Refinement.Rounded.solve`, built from `Cholesky.leftLooking`, `TriangularSolve.forward`, `TriangularSolve.backward`, `Refinement.residualRows`, `Refinement.addInPlace` and `Refinement.castLoop`. The matrix is stored by columns.

| Buffer | Content |
| --- | --- |
| 0 | The $n^2$ words of $\mathbf A$, read only |
| 1 | The $n$ words of $\mathbf b$, read only |
| 2 | The $n$ words of $\mathbf x_0$, overwritten by the output |

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

There are three machines, each in the standard model on all its operands, with unit roundoffs $u_f$ (factorization), $u$ (working) and $u_r$ (residual), and four casts:

| Cast | Assumption |
| --- | --- |
| Working to factorization | relative error at most $u_f$ |
| Factorization to working | exact |
| Working to residual | exact |
| Residual to working | relative error at most $u$ |

The theorem does not assume an order among $u_f,u,u_r$, but the exact widening casts are what the usual order $u_r\le u\le u_f$ provides. Overflow and underflow are not modelled, and the machines are abstract: no IEEE format is fixed.

## Operations and Storage

Each scalar operation, cast and structural instruction counts one. The work and span are at most

$$52n^3+104n^2k+97n^2+125nk+38n+113k+119$$

instructions, so factorization is $O(n^3)$ and each refinement step $O(n^2)$. The count does not distinguish the cost of an operation at different precisions. The supplied buffers hold $n^2+2n$ words, and the scratch is bounded by the static count of the program. Storage is in abstract cells of one size: the low-precision factor is not credited with using fewer bytes.

## Accuracy

::: theorem result:three-precision-iterative-refinement name="Forward error of the stored output" id=certificate
Let $\mathbf A$ be positive definite of order $n$, $\kappa=\kappa_2(\mathbf A)$, $(n+1)u_r<1$, and

$$\theta=48(n+1)^2\kappa u_f\le1,\qquad\eta=(1+u)(n+1)\gamma_{n+1}(u_r),\qquad\gamma_m=(1-u_r)^{-m}-1,$$

$$\varphi=(1+u)\bigl(\theta+(1+\theta)\kappa(u+\eta)\bigr)<1,\qquad\xi=(1+u)(1+\theta)\,2\kappa\eta+u.$$

At an admitted size, for every $\mathbf b$ and $\mathbf x_0$, every interpretation satisfying the model and every tape, the run of the fixed program succeeds within the instruction bound above, and buffer 2 then holds $\hat{\mathbf x}$ with, for $\mathbf A\mathbf x_\star=\mathbf b$,

$$\|\mathbf x_\star-\hat{\mathbf x}\|\le\varphi^k\|\mathbf x_\star-\mathbf x_0\|+\frac{\xi}{1-\varphi}\|\mathbf x_\star\|.$$
:::

An admitted size is one where these conditions hold for the identity matrix, so that the certificate covers at least one input at each size. Success is proved, not assumed: under the hypotheses every computed pivot is positive.

::: theorem result:cholesky-backward-error name="Cholesky does not break down" id=cholesky
If $\mathbf A$ is positive definite of order $n$, read with relative error $v$ and factored at unit roundoff $u$, with $4(n+1)^2(u+v)\kappa_2(\mathbf A)\le1$, then every computed pivot is positive and

$$\|\mathbf A-\hat{\mathbf L}\hat{\mathbf L}^{\mathsf T}\|_2\le2(n+1)^2(u+v)\|\mathbf A\|_2.$$
:::

::: theorem decl:NLAlib.Computation.norm_inv_mulVec_sub_le_of_isCholTrace name="The solve with the computed factors" id=solve
With a computed Cholesky factor as above, $24(n+1)^2(u+v)\kappa_2(\mathbf A)\le1$, a right-hand side read with relative error $v$, and forward and back substitution at unit roundoff $u$, the computed $\mathbf d$ satisfies

$$\|\mathbf A^{-1}\mathbf r-\mathbf d\|\le24(n+1)^2(u+v)\kappa_2(\mathbf A)\|\mathbf A^{-1}\mathbf r\|.$$
:::

The bound is normwise in the 2-norm. Its condition on $u_f$ carries a factor $(n+1)^2$ and its limiting term a factor of order $(n+1)^2\kappa u_r$; neither constant is claimed to be sharp.

## Not yet presented

- LU with pivoting, for matrices that are not positive definite.
- Concrete IEEE formats, overflow and underflow, and byte widths per precision.
- A stopping test, componentwise bounds with $\operatorname{cond}(\mathbf A,\mathbf x)$, and the backward-error results of Carson and Higham.
