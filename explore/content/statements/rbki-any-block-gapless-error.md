---
kind: statement
id: rbki-any-block-gapless-error
uid: 188aac98-6bd6-511d-a625-99a6935d7b28
---

::: theorem result:rbki-any-block-gapless-error name="Any block size, relative form" id=any-block-gapless
Let $\mathbf{X}$ be an $n\times\ell$ matrix with independent standard normal entries, $\ell\ge1$. Fix a target rank $r$, a depth $q\ge r$, $\delta>0$, and $\varepsilon>0$, and suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<r$. Then

$$\mathbb P\Bigl[\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_2^2>(1+\varepsilon)^2\sigma_r^2+32\,e^{-8(q-r)\sqrt{\varepsilon/(2+\varepsilon)}}\,\Delta^{-2(r-1)}\,\frac{r^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2\Bigr]\le\delta.$$

The bound does not depend on $\ell$. For $r+2\le\ell$ the expectation bound above needs no gap $\Delta$.
:::
