---
kind: statement
id: nlalib-integral-frobnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: 09cd1af3-5651-547a-a481-b16bf9a1dcba
---

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Under the same hypotheses ($r=h+1\le t$, $t+2\le\ell$),

$$\mathbb E\|\mathbf{A}-[\mathsf{rsi}(\mathbf{A},\mathbf{X},p)]_r\|_{\mathrm F}^2\le\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2.$$
:::
