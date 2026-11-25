---
kind: statement
id: cgs2-basis-extension
uid: 501be497-13e8-5f2d-b5bc-aeb5ccee7c75
---

::: theorem result:cgs2-basis-extension name="Two exact passes give an exact extension"
Let $\mathbf{Q}$ be an arbitrary real or complex matrix with $k$ columns, $\mathbf{W}$ a block of $\ell$ columns, and write $\operatorname{su}(\mathbf{M})$ for the strictly upper triangular part of $\mathbf{M}$. Suppose

$$\mathbf{H}_1=\mathbf{Q}^{\mathsf{H}}\mathbf{W},\quad\mathbf{R}_1=\operatorname{su}(\mathbf{Q}'^{\mathsf{H}}\mathbf{W}),\quad\mathbf{W}_1=\mathbf{W}-\mathbf{Q}\mathbf{H}_1-\mathbf{Q}'\mathbf{R}_1,$$

$$\mathbf{H}_2=\mathbf{Q}^{\mathsf{H}}\mathbf{W}_1,\quad\mathbf{R}_2=\operatorname{su}(\mathbf{Q}'^{\mathsf{H}}\mathbf{W}_1),\quad\mathbf{W}_2=\mathbf{W}_1-\mathbf{Q}\mathbf{H}_2-\mathbf{Q}'\mathbf{R}_2,$$

and that each column of $\mathbf{Q}'$ is the corresponding column $\mathbf{w}$ of $\mathbf{W}_2$ divided by its norm, or the zero column when $\mathbf{w}=\mathbf 0$. Then $\mathbf{Q}'$ with coefficients $\mathbf{H}_1+\mathbf{H}_2$ and $\mathbf{R}_1+\mathbf{R}_2+\mathbf{D}$, where $\mathbf{D}$ is the diagonal matrix of the norms of the columns of $\mathbf{W}_2$, is an exact extension of $\mathbf{Q}$ by $\mathbf{W}$.

No hypothesis is made on $\mathbf{Q}$. Orthonormality of its nonzero columns enters only through the clause of the contract that preserves it.
:::
