---
kind: statement
id: nlalib-lanczosquadrature-6d8b12f4
uid: 6d8b12f4-2783-5f4b-8c76-53d3c62f914f
---

::: definition decl:NLAlib.lanczosQuadrature name="Lanczos quadrature"
For Hermitian $\mathbf{A}$ and nonzero $\mathbf{b}$, approximate the quadratic form by

$$\mathbf{b}^{\mathsf{H}}f(\mathbf{A})\mathbf{b}\approx\|\mathbf{b}\|_2^2\mathbf{e}_1^{\mathsf{H}}f(\mathbf{T}_k)\mathbf{e}_1.$$

The eigenvalues of the Lanczos compression $\mathbf{T}_k$ provide quadrature nodes; the squared first components of its normalized eigenvectors provide weights. The function, interval, and derivative assumptions determine which error bounds apply.
:::
