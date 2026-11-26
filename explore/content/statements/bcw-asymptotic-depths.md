---
kind: statement
id: bcw-asymptotic-depths
uid: a4b8b810-e947-4596-8b7f-424f26b8dfbd
---

::: theorem decl:NLAlib.exists_forall_integral_schattenNorm_sub_truncatedSVD_rbkiSum_rpow_le_of_hasLaw_gaussianMatrix name="Dimension-free asymptotic depths"
There are absolute constants $C,\varepsilon_0>0$ such that, for $2\le p<\infty$, a real matrix $\mathbf{A}$, $k\ge1$ and $0<\varepsilon\le\varepsilon_0$, real Gaussian blocks of widths $\ell_1\ge2k+1$ and $\ell_2\ge Ck\varepsilon^{-1/3}$ and depths

$$q_1\ge C\!\left(p+\frac{\sqrt{p}\log(pk/\varepsilon)}{\varepsilon^{1/3}}\right),\qquad q_2\ge C\!\left(p+\sqrt{p}\log(pk/\varepsilon)\right)$$

give $\mathbb{E}\|\mathbf{A}-\mathbf{B}\|_{S_p}^p\le(1+\varepsilon)\operatorname{OPT}_p^p$, where $\mathbf{B}$ is the rank-$k$ truncation of the combined-space output. The two Gaussian blocks need not be mutually independent. The constants are independent of $p$ and of the matrix dimensions, and zero optimal residual is included. The proof supplies $C=1000$ and $\varepsilon_0=e^{-1}$.
:::
