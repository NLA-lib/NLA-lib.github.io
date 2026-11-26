---
kind: statement
id: eckart-young-frobenius
uid: 35e54249-105c-5da3-980b-30e3d93943b4
---

::: theorem result:eckart-young-frobenius name="Optimal rank truncation"
Let $\mathbf{A}$ be a matrix and $k\in\mathbb{N}$. Write $[\mathbf{A}]_k$ for its
[truncated SVD retaining at most $k$ singular components](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/).
For every matrix $\mathbf{B}$ of the same shape as $\mathbf{A}$ with rank at most $k$,

$$\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm F}\le\|\mathbf{A}-\mathbf{B}\|_{\mathrm F}.$$

Thus retaining the [leading singular components](/explore/statements/d5bca832-63a1-5043-ab6e-03b8402a2a55/) gives a best rank-at-most-$k$ approximation in Frobenius norm. A separate result gives the spectral-norm optimum.
:::
