---
kind: statement
id: nlalib-integral-specnorm-sub-truncatedsvd-rbki-sq-le-one-add-sq-mul-of-haslaw-gaussianmatrix
uid: ab58d6c1-feba-55f1-928f-db09057451b9
---

::: theorem decl:NLAlib.integral_specNorm_sub_truncatedSVD_rbki_sq_le_one_add_sq_mul_of_hasLaw_gaussianMatrix name="Expected spectral error without a gap" id=gapless
Let $q\ge1$, let $r$ be the target rank with $r+2\le\ell$, and let $\varepsilon>0$. Then

$$\mathbb E\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_2^2\le(1+\varepsilon)^2\sigma_r^2+4e^{-8(q-1)\sqrt{\varepsilon/(2+\varepsilon)}}\,\frac{r}{\ell-r-1}\,\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2.$$

No gap between singular values is assumed.
:::
