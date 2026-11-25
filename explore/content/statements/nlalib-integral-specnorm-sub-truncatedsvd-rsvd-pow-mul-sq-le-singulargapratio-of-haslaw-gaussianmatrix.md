---
kind: statement
id: nlalib-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: ce90654e-db13-5ef8-bd4d-3c665dd98c60
---

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected spectral error with a gap" id=gapped-spectral
Let $r=h+1$ be the number of head singular values and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-[\mathsf{rsi}(\mathbf{A},\mathbf{X},p)]_r\|_2^2\le\sigma_r^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::
