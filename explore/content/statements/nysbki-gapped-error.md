---
kind: statement
id: nysbki-gapped-error
uid: d74a9224-eb70-5c39-9686-25440e2eceab
---

::: theorem result:nysbki-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $q\ge1$, let $r=h+1$ be the number of head eigenvalues, and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{nysbki}(\mathbf{A},\mathbf{X},q)\|_2\le\sigma_r+4e^{-4\sqrt2\,(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_*,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::
