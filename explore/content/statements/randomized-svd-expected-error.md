---
kind: statement
id: randomized-svd-expected-error
uid: 77274ec4-3d45-51a1-9390-7258d66c9efd
---

::: theorem result:randomized-svd-expected-error name="Expected Frobenius error"
For a real matrix $\mathbf{A}$, a standard Gaussian test matrix $\mathbf\Omega\in\mathbb R^{n\times\ell}$, and $k+2\le\ell$,

$$\mathbb E\|\mathbf{A}-\mathbf{P}_{\mathbf{A}\mathbf\Omega}\mathbf{A}\|_{\mathrm F}^2\le\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm F}^2.$$

Here $[\mathbf{A}]_k$ is a best rank-at-most-$k$ approximation. Increasing the sketch width above $k$ reduces the multiplicative excess over the optimal squared error.
:::
