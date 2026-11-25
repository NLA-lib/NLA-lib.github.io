---
kind: statement
id: iterative-refinement-acb8b8c2
uid: acb8b8c2-271a-594d-9431-e0d4447ee5a0
---

::: definition name="Iterative refinement"
For an invertible $\mathbf{A}$, a right-hand side $\mathbf{b}$ and a start $\mathbf{x}_0$, repeat for $j=0,1,\dots$:

$$\mathbf{r}_j\approx\mathbf{b}-\mathbf{A}\mathbf{x}_j,\qquad\mathbf{d}_j\approx\mathbf{A}^{-1}\mathbf{r}_j,\qquad\mathbf{x}_{j+1}\approx\mathbf{x}_j+\mathbf{d}_j.$$

In exact arithmetic the first correction gives the solution. The method is of interest because each $\approx$ is a different computation with a different error.
:::
