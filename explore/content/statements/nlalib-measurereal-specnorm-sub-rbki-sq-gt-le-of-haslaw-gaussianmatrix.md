---
kind: statement
id: nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianmatrix
uid: a5d91c5d-df40-55e9-ac3f-92bb1c0dbf85
---

::: theorem decl:NLAlib.measureReal_specNorm_sub_rbki_sq_gt_le_of_hasLaw_gaussianMatrix name="Any block size with a gap: spectral-norm tail bound" id=any-block-tail
Let $\mathbf{A}$ be a real matrix with $n$ columns and let $\mathbf{X}$ be an $n\times\ell$ matrix with independent standard normal entries, $\ell\ge1$. With $r=h+1\le t\le q$, $\delta>0$, $\Delta>0$ satisfying $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<t$, and $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$,

$$\mathbb P\Bigl[\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{X},q)\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The right-hand side is the single-vector bound and does not depend on $\ell$. The Frobenius-norm form is listed under Further results.
:::
