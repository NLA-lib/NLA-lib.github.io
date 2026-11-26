---
kind: statement
id: entry-af21c8a6-c63a-513c-b0d0-e68ca1221c5e
uid: af21c8a6-c63a-513c-b0d0-e68ca1221c5e
---
::: theorem result:gmres-petrov-galerkin name="The Petrov–Galerkin condition characterises GMRES"
For invertible $\mathbf{A}$: with
$\mathbf{r}_0 = \mathbf{b} - \mathbf{A}\mathbf{x}_0$, a vector $\mathbf{y}$ of
$\mathbf{x}_0 + \mathcal{K}_q(\mathbf{A}, \mathbf{r}_0)$ with
$(\mathbf{A}\mathbf{K}_q(\mathbf{A}, \mathbf{r}_0))^{\mathsf{H}}(\mathbf{b} - \mathbf{A}\mathbf{y})
= \mathbf{0}$, a residual orthogonal to $\mathbf{A}\mathcal{K}_q(\mathbf{A}, \mathbf{r}_0)$, is
$\mathsf{gmresIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, q)$. The parallel of
`Matrix.PosDef.eq_cgIterate_of_conjTranspose_krylovMatrix_mulVec_sub_eq_zero`.
The cited result shows, for any square matrix, that this condition is equivalent to minimising
the residual over $\mathbf{x}_0 + \mathcal{K}$, and GMRES is the method with $\mathcal{K} = \mathcal{K}_q$;
invertibility makes the minimiser unique.
:::
