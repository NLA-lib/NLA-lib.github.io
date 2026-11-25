---
kind: statement
id: nlalib-measurereal-specnorm-sub-rbki-sq-gt-le-of-haslaw-gaussianvector
uid: b6e3068d-bde4-5d5c-aafe-f3918ea961e1
---

::: theorem decl:NLAlib.measureReal_specNorm_sub_rbki_sq_gt_le_of_hasLaw_gaussianVector name="Single start vector with a gap: spectral-norm tail bound" id=single-vector-tail
Let $\mathbf{A}$ be a real matrix with $n$ columns and let $\mathbf{x}\in\mathbb R^n$ have independent standard normal entries. Fix a head of $r=h+1$ singular values, a tail index $t\ge r$, a depth $q\ge t$, and $\delta>0$. Suppose there is $\Delta>0$ with

$$\sigma_{i+1}^2\le(1-\Delta)\,\sigma_i^2\qquad\text{whenever } i+1<t,$$

and let $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$. Then

$$\mathbb P\Bigl[\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{x},q)\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The start block is the single column $\mathbf{x}$. The gap hypothesis concerns only $\sigma_0,\ldots,\sigma_{t-1}$: no gap between $\sigma_{t-1}$ and $\sigma_t$ and no positivity of $\sigma_{t-1}$ is assumed. The same result group, listed under Further results, contains the Frobenius-norm form and an expectation restricted to an explicit event.
:::
