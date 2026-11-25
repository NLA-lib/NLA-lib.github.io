---
kind: statement
id: randomized-kaczmarz-76e7063b
uid: 76e7063b-9c06-5517-9953-ba9b8e5adf49
---

::: definition name="Randomized Kaczmarz"
For a real linear system, choose row $i$ independently with probability proportional to its squared norm. Project the current iterate onto $(\mathbf{A}\mathbf{x})_i=b_i$. If $\mathbf{a}_i$ is the transpose of row $i$, the update is $\mathbf{x}\leftarrow\mathbf{x}+\frac{b_i-(\mathbf{A}\mathbf{x})_i}{\|\mathbf{a}_i\|_2^2}\mathbf{a}_i$. A zero row leaves the iterate unchanged. Consistent, inconsistent, and rank-deficient systems have different guarantees.
:::
