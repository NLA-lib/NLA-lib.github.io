---
kind: statement
id: lanczos-process-d9e8ae48
uid: d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239
---

::: definition name="Lanczos process"
For a Hermitian matrix $\mathbf{A}$ and starting vector $\mathbf{b}$, build a graded orthonormal basis $\mathbf{Q}_k$ of $\mathcal K_k(\mathbf{A},\mathbf{b})$. The compression $\mathbf{T}_k=\mathbf{Q}_k^{\mathsf{H}}\mathbf{A}\mathbf{Q}_k$ is Hermitian tridiagonal. In exact arithmetic, each new basis vector can be generated with a three-term recurrence. Breakdown means the next Krylov direction is zero; the generated space is then invariant. Reorthogonalization changes the concrete recurrence and its rounded behavior.
:::
