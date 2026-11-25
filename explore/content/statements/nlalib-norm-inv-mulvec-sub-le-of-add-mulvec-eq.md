---
kind: statement
id: nlalib-norm-inv-mulvec-sub-le-of-add-mulvec-eq
uid: ca9a7176-8d3f-5ea4-bb63-fc9416576e9b
---

::: theorem decl:NLAlib.norm_inv_mulVec_sub_le_of_add_mulVec_eq name="A backward stable solve has a small relative error" id=solve-accuracy
If $\mathbf{A}$ is invertible, $(\mathbf{A}+\mathbf{E})\mathbf{d}=\mathbf{r}$ and $\|\mathbf{A}^{-1}\mathbf{E}\|_2\le\omega<1$, then

$$\|\mathbf{A}^{-1}\mathbf{r}-\mathbf{d}\|\le\frac{\omega}{1-\omega}\|\mathbf{A}^{-1}\mathbf{r}\|.$$

So $\theta=\omega/(1-\omega)$, and $\|\mathbf{E}\|_2\le c\,u_f\|\mathbf{A}\|_2$ allows $\omega=c\,\kappa_2(\mathbf{A})u_f$.
:::
