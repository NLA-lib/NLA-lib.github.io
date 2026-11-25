---
kind: statement
id: rsi-gapped-error
uid: 6d8bbd02-a064-5571-b084-98e3cfe2ee2d
---

::: theorem result:rsi-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head singular values and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rsi}(\mathbf{A},\mathbf{X},p)\|_2^2\le\sigma_r^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$

No positivity of the gap is assumed. At $p=0$ this is the range-finder bound at rank $t$ with $\sigma_t$ replaced by the larger $\sigma_r$.
:::
