---
kind: statement
id: entry-e835324a-a005-5849-bdab-fe6e1edd8e9c
uid: e835324a-a005-5849-bdab-fe6e1edd8e9c
---
::: theorem result:randomized-svd-tail name="Randomized SVD: tail bounds"
For
$\mathbf{A} \in \mathbb{R}^{m \times n}$, a test matrix $\mathbf{X} \in \mathbb{R}^{n \times \ell}$
with independent standard Gaussian entries (`HasLaw X (gaussianMatrix n l) μ`), a target rank $k$
with $d = \ell - k + 1$ (`hd : k + d = Fintype.card l + 1`),
$s \ge 0$ and $t > 0$, <!-- value gaussianPinvFrobTail k d t -->
$$\mathbb{P}\Bigl[\|\mathbf{A} - \mathsf{rsvd}(\mathbf{A}, \mathbf{X})\|_{\mathsf{F}}^2 >
\|\mathbf{A} - \llbracket\mathbf{A}\rrbracket_k\|_{\mathsf{F}}^2 + \frac{tk}{d}\bigl(
\|\mathbf{A} - \llbracket\mathbf{A}\rrbracket_k\|_{\mathsf{F}} +
s\,\sigma_k(\mathbf{A})\bigr)^2\Bigr]
\le e^{-s^2/2} + \frac{2\sqrt{k}\,(d/(2t))^{d/2}}{\Gamma(d/2 + 1)}\,,$$
the second failure term being `gaussianPinvFrobTail k d t`.

Note: The cited theorem is stated at $p = 2$, with the noise term
$(utk/d)\|\mathbf{E}\|_{\mathsf{F}}^2$ and failure probability
$e^{-(u-2)/4} + \sqrt{\pi k}\,(t/e)^{-d/2}$; these follow from this bound at $s = \sqrt{u} - 1$.
:::
