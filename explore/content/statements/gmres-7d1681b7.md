---
kind: statement
id: gmres-7d1681b7
uid: 7d1681b7-7670-532a-98d3-4e7886e4adcc
---

::: definition name="GMRES"
For $\mathbf{A}\mathbf{x}=\mathbf{b}$, set $\mathbf{r}_0=\mathbf{b}-\mathbf{A}\mathbf{x}_0$. Choose

$$\mathbf{x}_k\in\operatorname*{arg\,min}_{\mathbf{y}\in\mathbf{x}_0+\mathcal K_k(\mathbf{A},\mathbf{r}_0)}\|\mathbf{b}-\mathbf{A}\mathbf{y}\|_2.$$

[Arnoldi](/explore/statements/1ebd9712-579d-596a-966f-9119a353806b/) reduces this minimization to a small least-squares problem. Restarting changes the sequence of search spaces and is a distinct concrete variant.
:::
