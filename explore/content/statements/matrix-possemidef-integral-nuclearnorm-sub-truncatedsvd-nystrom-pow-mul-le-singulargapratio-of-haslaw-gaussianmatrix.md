---
kind: statement
id: matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-singulargapratio-of-haslaw-gaussianmatrix
uid: a5e449d4-fd34-5212-96fa-75ce7fa2feaf
---

::: theorem decl:Matrix.PosSemidef.integral_nuclearNorm_sub_truncatedSVD_nystrom_pow_mul_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected nuclear-norm error with a gap" id=gapped-nuclear
Let $r=h+1$ be the number of head eigenvalues and let $t\ge r$ be a tail index with $t+2\le\ell$. With $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, and $\gamma=0$ when both vanish,

$$\mathbb E\|\mathbf{A}-[\mathsf{nyssi}(\mathbf{A},\mathbf{X},p)]_r\|_*\le\|\mathbf{A}-[\mathbf{A}]_r\|_*+e^{-4p\gamma}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_*.$$
:::
