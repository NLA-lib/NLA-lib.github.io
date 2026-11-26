---
kind: statement
id: nlalib-lanczosquadrature-6d8b12f4
uid: 6d8b12f4-2783-5f4b-8c76-53d3c62f914f
---

::: definition decl:NLAlib.lanczosQuadrature name="Lanczos quadrature"
For [Hermitian](/explore/statements/49f5c3f6-f926-5bc6-b401-16993ec1e357/) $\mathbf{A}$ and nonzero $\mathbf{b}$, approximate the quadratic form by

$$\mathbf{b}^{\mathsf{H}}f(\mathbf{A})\mathbf{b}\approx\|\mathbf{b}\|_2^2\mathbf{e}_1^{\mathsf{H}}f(\mathbf{T}_k)\mathbf{e}_1.$$

The eigenvalues of the [Lanczos compression](/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/) $\mathbf{T}_k$ provide quadrature nodes; the squared first components of its normalized eigenvectors provide weights. The function, interval, and derivative assumptions determine which error bounds apply.
:::
