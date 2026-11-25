---
kind: statement
id: nlalib-isblockgolubkahan-4dfc5d02
uid: 4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58
---

::: definition decl:NLAlib.IsBlockGolubKahan name="Block Golub–Kahan process"
Write $\operatorname{extend}(\mathbf{Q},\mathbf{W})$ for any exact extension of $\mathbf{Q}$ by $\mathbf{W}$. All blocks have width $\ell$ and are stored side by side.

1. $\mathbf{V}_0,\ \mathbf{R}_0=\operatorname{extend}(\emptyset,\mathbf\Omega)$.
2. For $j=0,\ldots,q-1$:
   1. $\mathbf{U}_j=\operatorname{extend}(\mathbf{U}_{<j},\ \mathbf{A}\mathbf{V}_j)$, with coefficients stored in block column $j$ of $\mathbf{R}$;
   2. $\mathbf{V}_{j+1}=\operatorname{extend}(\mathbf{V}_{\le j},\ \mathbf{A}^{\mathsf{H}}\mathbf{U}_j)$, with coefficients stored in block column $j$ of $\mathbf{S}$.

The output is $\mathbf{U}\in\Bbbk^{m\times q\ell}$, $\mathbf{V}\in\Bbbk^{n\times(q+1)\ell}$, $\mathbf{R}_0\in\Bbbk^{\ell\times \ell}$, $\mathbf{R}\in\Bbbk^{q\ell\times q\ell}$, and $\mathbf{S}\in\Bbbk^{(q+1)\ell\times q\ell}$; the rows of each coefficient block column below the newly extended block are zero. Every block is extended against all earlier blocks of its side. Because an extension is a relation, the process is a relation between the input $(\mathbf{A},\mathbf\Omega,q)$ and the stored matrices $(\mathbf{U},\mathbf{V},\mathbf{R}_0,\mathbf{R},\mathbf{S})$, over real or complex scalars. An exact run is any output related to the input; the statements below hold for every exact run.
:::
