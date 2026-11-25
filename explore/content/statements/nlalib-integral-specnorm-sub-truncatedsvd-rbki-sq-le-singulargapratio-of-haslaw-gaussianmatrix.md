---
kind: statement
id: nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: 61e06e3d-bf47-552c-9e75-a9af204ad122
---

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected spectral error with a gap" id=gapped-spectral
Let $q\ge1$, let $r=h+1$ be the number of head singular values, and let $t\ge r$ be a tail index with $t+2\le\ell$. Then

$$\mathbb E\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_2^2\le\sigma_r^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2,\qquad\gamma=\frac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}.$$
:::
