---
kind: statement
id: nyssi-gapped-error
uid: 83eaf2e3-a5c0-5758-acdf-61e684bff986
---

::: theorem result:nyssi-gapped-error name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head eigenvalues and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{nyssi}(\mathbf{A},\mathbf{X},p)\|_2\le\sigma_r+e^{-4p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_*,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::
