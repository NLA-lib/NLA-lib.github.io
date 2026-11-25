---
kind: statement
id: rbki-single-vector-gapless-error
uid: 023fc92c-a7f4-5544-8eaf-7774ad5ced2f
---

::: theorem result:rbki-single-vector-gapless-error name="Single start vector, relative form" id=single-vector-gapless
Let $\mathbf{x}\in\mathbb R^n$ have independent standard normal entries. Fix a target rank $r$, a depth $q\ge r$, $\delta>0$, and $\varepsilon>0$. Suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<r$. Then

$$\mathbb P\Bigl[\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{x},q)]_r\|_2^2>(1+\varepsilon)^2\sigma_r^2+32\,e^{-8(q-r)\sqrt{\varepsilon/(2+\varepsilon)}}\,\Delta^{-2(r-1)}\,\frac{r^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2\Bigr]\le\delta.$$

No gap between $\sigma_{r-1}$ and $\sigma_r$ is assumed. The gap $\Delta$ among the first $r$ singular values is still required.
:::
