---
kind: statement
id: nlalib-integral-specnorm-sub-rsvd-aeval-sq-le-of-haslaw-gaussianmatrix
uid: 8f2f113d-fe93-5cfc-8e86-00d35dd428ff
---

::: theorem decl:NLAlib.integral_specNorm_sub_rsvd_aeval_sq_le_of_hasLaw_gaussianMatrix name="Expected spectral error for a polynomial filter" id=expected-spectral
Let $\mathbf{A}$ be a real matrix with $n$ columns and singular values $\sigma_0\ge\sigma_1\ge\cdots$, let $\mathbf{X}$ be an $n\times\ell$ matrix with independent standard normal entries, and let $r\le t$ with $t+2\le\ell$. Let $f$ be a real polynomial and $c>0$, $a$ real numbers with

$$|f(\sigma_i^2)|\ge c\quad\text{for } i<r,\qquad|f(\lambda)|\le a\quad\text{for } \lambda\in[0,\sigma_t^2].$$

Then

$$\mathbb{E}\bigl\|\mathbf{A}-\mathsf{rsvd}\bigl(\mathbf{A},f(\mathbf{A}^{\mathsf{H}}\mathbf{A})\mathbf{X}\bigr)\bigr\|_2^2\le\sigma_r^2+\Bigl(\frac{a}{c}\Bigr)^2\frac{t}{\ell-t-1}\,\|\mathbf{A}-[\mathbf{A}]_t\|_{\mathrm F}^2.$$

The bound is small when the filter is large on the head singular values and small on the tail interval. The deterministic bound for a general spectral filter, the Frobenius form, and the form in every unitarily invariant norm are listed below.
:::
