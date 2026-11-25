---
kind: statement
id: nlalib-integral-frobnorm-sub-truncatedsvd-generalizednystrom-sq-le-one-add-of-haslaw-gaussianmatrix-of-truncatedgeneralizednystromrangedim-le
uid: 1266e5b2-8402-52e9-b859-115a81dc709f
---

::: theorem decl:NLAlib.integral_frobNorm_sub_truncatedSVD_generalizedNystrom_sq_le_one_add_of_hasLaw_gaussianMatrix_of_truncatedGeneralizedNystromRangeDim_le name="Expected relative error" id=expected-error
For a real input $\mathbf{A}$, independent standard Gaussian sketches of widths $\ell,p$, and $0<\varepsilon\le1$, suppose

$$\ell\ge\frac{200k}{\varepsilon},\qquad p\ge14\ell.$$

Then

$$\mathbb E\|\mathbf{A}-[\mathsf{gn}(\mathbf{A},\mathbf\Omega,\mathbf\Psi)]_k\|_{\mathrm F}^2\le(1+\varepsilon)\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm F}^2.$$

Both sketch widths can be chosen of order $k/\varepsilon$. This is a sufficient upper bound on the expected squared approximation error, valid for every real input matrix. The source also retains alternative bounds with different sufficient sketch sizes.
:::
