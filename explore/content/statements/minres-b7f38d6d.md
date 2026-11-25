---
kind: statement
id: minres-b7f38d6d
uid: b7f38d6d-61b5-5315-97b5-ad37f607e474
---

::: definition name="MINRES"
For a real symmetric system $\mathbf{A}\mathbf{x}=\mathbf{b}$, choose the iterate that minimizes the Euclidean residual norm over $\mathbf{x}_0+\mathcal K_k(\mathbf{A},\mathbf{r}_0)$, where $\mathbf{r}_0=\mathbf{b}-\mathbf{A}\mathbf{x}_0$. Symmetry permits a Lanczos-based short recurrence. Positive definiteness is not required for this minimization; solvability and termination claims need their own hypotheses.
:::
