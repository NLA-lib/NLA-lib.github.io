---
kind: statement
id: preconditioned-minres-c9704060
uid: c9704060-abeb-5a36-9da4-7c1c288ebce6
---

::: definition name="Preconditioned MINRES"
For Hermitian $\mathbf{A}$ and a positive-definite inverse preconditioner $\mathbf{M}$, apply mathematical MINRES to $\mathbf{M}^{1/2}\mathbf{A}\mathbf{M}^{1/2}\mathbf{y}=\mathbf{M}^{1/2}\mathbf{b}$ and recover $\mathbf{x}=\mathbf{M}^{1/2}\mathbf{y}$. The corresponding original residual is measured in the $\mathbf{M}$-norm. The transformed spectrum, rather than the original spectrum alone, enters convergence bounds.
:::
