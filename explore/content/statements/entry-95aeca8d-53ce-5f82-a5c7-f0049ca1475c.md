---
kind: statement
id: entry-95aeca8d-53ce-5f82-a5c7-f0049ca1475c
uid: 95aeca8d-53ce-5f82-a5c7-f0049ca1475c
---
::: theorem result:gmres-arnoldi name="The Arnoldi basis yields GMRES"
For every $\mathbf{A}$ and $q$: with
$\mathbf{r}_0 = \mathbf{b} - \mathbf{A}\mathbf{x}_0$, the canonical bases
$\mathbf{Q}_j = \mathsf{arnoldiMatrix}(\mathbf{A}, \mathbf{r}_0, j)$ and
$\underline{\mathbf{H}}_q = \mathbf{Q}_{q+1}^{\mathsf{H}}\mathbf{A}\mathbf{Q}_q$,
$\mathsf{gmresIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, q) = \mathbf{x}_0 +
\|\mathbf{r}_0\|\,\mathbf{Q}_q\underline{\mathbf{H}}_q^{+}\mathbf{e}_0$, with no grade
hypothesis. The cited accounts give (8) and (6.29)–(6.30), using the least-squares minimiser of
$\|\|\mathbf{r}_0\|\mathbf{e}_0 - \underline{\mathbf{H}}_q\mathbf{y}\|$ in place of the
pseudoinverse, for $q$ up to the breakdown step.
:::
