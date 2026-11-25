---
kind: statement
id: cgls-d881b1fc
uid: d881b1fc-87da-5f4f-a75d-8d11c09f6fbf
---

::: definition name="CGLS"
For $\min_{\mathbf{x}}\|\mathbf{A}\mathbf{x}-\mathbf{b}\|_2$, apply the mathematical CG iteration to the normal equations $\mathbf{A}^{\mathsf{H}}\mathbf{A}\mathbf{x}=\mathbf{A}^{\mathsf{H}}\mathbf{b}$. Compute products through $\mathbf{A}$ and its adjoint rather than explicitly forming their Gram matrix. Full column rank makes the normal-equation matrix positive definite. Rank-deficient inputs require the corresponding breakdown and solution-selection conventions.
:::
