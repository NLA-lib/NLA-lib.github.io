---
kind: statement
id: cholesky-backward-error
uid: 2ddefe08-7b63-50a0-a85b-a0d1f4e05a14
---

::: theorem result:cholesky-backward-error name="Cholesky does not break down" id=cholesky
If $\mathbf{A}$ is positive definite of order $n$, read with relative error $v$ and factored at unit roundoff $u$, with $4(n+1)^2(u+v)\kappa_2(\mathbf{A})\le1$, then every computed pivot is positive and

$$\|\mathbf{A}-\hat{\mathbf{L}}\hat{\mathbf{L}}^{\mathsf{T}}\|_2\le2(n+1)^2(u+v)\|\mathbf{A}\|_2.$$
:::
