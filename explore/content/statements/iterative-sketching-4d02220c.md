---
kind: statement
id: iterative-sketching-4d02220c
uid: 4d02220c-4aa0-5cd0-8df1-afff8a1279ba
---

::: definition name="Iterative sketching"
Fix a sketch $\mathbf{S}$, form $\mathbf{G}=(\mathbf{S}\mathbf{A})^{\mathsf{H}}\mathbf{S}\mathbf{A}$, and update $\mathbf{x}_{j+1}=\mathbf{x}_j+\omega\mathbf{G}^\dagger\mathbf{A}^{\mathsf{H}}(\mathbf{b}-\mathbf{A}\mathbf{x}_j)$. The same sketch is reused in every step. A positive step alone does not ensure convergence; the embedding bounds and damping parameter must give a contraction.
:::
