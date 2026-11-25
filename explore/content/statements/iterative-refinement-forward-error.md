---
kind: statement
id: iterative-refinement-forward-error
uid: e1a72f9d-aab8-55c4-b50b-40b1279609fc
---

::: theorem result:iterative-refinement-forward-error name="Forward error of iterative refinement" id=forward-error
Let $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$, $\kappa=\kappa_2(\mathbf{A})$, and

$$\varphi=(1+\varepsilon)\bigl(\theta+(1+\theta)\kappa(\zeta+\eta)\bigr),\qquad\xi=(1+\varepsilon)(1+\theta)\,2\kappa\eta+\varepsilon.$$

If $\varphi<1$, every iterate $j\le k$ of a run satisfies

$$\|\mathbf{x}_\star-\mathbf{x}_j\|\le\varphi^j\|\mathbf{x}_\star-\mathbf{x}_0\|+\frac{\xi}{1-\varphi}\|\mathbf{x}_\star\|.$$
:::
