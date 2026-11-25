---
kind: statement
id: nlalib-integral-frobnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: 93310fa9-d261-5f3c-b56f-f8a9bf1d8124
---

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Under the same hypotheses ($q\ge1$, $r=h+1\le t$, $t+2\le\ell$),

$$\mathbb E\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_{\mathrm F}^2\le\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2.$$
:::
