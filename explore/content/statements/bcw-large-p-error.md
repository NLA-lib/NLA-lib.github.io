---
kind: statement
id: bcw-large-p-error
uid: 2c700dd8-8cdb-4f06-8f14-c38f62c880b0
---

::: theorem result:rbki-sum-schatten-large-p-error name="Dimension-free large-p error in expectation"
Let $2\le p<\infty$, $k\ge1$, $0<\varepsilon\le1$ and $r=\lceil(p-2)/4\rceil$. Use real Gaussian start blocks with $2k+1$ and $2(k+j)+1$ columns. If

$$j+1\ge\frac{2ek}{\varepsilon^{1/3}},\qquad q_1\ge1+r+\frac{\sqrt{p}\log(14pk/\varepsilon)}{2\varepsilon^{1/3}},\qquad q_2\ge1+r+\frac{\sqrt{p}\log(8pk/\varepsilon)}{2},$$

then, for $\mathbf{B}=[\mathsf{rbkiSum}(\mathbf{A},\mathbf{X}_1,\mathbf{X}_2,q_1,q_2)]_k$,

$$\mathbb{E}\|\mathbf{A}-\mathbf{B}\|_{S_p}^p\le(1+\varepsilon)\operatorname{OPT}_p^p.$$

The blocks need not be mutually independent. The bound includes zero optimal residual and has no matrix-dimension factor, including inside the logarithms.
:::
