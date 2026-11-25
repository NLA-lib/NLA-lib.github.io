---
kind: statement
id: nlalib-linearsystems-refinement-certification-algorithm-checked
uid: 4665c197-4b8f-5074-bbc4-261137cc421b
---

::: theorem decl:NLAlib.LinearSystems.Refinement.Certification.algorithm_checked name="Forward error of the stored output" id=certificate
Let $\mathbf{A}$ be invertible of order $n$, with

$$\varphi=(1+\varepsilon)\bigl(\theta+(1+\theta)\kappa_2(\mathbf{A})(\zeta+\eta)\bigr)<1,\qquad\xi=(1+\varepsilon)(1+\theta)\,2\kappa_2(\mathbf{A})\eta+\varepsilon.$$

For every $\mathbf{b}$ and $\mathbf{x}_0$, every interpretation satisfying the three contracts and every tape, the run of the fixed program from $\mathbf{b}$, $\mathbf{x}_0$ and two blank vectors succeeds within $25k+15$ instructions, and buffer 1 then holds $\hat{\mathbf{x}}$ with, for $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$,

$$\|\mathbf{x}_\star-\hat{\mathbf{x}}\|\le\varphi^k\|\mathbf{x}_\star-\mathbf{x}_0\|+\frac{\xi}{1-\varphi}\|\mathbf{x}_\star\|.$$
:::
