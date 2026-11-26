---
kind: statement
id: bcw-definition
uid: 39a7e927-15c2-41c3-9d83-4b3358e74d95
---

::: definition decl:NLAlib.rbkiSum name="Two-space block Krylov projection and rank-k outputs"
For start blocks $\boldsymbol{\Omega}_1,\boldsymbol{\Omega}_2$ and depths $q_1,q_2$, let

$$\mathbf{Y}=\begin{bmatrix}\mathbf{K}_{q_1}(\mathbf{A}^{\mathsf{H}}\mathbf{A},\boldsymbol{\Omega}_1)&\mathbf{K}_{q_2}(\mathbf{A}^{\mathsf{H}}\mathbf{A},\boldsymbol{\Omega}_2)\end{bmatrix},\qquad \mathbf{C}=\mathsf{rsvd}(\mathbf{A},\mathbf{Y})=\mathbf{P}_{\mathbf{A}\mathbf{Y}}\mathbf{A}.$$

Here $\mathbf{K}_q(\mathbf{H},\boldsymbol{\Omega})=[\boldsymbol{\Omega},\mathbf{H}\boldsymbol{\Omega},\ldots,\mathbf{H}^{q-1}\boldsymbol{\Omega}]$ has $q$ blocks. The source identifier `rbkiSum` denotes $\mathbf{C}$. The one-sided rank-$k$ output is $\mathbf{B}=[\mathbf{C}]_k$. The two-sided output is $\mathbf{A}\mathbf{P}_{\mathbf{B}^{\mathsf{H}}}$, using the orthogonal projector onto the row space of $\mathbf{B}$.
:::
