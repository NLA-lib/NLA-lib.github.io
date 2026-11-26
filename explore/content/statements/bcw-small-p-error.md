---
kind: statement
id: bcw-small-p-error
uid: a72cc0e1-75e8-408a-827b-dc211b166032
---

::: theorem result:rbki-sum-schatten-error name="Small-p Schatten error in expectation"
For $1\le p\le2$, $k\ge1$ and $0<\varepsilon\le1$, use real Gaussian start blocks with $2k+1$ and $2(k+j)+1$ columns and the thresholds

$$j+1\ge\frac{6k}{\varepsilon^{1/3}},\qquad q_1\ge1+\frac{\log(12k/\varepsilon)}{2\sqrt{2}\,\varepsilon^{1/3}},\qquad q_2\ge1+\frac{\log(12/\varepsilon)}{3}.$$

Writing $\mathbf{B}=[\mathsf{rbkiSum}(\mathbf{A},\mathbf{X}_1,\mathbf{X}_2,q_1,q_2)]_k$, the two-sided output satisfies

$$\mathbb{E}\|\mathbf{A}-\mathbf{A}\mathbf{P}_{\mathbf{B}^{\mathsf{H}}}\|_{S_p}^p\le(1+\varepsilon)\operatorname{OPT}_p^p.$$

The blocks need not be mutually independent, and zero optimal residual is included. For $p<2$ this statement concerns the two-sided output.
:::
