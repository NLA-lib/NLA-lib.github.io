---
kind: statement
id: matrix-norms-19646f49
uid: 19646f49-e8db-5918-a0df-83eaf8db1648
---

::: definition name="Matrix norms"
For $\mathbf{A}\in\mathbb C^{m\times n}$,

$$\|\mathbf{A}\|_2=\sup_{\|\mathbf{x}\|_2=1}\|\mathbf{A}\mathbf{x}\|_2,\qquad\|\mathbf{A}\|_{\mathrm F}=\left(\sum_{i,j}|\mathbf{A}_{ij}|^2\right)^{1/2},\qquad\|\mathbf{A}\|_*=\sum_j\sigma_j(\mathbf{A}).$$

For $1\le p<\infty$, the Schatten $p$-norm is $(\sum_j\sigma_j(\mathbf{A})^p)^{1/p}$, where $\sigma_j(\mathbf{A})$ are the singular values from a [singular-value decomposition](/explore/statements/d5bca832-63a1-5043-ab6e-03b8402a2a55/). These norms provide different comparisons with a best low-rank approximation.
:::
