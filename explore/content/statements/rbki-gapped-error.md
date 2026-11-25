---
kind: statement
id: rbki-gapped-error
uid: 6cec8318-a6a3-5186-a4c8-1928457d0cc8
---

::: theorem result:rbki-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $q\ge1$, let $r=h+1$ be the number of head singular values, and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{X},q)\|_2^2\le\sigma_r^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$

No positivity of the gap or of $\sigma_t$ is assumed; the exponential factor decreases with the depth when $\gamma>0$.
:::
