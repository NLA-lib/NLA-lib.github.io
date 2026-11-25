---
kind: statement
id: block-golub-kahan-forward-error
uid: a9113600-2f7a-5cd9-a415-1e61064f8920
---

::: theorem result:block-golub-kahan-forward-error name="Forward bound for the returned factors" id=forward-error
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. Let $\mathbf{P}_{\mathbf{U}}$ be the orthogonal projector onto the range of the computed $\mathbf{U}$. Then, in the Frobenius norm and in the spectral norm,

$$\|\mathbf{A}-\mathbf{U}\mathbf{S}^{\mathsf{T}}\mathbf{V}^{\mathsf{T}}\|\le\|(\mathbf{I}-\mathbf{P}_{\mathbf{U}})\mathbf{A}\|+\Bigl(\sqrt{3q\ell}\,\mu+\sqrt{1+\eta_0}\,\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\Bigr)\|\mathbf{A}\|_2,$$

where the two unsubscripted norms are the same norm and the last factor is the spectral norm in both cases. The comparison is with the projection of $\mathbf{A}$ onto the computed left range. The statement does not bound the distance from that range to the exact block Krylov range.
:::
