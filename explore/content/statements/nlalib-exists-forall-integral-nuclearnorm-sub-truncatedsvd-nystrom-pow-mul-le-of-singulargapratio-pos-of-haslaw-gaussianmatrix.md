---
kind: statement
id: nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrom-pow-mul-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix
uid: e9cd7afc-bec4-59b6-b5d9-8b006e4b1d5b
---

::: theorem decl:NLAlib.exists_forall_integral_nuclearNorm_sub_truncatedSVD_nystrom_pow_mul_le_of_singularGapRatio_pos_of_hasLaw_gaussianMatrix name="Sufficient number of power steps with a gap" id=gapped-steps
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for $r=h+1\le t$ with $t+2\le\ell$, a positive gap $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, every $0<\varepsilon\le\varepsilon_0$, and every number of power steps

$$p\ge\frac{C\log(n/\varepsilon)}{\gamma},$$

the truncated output satisfies

$$\mathbb E\|\mathbf{A}-[\mathsf{nyssi}(\mathbf{A},\mathbf{X},p)]_r\|_*\le(1+\varepsilon)\,\|\mathbf{A}-[\mathbf{A}]_r\|_*.$$

The statement asserts the existence of the constants.
:::
