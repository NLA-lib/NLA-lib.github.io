---
kind: statement
id: generalized-nystrom-expected-error
uid: 07a22a07-cf1a-5eab-9c15-e691321845a2
---

::: theorem result:generalized-nystrom-expected-error name="Expected Frobenius error"
Let $\mathbf{A}\in\mathbb R^{m\times n}$, with independent standard Gaussian test matrices $\mathbf\Omega\in\mathbb R^{n\times\ell}$ and $\mathbf\Psi\in\mathbb R^{m\times p}$. If $k+2\le\ell$ and $\ell+2\le p$, then

$$\mathbb E\|\mathbf{A}-\mathsf{gn}(\mathbf{A},\mathbf\Omega,\mathbf\Psi)\|_{\mathrm F}^2\le\left(1+\frac{\ell}{p-\ell-1}\right)\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm F}^2.$$

The two factors measure the excess from the range sketch and the second sketch. Here $[\mathbf{A}]_k$ denotes a best rank-at-most-$k$ approximation.
:::
