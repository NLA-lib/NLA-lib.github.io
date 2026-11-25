---
kind: statement
id: nystr-m-subspace-iteration-a2eae5c1
uid: a2eae5c1-9838-5481-bd1e-23c8c937297c
---

::: definition name="Nyström subspace iteration"
For Hermitian positive-semidefinite $\mathbf{A}$, replace the test matrix in the Nyström approximation by $\mathbf{A}^p\mathbf\Omega$, with $p\ge0$:

$$\mathsf{nyssi}(\mathbf{A},\mathbf\Omega,p)=\mathsf{nystrom}(\mathbf{A},\mathbf{A}^p\mathbf\Omega).$$

The powers emphasize dominant spectral directions. Only the last power is kept; the block Krylov variant keeps all of them. The choice of stable intermediate bases belongs to a concrete implementation.
:::
