---
kind: statement
id: gmres-optimality
uid: ab283d6b-fe5a-5ca9-bae6-317a3a172f42
---

::: theorem result:gmres-optimality name="Minimum residual"
For any square $\mathbf{A}$, right-hand side $\mathbf{b}$, starting point $\mathbf{x}_0$, and $k\ge0$, the mathematical [GMRES iterate](/explore/statements/7d1681b7-7670-532a-98d3-4e7886e4adcc/) satisfies

$$\|\mathbf{b}-\mathbf{A}\mathbf{x}_k\|_2\le\|\mathbf{b}-\mathbf{A}\mathbf{y}\|_2\quad\text{for every }\mathbf{y}\in\mathbf{x}_0+\mathcal K_k(\mathbf{A},\mathbf{r}_0),$$

where $\mathbf{r}_0=\mathbf{b}-\mathbf{A}\mathbf{x}_0$. No positive-definiteness assumption is required for this optimality statement.
:::
