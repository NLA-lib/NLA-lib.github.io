---
kind: statement
id: block-golub-kahan-residual
uid: b5af9bf0-05f0-5bd0-a29b-b8f4e5d279ea
---

::: theorem result:block-golub-kahan-residual name="Residuals of the two block relations" id=residuals
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. With $\mathbf{V}_{<q}$ the first $q$ blocks of $\mathbf{V}$,

$$\|\mathbf{A}\mathbf{V}_{<q}-\mathbf{U}\mathbf{R}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2,$$

$$\|\mathbf{A}^{\mathsf{T}}\mathbf{U}-\mathbf{V}\mathbf{S}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2.$$
:::
