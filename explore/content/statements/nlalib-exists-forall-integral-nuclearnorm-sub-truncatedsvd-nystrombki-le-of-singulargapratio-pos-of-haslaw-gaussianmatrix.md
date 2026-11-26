---
kind: statement
id: nlalib-exists-forall-integral-nuclearnorm-sub-truncatedsvd-nystrombki-le-of-singulargapratio-pos-of-haslaw-gaussianmatrix
uid: 84d02c77-a2fc-5e91-9252-6a5c17632cf4
---

::: theorem decl:NLAlib.exists_forall_integral_nuclearNorm_sub_truncatedSVD_nystromBKI_le_of_singularGapRatio_pos_of_hasLaw_gaussianMatrix name="Sufficient depth with a gap" id=gapped-depth
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for $r=h+1\le t$ with $t+2\le\ell$, a positive gap $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$, every $0<\varepsilon\le\varepsilon_0$, and every depth

$$q\ge\frac{C\log(n/\varepsilon)}{\sqrt{\gamma}},$$

the truncated output satisfies

$$\mathbb{E}\|\mathbf{A}-[\mathsf{nysbki}(\mathbf{A},\mathbf{X},q)]_r\|_*\le(1+\varepsilon)\,\|\mathbf{A}-[\mathbf{A}]_r\|_*.$$

The statement asserts the existence of the constants.
:::
