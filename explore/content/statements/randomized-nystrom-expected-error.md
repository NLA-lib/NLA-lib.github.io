---
kind: statement
id: randomized-nystrom-expected-error
uid: f999f45d-a5f9-55fb-b592-dae1c50c70ab
---

::: theorem result:randomized-nystrom-expected-error name="Expected nuclear-norm error"
For real positive-semidefinite $\mathbf{A}$, standard Gaussian $\boldsymbol{\Omega}\in\mathbb R^{n\times\ell}$, and $k+2\le\ell$,

$$\mathbb E\|\mathbf{A}-\mathsf{nystrom}(\mathbf{A},\boldsymbol{\Omega})\|_*\le\left(1+\frac{k}{\ell-k-1}\right)\|\mathbf{A}-[\mathbf{A}]_k\|_*.$$

The residual is positive semidefinite, so its nuclear norm is also its trace. The bound compares the expected residual trace with the optimal rank-$k$ tail.
:::
