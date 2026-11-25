---
kind: statement
id: nlalib-integral-specnorm-sub-rsvd-pow-mul-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix
uid: c9146d75-6940-51e0-b74c-ae8dc5904fac
---

::: theorem decl:NLAlib.integral_specNorm_sub_rsvd_pow_mul_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap, relative form" id=gapless-relative
Let $r$ be a target rank with $r+2\le\ell$ and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf{A}-\mathsf{rsi}(\mathbf{A},\mathbf{X},p)\|_2^2\le(1+\varepsilon)^2\sigma_r^2+e^{-8p\varepsilon/(2+\varepsilon)}\,\frac{r}{\ell-r-1}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2.$$

No gap is assumed and $\sigma_r>0$ is not required. This bound and the preceding one are alternative regimes for the same error.
:::
