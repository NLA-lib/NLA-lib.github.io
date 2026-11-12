---
kind: index
id: arithmetic-models
title: Arithmetic models
summary: Definitions of the arithmetic contracts used by the algorithm pages.
status: ready
---

An algorithm specifies which operations are performed. An arithmetic model specifies
what each operation may return. These choices are separate from the storage format,
matrix-access model, and resource charges.

::: definition name="Exact arithmetic" id=exact
Scalar arithmetic, dot products, vector updates, and matrix–vector products are exact.
The resulting CG recurrence agrees with mathematical CG, so classical convergence
and finite-termination results apply under their matrix assumptions.
:::

::: definition name="Relative-error BLAS + matvec" id=relative
The implementation supplies error coefficients rather than a particular reduction
order. The dot-product contract is

$$|\widehat{\langle\mathbf{x},\mathbf{y}\rangle}-\langle\mathbf{x},\mathbf{y}\rangle|
\le d_n\sum_{i=1}^n |x_i y_i|.$$

This scales with the sum of absolute products, not with the absolute value of the
dot product; the distinction matters when there is cancellation.

A scaled vector addition satisfies

$$|\widehat z_i-(y_i+\alpha x_i)|\le e_a(|y_i|+|\alpha x_i|),$$

and matrix–vector multiplication satisfies

$$\|\widehat{\mathbf{A}\mathbf{v}}-\mathbf{A}\mathbf{v}\|_2
\le e_m\|\mathbf{A}\|_2\|\mathbf{v}\|_2.$$

Scalar arithmetic has unit roundoff $u$. Copies and decoded comparisons are exact.
The solver theorem requires the supplied coefficients to satisfy its accuracy budget.
:::

::: definition name="Standard rounding with sequential BLAS" id=sequential
Scalar operations obey the standard relative-rounding model with unit roundoff $u$
and unbounded exponents. Dot products form rounded products and accumulate them
sequentially, giving

$$d_n=(1+u)^n-1.$$

The BLAS implementation supplies the vector-update bounds. All vector lengths are
admitted. Matvec error is supplied separately; this choice does not assume exact matvecs.
:::

::: definition name="Standard rounding with pairwise BLAS" id=pairwise
Scalar arithmetic has the same relative-rounding contract, while reductions use a
pairwise summation tree:

$$d_n=(1+u)^{\lceil\log_2 n\rceil+1}-1.$$

The implementation requires $\lceil\log_2 n\rceil<\mathrm{depth}$. Pairwise summation
specifies the reduction order; it does not by itself certify parallel execution.
Matvec error is supplied separately.
:::

::: definition name="Accuracy budgets" id=accuracy

For the abstract relative-error CG theorem, choose a nonnegative allowance $E$ with

$$u,d_n,e_a,e_m\le E\le10^{-2}.$$

The named standard profiles use a stricter envelope shared with other solvers:

$$0\le E\le10^{-2},\qquad e_m,e_a\le E,\qquad
u,d_n,e_{\mathrm{scal}}\le E/16.$$

Here $e_{\mathrm{scal}}$ bounds componentwise vector division. The CG theorem also
has spectral and iteration-window assumptions, stated on its implementation page.
:::

[Open ordinary CG](/explore/algorithms/conjugate-gradient/implementations/ordinary/)

[Computational-model theory](/explore/theory/computational-models/)
