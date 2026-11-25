---
kind: statement
id: nlalib-computation-norm-inv-mulvec-sub-le-of-ischoltrace
uid: 5b8c8de4-ac54-5a02-a6ea-5cf2c96cee62
---

::: theorem decl:NLAlib.Computation.norm_inv_mulVec_sub_le_of_isCholTrace name="The solve with the computed factors" id=solve
With a computed Cholesky factor as above, $24(n+1)^2(u+v)\kappa_2(\mathbf{A})\le1$, a right-hand side read with relative error $v$, and forward and back substitution at unit roundoff $u$, the computed $\mathbf{d}$ satisfies

$$\|\mathbf{A}^{-1}\mathbf{r}-\mathbf{d}\|\le24(n+1)^2(u+v)\kappa_2(\mathbf{A})\|\mathbf{A}^{-1}\mathbf{r}\|.$$
:::
