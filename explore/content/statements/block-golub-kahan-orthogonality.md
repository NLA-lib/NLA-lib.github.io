---
kind: statement
id: block-golub-kahan-orthogonality
uid: 744bc84b-2659-5cf7-9107-9cf1b628c872
---

::: theorem result:block-golub-kahan-orthogonality name="Orthogonality of the computed bases" id=orthogonality
Let $\mathbf{A}\in\mathbb{R}^{m\times n}$, and let $\mathbf{U}\in\mathbb{R}^{m\times q\ell}$ and $\mathbf{V}\in\mathbb{R}^{n\times(q+1)\ell}$ be the bases of a [rounded block Golub--Kahan run](/explore/statements/593daa98-8a52-5a89-a792-f46844fd76d6/) with start-block width $\ell$, scheme parameters $(\eta_0,\mu,\varepsilon)$, and matrix-product parameter $\varepsilon_{\mathrm{mv}}$. Let $\mathbf{D}(\cdot)$ be the [Gram defect on the support](/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/). If $\mu\ge0$ and $\sqrt{3q\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{U})\|_{\mathrm{F}}\le\sqrt{3q\ell}\,\mu.$$

If $\mu\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{V})\|_{\mathrm{F}}\le\sqrt{3(q+1)\ell}\,\mu.$$

The bounds measure orthonormality of the nonzero columns; dropped columns are allowed.
:::
