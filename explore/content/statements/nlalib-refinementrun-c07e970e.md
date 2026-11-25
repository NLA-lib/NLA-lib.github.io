---
kind: statement
id: nlalib-refinementrun-c07e970e
uid: c07e970e-5e57-5ffc-95c4-0a61ec4b2f4d
---

::: definition decl:NLAlib.RefinementRun name="Refinement run" id=run
A run of $k$ steps for an invertible $\mathbf{A}$ consists of iterates, residuals and corrections with, for every $j<k$,

$$\|\mathbf{b}-\mathbf{A}\mathbf{x}_j-\mathbf{r}_j\|\le\zeta\|\mathbf{b}-\mathbf{A}\mathbf{x}_j\|+\eta\bigl(\|\mathbf{b}\|+\|\mathbf{A}\|_2\|\mathbf{x}_j\|\bigr),$$

$$\|\mathbf{A}^{-1}\mathbf{r}_j-\mathbf{d}_j\|\le\theta\|\mathbf{A}^{-1}\mathbf{r}_j\|,\qquad\|\mathbf{x}_j+\mathbf{d}_j-\mathbf{x}_{j+1}\|\le\varepsilon\|\mathbf{x}_j+\mathbf{d}_j\|,$$

with $\theta,\eta,\zeta,\varepsilon\ge0$. The start is unrestricted, and no smallness of the parameters is assumed.
:::
