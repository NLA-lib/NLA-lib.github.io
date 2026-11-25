---
kind: statement
id: nlalib-hessenbergreduction-21c93d07
uid: 21c93d07-2c81-555f-80b2-eff7e5316a67
---

::: definition decl:NLAlib.hessenbergReduction name="Hessenberg reduction"
For a square $\mathbf{A}$, accumulate Householder similarities to obtain a unitary $\mathbf{Q}$ and upper-Hessenberg $\mathbf{H}=\mathbf{Q}^{\mathsf{H}}\mathbf{A}\mathbf{Q}$. The mathematical construction uses $n-2$ similarities; for $n\le2$ it returns $(\mathbf{I},\mathbf{A})$. It changes the representation of the eigenproblem, not its eigenvalues.
:::
