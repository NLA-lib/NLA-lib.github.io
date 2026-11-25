---
kind: statement
id: relative-error-blas-matvec-5bd8642a
uid: 5bd8642a-3621-59ba-b33e-e63b422d2803
---

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

The library's matrix–vector contract has an absolute allowance $\delta$ in place of
$e_m\|\mathbf{A}\|_2$; the CG theorems take $\delta=e_m\|\mathbf{A}\|_2$.

Scalar arithmetic has unit roundoff $u$. Copies and decoded comparisons are exact.
The solver theorem requires the supplied coefficients to satisfy its accuracy budget.
:::
