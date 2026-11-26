---
kind: statement
id: bcw-frobenius-error
uid: affc75db-b874-4278-af6e-0e752cd51a1d
---

::: theorem result:rbki-sum-frobenius-error name="Cube-root Frobenius error in expectation"
Let $\mathbf{A}\in\mathbb{R}^{m\times n}$, $k\ge1$ and $0<\varepsilon\le1$. Use Gaussian blocks with $2k+1$ and $2(k+j)+1$ columns, where

$$j+1\ge\frac{6k}{\varepsilon^{1/3}},\qquad q_1\ge1+\frac{\log(12k/\varepsilon)}{2\sqrt{2}\,\varepsilon^{1/3}},\qquad q_2\ge1+\frac{\log(12/\varepsilon)}{3}.$$

For $\mathbf{B}=[\mathsf{rbkiSum}(\mathbf{A},\mathbf{X}_1,\mathbf{X}_2,q_1,q_2)]_k$,

$$\mathbb{E}\|\mathbf{A}-\mathbf{B}\|_{\mathrm{F}}^2\le(1+\varepsilon)\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm{F}}^2.$$

Each block has independent standard normal entries; mutual independence of the blocks is not required. Zero optimal residual is included.
:::
