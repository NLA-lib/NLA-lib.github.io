---
kind: statement
id: countsketch-second-moment
uid: 257222e6-7828-5cbd-82ba-e05f7e257514
---

::: theorem result:countsketch-second-moment name="Exact squared Gram error"
Let $\mathbf{U}\in\mathbb{R}^{n\times d}$ have orthonormal columns, and let $\mathbf{S}$ be a standard [CountSketch](/explore/statements/161d8fd6-2f0a-5e7e-8b4c-e7e67c1e6289/) with $s\ge1$ rows. Write $\ell_i=\|\mathbf{U}_{i,:}\|_2^2$ for its leverage scores. Then

$$\mathbb{E}\|(\mathbf{S}\mathbf{U})^{\mathsf{T}}\mathbf{S}\mathbf{U}-\mathbf{I}\|_{\mathrm F}^2=\frac{d^2+d-2\sum_i\ell_i^2}{s}.$$

This is the real specialization of the checked real-or-complex identity. It gives the exact mean squared distortion of the subspace Gram matrix.
:::
