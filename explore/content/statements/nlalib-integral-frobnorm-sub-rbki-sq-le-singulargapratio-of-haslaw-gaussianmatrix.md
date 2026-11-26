---
kind: statement
id: nlalib-integral-frobnorm-sub-rbki-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: c895cc03-43bf-5ab0-831d-8720e5af74b6
---

::: theorem decl:NLAlib.integral_frobNorm_sub_rbki_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Let $\mathbf{A}\in\mathbb{R}^{m\times n}$ have [singular values](/explore/statements/581c9098-24f3-55b6-bd36-a47af48b21ff/) $\sigma_0\ge\sigma_1\ge\cdots$, and let $\mathbf{X}\in\mathbb{R}^{n\times\ell}$ have independent standard Gaussian entries. Let $h,r,t,q\in\mathbb{N}$ satisfy $h+1=r$, $r\le t$, $t+2\le\ell$, and $q\ge1$, and set $\gamma=\dfrac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}$, with $\gamma=0$ if $\sigma_h=\sigma_t=0$. Here $\sigma_i$ is indexed from zero, $[\mathbf{A}]_s$ denotes the [rank-at-most-$s$ truncated singular-value approximation](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/), and $\mathsf{rbki}$ denotes [block Krylov iteration](/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/). Then have singular values $\sigma_0\ge\sigma_1\ge\cdots$, and let $\mathbf{X}\in\mathbb{R}^{n\times\ell}$ have independent standard Gaussian entries. Let $h,r,t,q\in\mathbb{N}$ satisfy $h+1=r$, $r\le t$, $t+2\le\ell$, and $q\ge1$, and set $\gamma=\dfrac{\sigma_h-\sigma_t}{\sigma_h+\sigma_t}$, with $\gamma=0$ if $\sigma_h=\sigma_t=0$. Then

$$\mathbb{E}\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf{X},q)\|_{\mathrm F}^2\le\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2+4e^{-8(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2.$$
:::
