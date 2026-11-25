---
kind: statement
id: rsi-gapless-error
uid: 6465b959-693e-56a3-8315-d53e6f666abd
---

::: theorem result:rsi-gapless-error name="Expected spectral error without a gap" id=gapless
Let $r$ be a target rank with $r+2\le\ell$ and $\sigma_r>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rsi}(\mathbf{A},\mathbf{X},p)\|_2^2\le\sigma_r^2\Bigl(1+\frac{r}{\ell-r-1}\,\frac{\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2}{\sigma_r^2}\Bigr)^{1/(2p+1)}.$$

No gap between singular values is assumed. At $p=0$ the right side is the range-finder bound.
:::
