---
kind: statement
id: nlalib-isblockgolubkahan-range-blockprefix-right
uid: c52e956e-6658-55db-a3ff-01104cb2ade8
---

::: theorem decl:NLAlib.IsBlockGolubKahan.range_blockPrefix_right name="The right basis spans the block Krylov spaces" id=krylov-range
For an exact run and every $j\le q$, the first $j+1$ blocks of $\mathbf{V}$ span

$$\mathcal K_{j+1}(\mathbf{A}^{\mathsf{H}}\mathbf{A},\mathbf\Omega)=\operatorname{range}[\mathbf\Omega,\ \mathbf{A}^{\mathsf{H}}\mathbf{A}\mathbf\Omega,\ldots,(\mathbf{A}^{\mathsf{H}}\mathbf{A})^{j}\mathbf\Omega].$$

Zero columns are included in the stored blocks and contribute nothing to the range. The same result group, listed under Further results, states that the first $j$ blocks of $\mathbf{U}$ span $\mathbf{A}\,\mathcal K_j(\mathbf{A}^{\mathsf{H}}\mathbf{A},\mathbf\Omega)$ and that $\mathbf{U}\mathbf{U}^{\mathsf{H}}$ is the orthogonal projector onto the range of $\mathbf{A}[\mathbf\Omega,\ldots,(\mathbf{A}^{\mathsf{H}}\mathbf{A})^{q-1}\mathbf\Omega]$.
:::
