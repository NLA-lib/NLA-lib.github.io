---
kind: statement
id: nystr-m-subspace-iteration-a2eae5c1
uid: a2eae5c1-9838-5481-bd1e-23c8c937297c
---

::: definition name="Nyström subspace iteration"
For Hermitian positive-semidefinite $\mathbf{A}$, replace the test matrix in the [Nyström approximation](/explore/statements/254f7f6f-1199-596d-9347-4d32f1eab873/) by $\mathbf{A}^p\boldsymbol{\Omega}$, with $p\ge0$:

$$\mathsf{nyssi}(\mathbf{A},\boldsymbol{\Omega},p)=\mathsf{nystrom}(\mathbf{A},\mathbf{A}^p\boldsymbol{\Omega}).$$

The powers emphasize dominant spectral directions. Only the last power is kept; the [block Krylov variant](/explore/statements/8647f4e3-cefb-5ae0-9fac-51da15589631/) keeps all of them. The choice of stable intermediate bases belongs to a concrete implementation.
:::
