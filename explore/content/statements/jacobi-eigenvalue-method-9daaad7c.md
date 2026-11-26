---
kind: statement
id: jacobi-eigenvalue-method-9daaad7c
uid: 9daaad7c-093e-59a8-a0a5-b86b31c81bc3
---

::: definition name="Jacobi eigenvalue method"
For a [Hermitian](/explore/statements/49f5c3f6-f926-5bc6-b401-16993ec1e357/) matrix $\mathbf{A}_j$, choose an off-diagonal entry and a unitary plane rotation $\mathbf{J}_j$ that diagonalizes the associated two-by-two principal block. Set $\mathbf{A}_{j+1}=\mathbf{J}_j^{\mathsf{H}}\mathbf{A}_j\mathbf{J}_j$ and accumulate the rotations into an eigenvector basis. Cyclic and magnitude-based pivot schedules are concrete variants. This is distinct from Jacobi iteration for linear systems.
:::
