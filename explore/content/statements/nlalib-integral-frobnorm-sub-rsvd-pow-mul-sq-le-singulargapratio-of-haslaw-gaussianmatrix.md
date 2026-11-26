---
kind: statement
id: nlalib-integral-frobnorm-sub-rsvd-pow-mul-sq-le-singulargapratio-of-haslaw-gaussianmatrix
uid: bca995a9-a2a8-5034-b4bb-565f08cbb95b
---

::: theorem decl:NLAlib.integral_frobNorm_sub_rsvd_pow_mul_sq_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected Frobenius error with a gap" id=gapped-frobenius
Let $\mathbf{A}\in\mathbb{R}^{m\times n}$ have [singular values](/explore/statements/581c9098-24f3-55b6-bd36-a47af48b21ff/)
$\sigma_0\ge\sigma_1\ge\cdots$, indexed from zero, and let
$\mathbf{X}\in\mathbb{R}^{n\times\ell}$ have independent standard Gaussian entries.
Let $h,r,t,p\in\mathbb{N}$ satisfy $r=h+1\le t$ and $t+2\le\ell$.
Set $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, taking $\gamma=0$
when both singular values are zero. Write $[\mathbf{B}]_j$ for the
[truncated SVD retaining at most $j$ singular components](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/)
of a matrix $\mathbf{B}$, and $\mathsf{rsi}(\mathbf{A},\mathbf{X},p)$ for
[randomized subspace iteration](/explore/statements/90f9c5f5-2db3-5dde-afe2-c2d2f5bdd092/)
with $p$ power steps and initial sketch $\mathbf{X}$. Then

$$\mathbb{E}\|\mathbf{A}-\mathsf{rsi}(\mathbf{A},\mathbf{X},p)\|_{\mathrm F}^2\le\|\mathbf{A}-[\mathbf{A}]_r\|_{\mathrm F}^2+e^{-8p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2.$$
:::
