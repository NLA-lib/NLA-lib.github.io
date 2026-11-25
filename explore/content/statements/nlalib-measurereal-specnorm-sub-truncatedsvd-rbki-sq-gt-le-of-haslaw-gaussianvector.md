---
kind: statement
id: nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianvector
uid: b89d095b-73c0-59e2-a3f9-173e6d19b29c
---

::: theorem decl:NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianVector name="Single start vector with a gap" id=single-vector-gapped
Let $\mathbf{x}\in\mathbb R^n$ have independent standard normal entries. Fix a head of $r=h+1$ singular values, a tail index $t\ge r$, a depth $q\ge t$, and $\delta>0$. Suppose there is $\Delta>0$ with $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<t$, and let $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$. Then

$$\mathbb P\Bigl[\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{x},q)]_r\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The start block is the single column $\mathbf{x}$. No positivity of $\sigma_{t-1}$ is assumed.
:::
