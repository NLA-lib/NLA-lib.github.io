---
kind: statement
id: entry-4e147cee-35a0-58d0-9c56-ffaf46edccb4
uid: 4e147cee-35a0-58d0-9c56-ffaf46edccb4
---
::: theorem result:minres-spectrum-minimax-sharp name="The spectrum-minimax bound for MINRES is attained"
For $n$ nonempty and Hermitian
$\mathbf{A}$ (indefinite or singular allowed), every start $\mathbf{x}_0$ and every $q$ there is a
$\mathbf{b}$ with $\mathbf{r}_0 = \mathbf{b} - \mathbf{A}\mathbf{x}_0 \ne \mathbf{0}$ and
$$\|\mathbf{b} - \mathbf{A}\,\mathsf{gmresIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, q)\|
= \mathsf{residualMinimax}(\sigma(\mathbf{A}), q)\,\|\mathbf{r}_0\| \,.$$
So `Matrix.IsHermitian.norm_sub_mulVec_gmresIterate_le_residualMinimax_mul` cannot be improved
for any spectrum. For singular $\mathbf{A}$ the value is $1$ ($p(0) = 1$ on the eigenvalue $0$).
The initial residual carries the dual weights of
`exists_residualMinimax_sq_le_sum_mul_norm_sq` as its spectral weights.
The source locators require checking.
:::
