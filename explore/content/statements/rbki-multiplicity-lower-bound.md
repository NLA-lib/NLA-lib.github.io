---
kind: statement
id: rbki-multiplicity-lower-bound
uid: 2715e07f-95d2-5b31-863a-8adcfb6d65d4
---

::: theorem result:rbki-multiplicity-lower-bound name="A repeated singular value beyond the block size" id=multiplicity-lower-bound
Let $\mathbf{A}$ be a real or complex matrix and $\mathbf\Omega$ any start block with $\ell$ columns; no distribution and no rank condition is assumed. If indices $i,k$ satisfy $\sigma_i(\mathbf{A})=\sigma_{i+\ell+k}(\mathbf{A})$, then for every depth $q$,

$$\sigma_i(\mathbf{A})\le\sigma_k\bigl(\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)\bigr).$$

In particular, for $k=0$: if $\sigma_i=\sigma_{i+\ell}$, then $\sigma_i(\mathbf{A})\le\|\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)\|_2$ for every $q$. When such a $\sigma_i$ exceeds $\sigma_r$, the spectral error stays above the best rank-$r$ error at every depth. This is a statement about the exact projection defining the method.
:::
