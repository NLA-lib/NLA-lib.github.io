---
kind: statement
id: nlalib-arnoldimatrix-1ebd9712
uid: 1ebd9712-579d-596a-966f-9119a353806b
---

::: definition decl:NLAlib.arnoldiMatrix name="Arnoldi process"
For a square matrix $\mathbf{A}$ and starting vector $\mathbf{b}$, construct a graded orthonormal basis $\mathbf{Q}_k$ of $\mathcal K_k(\mathbf{A},\mathbf{b})$. Orthogonalize $\mathbf{A}\mathbf{q}_j$ against the current basis to obtain the next column. The compression $\mathbf{H}_k=\mathbf{Q}_k^{\mathsf{H}}\mathbf{A}\mathbf{Q}_k$ is upper Hessenberg. A zero residual signals that the Krylov space has stopped growing; no further nonzero basis column is available.
:::
