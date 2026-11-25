---
kind: statement
id: three-precision-iterative-refinement
uid: d5c04cd3-1440-51a5-afad-18cf3acb4fa8
---

::: theorem result:three-precision-iterative-refinement name="Forward error of the stored output" id=certificate
Let $\mathbf{A}$ be positive definite of order $n$, $\kappa=\kappa_2(\mathbf{A})$, $(n+1)u_r<1$, and

$$\theta=48(n+1)^2\kappa u_f\le1,\qquad\eta=(1+u)(n+1)\gamma_{n+1}(u_r),\qquad\gamma_m=(1-u_r)^{-m}-1,$$

$$\varphi=(1+u)\bigl(\theta+(1+\theta)\kappa(u+\eta)\bigr)<1,\qquad\xi=(1+u)(1+\theta)\,2\kappa\eta+u.$$

At an admitted size, for every $\mathbf{b}$ and $\mathbf{x}_0$, every interpretation satisfying the model and every tape, the run of the fixed program succeeds within the instruction bound above, and buffer 2 then holds $\hat{\mathbf{x}}$ with, for $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$,

$$\|\mathbf{x}_\star-\hat{\mathbf{x}}\|\le\varphi^k\|\mathbf{x}_\star-\mathbf{x}_0\|+\frac{\xi}{1-\varphi}\|\mathbf{x}_\star\|.$$
:::
