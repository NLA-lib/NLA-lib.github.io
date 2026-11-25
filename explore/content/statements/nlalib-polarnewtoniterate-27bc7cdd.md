---
kind: statement
id: nlalib-polarnewtoniterate-27bc7cdd
uid: 27bc7cdd-514e-5fd6-8349-3561c58491be
---

::: definition decl:NLAlib.polarNewtonIterate name="Newton polar iteration"
For a rectangular real or complex matrix, start at $\mathbf{X}_0=\mathbf{A}$ and set $\mathbf{X}_{j+1}=\tfrac12(\mathbf{X}_j+(\mathbf{X}_j^{\dagger})^{\mathsf{H}})$. The adjoint pseudoinverse gives the fixed-rank extension of inverse averaging. The target is the partial-isometry factor in the polar decomposition; the result below states the singular-value assumptions and quantitative behavior.
:::
