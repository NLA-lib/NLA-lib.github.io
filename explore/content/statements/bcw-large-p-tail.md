---
kind: statement
id: bcw-large-p-tail
uid: da4acb45-45b9-491c-a313-d000b003ec2b
---

::: theorem result:rbki-sum-schatten-large-p-tail name="Dimension-free large-p tail bound"
Let $2\le p<\infty$, $k\ge1$, $0<\varepsilon\le1$, $\delta>0$ and $r=\lceil(p-2)/4\rceil$. Use real Gaussian start blocks with $2k+1$ and $2(k+j)+1$ columns. If

$$j+1\ge\frac{ek}{\varepsilon^{1/3}},\qquad q_1\ge1+r+\frac{\sqrt{p}\log(20pk/(\varepsilon\delta))}{2\varepsilon^{1/3}},\qquad q_2\ge1+r+\frac{\sqrt{p}\log(12pk/(\varepsilon\delta))}{2},$$

then the rank-$k$ truncation $\mathbf{B}$ of the combined-space output satisfies

$$\mathbb{P}\!\left[\|\mathbf{A}-\mathbf{B}\|_{S_p}^p>(1+\varepsilon)\operatorname{OPT}_p^p\right]\le\delta.$$

Mutual independence of the blocks is not required. Zero optimal residual is included; $\delta\ge1$ is allowed. The failure probability appears only inside the depth logarithms.
:::
