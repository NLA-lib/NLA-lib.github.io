---
kind: statement
id: matrix-possemidef-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-singulargapratio-of-haslaw-gaussianmatrix
uid: e59d814f-e0b1-56c7-af02-203f32b258da
---

::: theorem decl:Matrix.PosSemidef.integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_singularGapRatio_of_hasLaw_gaussianMatrix name="Expected nuclear-norm error with a gap" id=gapped-nuclear
Let $q\ge1$, let $r=h+1$ be the number of head eigenvalues, and let $t\ge r$ be a tail index with $t+2\le\ell$. With $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, and $\gamma=0$ when both vanish,

$$\mathbb E\|\mathbf{A}-[\mathsf{nysbki}(\mathbf{A},\mathbf{X},q)]_r\|_*\le\|\mathbf{A}-[\mathbf{A}]_r\|_*+4e^{-4\sqrt2\,(q-1)\sqrt{\gamma}}\,\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_*.$$
:::
