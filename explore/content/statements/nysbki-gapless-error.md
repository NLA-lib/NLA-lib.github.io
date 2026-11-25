---
kind: statement
id: nysbki-gapless-error
uid: 18fb3656-465b-5da8-bce5-1fa5a2eab23c
---

::: theorem result:nysbki-gapless-error name="Expected spectral error without a gap" id=gapless
Let $q\ge2$ and let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{nysbki}(\mathbf{A},\mathbf{X},q)\|_2\le\sigma_r\exp\!\biggl(\frac{\log^2(4\rho)}{16(q-1)^2}\biggr),\qquad\rho=1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf{A}^{1/2}-[\mathbf{A}^{1/2}]_r\|_{\mathrm F}^2}{\sigma_r(\mathbf{A}^{1/2})^2}.$$

The library also proves $\rho=1+\dfrac{r}{\ell-r-1}\,\dfrac{\|\mathbf{A}-[\mathbf{A}]_r\|_*}{\sigma_r}$. No gap between eigenvalues is assumed.
:::
