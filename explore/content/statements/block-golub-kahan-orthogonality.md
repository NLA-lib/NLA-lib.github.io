---
kind: statement
id: block-golub-kahan-orthogonality
uid: 744bc84b-2659-5cf7-9107-9cf1b628c872
---

::: theorem result:block-golub-kahan-orthogonality name="Orthogonality of the computed bases" id=orthogonality
Let $\mathbf{U}$ ($q\ell$ columns) and $\mathbf{V}$ ($(q+1)\ell$ columns) be the bases of a rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$, and let $\mathbf{D}(\cdot)$ be the Gram defect on the support. If $\mu\ge0$ and $\sqrt{3q\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{U})\|_{\mathrm{F}}\le\sqrt{3q\ell}\,\mu.$$

If $\mu\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{V})\|_{\mathrm{F}}\le\sqrt{3(q+1)\ell}\,\mu.$$

The bounds measure orthonormality of the nonzero columns; dropped columns are allowed.
:::
