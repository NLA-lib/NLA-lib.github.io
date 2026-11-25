---
kind: statement
id: nlalib-isblockgolubkahanerr-593daa98
uid: 593daa98-8a52-5a89-a792-f46844fd76d6
---

::: definition decl:NLAlib.IsBlockGolubKahanErr name="Rounded run of the block Golub–Kahan process"
A rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$ and product parameter $\varepsilon_{\mathrm{mv}}$ has the same stored shape as an exact run. Block $0$ of $\mathbf{V}$ is a rounded extension of the empty basis by $\mathbf\Omega$. For each $j<q$ there are computed products $\mathbf{P}\approx\mathbf{A}\mathbf{V}_j$ and $\mathbf{P}'\approx\mathbf{A}^{\mathsf{T}}\mathbf{U}_j$ whose columns satisfy

$$\|(\mathbf{P}-\mathbf{A}\mathbf{V}_j)\mathbf{e}_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf{A}\|_2\|\mathbf{V}_j\mathbf{e}_c\|,\qquad\|(\mathbf{P}'-\mathbf{A}^{\mathsf{T}}\mathbf{U}_j)\mathbf{e}_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf{A}\|_2\|\mathbf{U}_j\mathbf{e}_c\|,$$

such that $\mathbf{U}_j$ is a rounded extension of $\mathbf{U}_{<j}$ by $\mathbf{P}$ and $\mathbf{V}_{j+1}$ is a rounded extension of $\mathbf{V}_{\le j}$ by $\mathbf{P}'$, with coefficients stored as in the exact process.
:::
