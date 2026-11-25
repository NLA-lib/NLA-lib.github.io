---
kind: statement
id: nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix
uid: 8e47438a-9c8e-5414-ab32-1d0cdeb3e198
---

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap" id=gapless
Let $r$ be the target rank with $r+2\le\ell$ and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf{A}-[\mathsf{rsi}(\mathbf{A},\mathbf{X},p)]_r\|_2^2\le(1+\varepsilon)^2\sigma_r^2+e^{-8p\varepsilon/(2+\varepsilon)}\,\frac{r}{\ell-r-1}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2.$$

No gap between singular values is assumed.
:::
