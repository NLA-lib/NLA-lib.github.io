---
kind: statement
id: nyssi-gapless-error
uid: 69730256-680f-52ed-b25b-2c3d9a9198af
---

::: theorem result:nyssi-gapless-error name="Expected spectral error without a gap" id=gapless
Let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{nyssi}(\mathbf{A},\mathbf{X},p)\|_2\le\sigma_r\,\rho^{1/(2p+1)},\qquad\rho=1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf{A}^{1/2}-[\mathbf{A}^{1/2}]_r\|_{\mathrm F}^2}{\sigma_r(\mathbf{A}^{1/2})^2}.$$

The library also proves $\rho=1+\dfrac{r}{\ell-r-1}\,\dfrac{\|\mathbf{A}-[\mathbf{A}]_r\|_*}{\sigma_r}$. No gap between eigenvalues is assumed.
:::
