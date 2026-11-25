---
kind: statement
id: rbki-block-monotonicity
uid: 0bd6d1ef-ab85-5de8-85b7-6872fc39dae0
---

::: theorem result:rbki-block-monotonicity name="A block with a larger range does at least as well" id=block-monotonicity
Let $\mathbf\Omega$ and $\mathbf\Omega'$ be start blocks with $\operatorname{range}(\mathbf\Omega')\subseteq\operatorname{range}(\mathbf\Omega)$; for example $\mathbf\Omega'$ consists of some columns of $\mathbf\Omega$. Then for every number of blocks $q$ and every index $i$,

$$\sigma_i\bigl(\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)\bigr)\le\sigma_i\bigl(\mathbf{A}-\mathsf{rbki}(\mathbf{A},\mathbf\Omega',q)\bigr).$$

The comparison is for the untruncated approximation at the same depth $q$.
:::
