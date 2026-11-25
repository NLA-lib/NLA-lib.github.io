---
kind: statement
id: nlalib-measurereal-specnorm-sub-truncatedsvd-rbki-sq-gt-le-of-haslaw-gaussianmatrix
uid: 830039af-0d41-5fa5-886e-01b1c11815c0
---

::: theorem decl:NLAlib.measureReal_specNorm_sub_truncatedSVD_rbki_sq_gt_le_of_hasLaw_gaussianMatrix name="Any block size with a gap" id=any-block-gapped
Let $\mathbf{X}$ be an $n\times\ell$ matrix with independent standard normal entries, $\ell\ge1$. With $r=h+1\le t\le q$, $\delta>0$, $\Delta>0$ satisfying $\sigma_{i+1}^2\le(1-\Delta)\sigma_i^2$ whenever $i+1<t$, and $\gamma=(\sigma_h-\sigma_t)/(\sigma_h+\sigma_t)$,

$$\mathbb P\Bigl[\|\mathbf{A}-[\mathsf{rbki}(\mathbf{A},\mathbf{X},q)]_r\|_2^2>\sigma_r^2+32\,e^{-8(q-t)\sqrt\gamma}\,\Delta^{-2(t-1)}\,\frac{t^3}{\delta^3}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2\Bigr]\le\delta.$$

The right-hand side does not depend on $\ell$. The truncated error is not monotone in the start block, so this is not obtained by comparing the outputs of two blocks.
:::
