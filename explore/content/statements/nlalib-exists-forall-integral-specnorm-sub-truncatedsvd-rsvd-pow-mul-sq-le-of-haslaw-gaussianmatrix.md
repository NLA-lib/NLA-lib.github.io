---
kind: statement
id: nlalib-exists-forall-integral-specnorm-sub-truncatedsvd-rsvd-pow-mul-sq-le-of-haslaw-gaussianmatrix
uid: 0ed7fc6a-e23a-5cc1-a1d8-2055f3edf2a8
---

::: theorem decl:NLAlib.exists_forall_integral_specNorm_sub_truncatedSVD_rsvd_pow_mul_sq_le_of_hasLaw_gaussianMatrix name="Sufficient number of power steps without a gap" id=gapless-steps
There are absolute constants $C>0$ and $\varepsilon_0>0$ such that, for every real matrix $\mathbf{A}$ with $n$ columns, every target rank $r$ with $r+2\le\ell$, every $0<\varepsilon\le\varepsilon_0$, and every number of power steps

$$p\ge\frac{C\log(n/\varepsilon)}{\varepsilon},$$

the truncated output satisfies

$$\mathbb{E}\|\mathbf{A}-[\mathsf{rsi}(\mathbf{A},\mathbf{X},p)]_r\|_2^2\le(1+\varepsilon)\,\sigma_r^2.$$

The statement asserts the existence of the constants. With a positive gap $\gamma$, the same result group as the gapped bounds contains the corresponding forms with $p\ge C\log(n/\varepsilon)/\gamma$, in the spectral and Frobenius norms; they are in the Library.
:::
