---
kind: statement
id: cg-optimality
uid: de598675-e038-5a75-a6b5-f471cab1156a
---

::: theorem result:cg-optimality name="Energy optimality"
The mathematical CG iterate minimizes the energy error over the initial guess plus its [Krylov space](/explore/statements/615008ca-f5db-5cff-ab6b-b07f178cbd05/):

$$\mathbf{x}_k\in\operatorname*{arg\,min}_{\mathbf{y}\in\mathbf{x}_0+\mathcal K_k(\mathbf{A},\mathbf{r}_0)}\|\mathbf{x}_\star-\mathbf{y}\|_\mathbf{A}^2.$$

Here $\mathcal K_k(\mathbf{A},\mathbf{r}_0)=\operatorname{span}\{\mathbf{r}_0,\mathbf{A}\mathbf{r}_0,\ldots,\mathbf{A}^{k-1}\mathbf{r}_0\}$. The energy error cannot increase as the search space grows.
:::
