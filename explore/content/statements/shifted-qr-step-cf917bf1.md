---
kind: statement
id: shifted-qr-step-cf917bf1
uid: cf917bf1-5d3f-5f8e-8e46-bf4041fd5e43
---

::: definition name="Shifted QR step"
Choose a shift $\mu_j$ and factor $\mathbf{A}_j-\mu_j\mathbf{I}=\mathbf{Q}_j\mathbf{R}_j$. Set $\mathbf{A}_{j+1}=\mathbf{R}_j\mathbf{Q}_j+\mu_j\mathbf{I}=\mathbf{Q}_j^{\mathsf{H}}\mathbf{A}_j\mathbf{Q}_j$. Thus each exact step preserves eigenvalues. Shift selection, deflation tests, and explicit or implicit execution belong to concrete variants. The target for a general matrix is Schur form, rather than necessarily a diagonal matrix.
:::
