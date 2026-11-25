---
kind: statement
id: nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rbki-sq-le-of-haslaw-gaussianmatrix
uid: dcf428cb-b48d-5638-ac05-ad9f844a1630
---

::: theorem decl:NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rbki_sq_le_of_hasLaw_gaussianMatrix name="Sufficient depth without a gap" id=gapless-depth
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for every real matrix $\mathbf{A}$ with $n$ columns, every target rank $r$ with $r+2\le\ell$, every $0<\varepsilon\le\varepsilon_0$, and every depth

$$q\ge\frac{C\log(n/\varepsilon)}{\sqrt{\varepsilon}},$$

the truncated output satisfies

$$\mathbb E\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_2^2\le(1+\varepsilon)\,\sigma_r^2.$$

The statement asserts the existence of the constants. With a positive gap $\gamma$, the same result group as the gapped bounds contains the corresponding forms with $q\ge C\log(n/\varepsilon)/\sqrt{\gamma}$, in the spectral and Frobenius norms; they are in the Library.
:::
