---
kind: statement
id: etgn
uid: d059f2c5-9a30-5050-9e0c-bfddc9d221d7
---

::: theorem result:etgn name="Gaussian relative-error guarantee"
For a real input $\mathbf{A}$, independent standard Gaussian sketches of widths $\ell,p$, and $0<\varepsilon\le1$, suppose

$$\ell\ge\frac{1600k}{\varepsilon^2},\qquad p\ge k+1+\frac{(2+\varepsilon)k}{\varepsilon}.$$

Then the mathematical [early-truncated output](/explore/statements/cdd691bb-6aef-5d59-b7e9-615785a98d27/) satisfies

$$\mathbb{E}\|\mathbf{A}-\widehat{\mathbf{A}}\|_{\mathrm F}^2\le(1+\varepsilon)\|\mathbf{A}-[\mathbf{A}]_k\|_{\mathrm F}^2.$$

Thus the expected squared error is within a factor $1+\varepsilon$ of the optimal rank-$k$ squared Frobenius error. The two sketch sizes have different accuracy dependence.
:::
