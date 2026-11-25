---
kind: statement
id: nlalib-integral-specnorm-sub-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix
uid: 1e71ef0b-3edf-5d7b-9a7b-f202eb006a97
---

::: theorem decl:NLAlib.integral_specNorm_sub_rbki_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap, relative form" id=gapless-relative
Let $q\ge1$, let $r$ be a target rank with $r+2\le\ell$, and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{X},q)\|_2^2\le(1+\varepsilon)^2\sigma_r^2+4e^{-8(q-1)\sqrt{\varepsilon/(2+\varepsilon)}}\,\frac{r}{\ell-r-1}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2.$$

No gap is assumed and $\sigma_r>0$ is not required. This bound and the preceding one are alternative regimes for the same error.
:::
