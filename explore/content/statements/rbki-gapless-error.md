---
kind: statement
id: rbki-gapless-error
uid: 49c904f7-6031-57df-9638-f96650269510
---

::: theorem result:rbki-gapless-error name="Expected spectral error without a gap" id=gapless
Let $q\ge2$ and let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{X},q)\|_2^2\le\sigma_r^2\exp\!\biggl(\frac{1}{16(q-1)^2}\log^2\!\Bigl(4\Bigl(1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2}{\sigma_r^2}\Bigr)\Bigr)\biggr).$$

No gap between singular values is assumed. For fixed $\mathbf{A}$ the right side tends to $\sigma_r^2$ as $q\to\infty$.
:::
