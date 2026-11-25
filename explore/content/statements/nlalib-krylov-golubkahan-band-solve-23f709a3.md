---
kind: statement
id: nlalib-krylov-golubkahan-band-solve-23f709a3
uid: 23f709a3-92ab-5cef-ab62-2b33870d9605
---

::: definition decl:NLAlib.Krylov.GolubKahan.Band.solve name="Driver with an abstract extension operation" id=algorithm
The dimensions are $[m,n,\ell,q]$. The call $\operatorname{extend}(\mathbf{Q},\mathbf{W})$ extends the stored basis $\mathbf{Q}$ by the block $\mathbf{W}$ and returns the new block and its coefficients.

1. Draw an $n\times \ell$ start block $\mathbf{W}$ from the tape stream into scratch.
2. $\mathbf{V}_0,\ \mathbf{G}=\operatorname{extend}(\emptyset,\mathbf{W})$.
3. For $j=0,\ldots,q-1$:
   1. $\mathbf{W}=\mathbf{A}\mathbf{V}_j$, one product per column;
   2. $\mathbf{U}_j$ and block column $j$ of $\mathbf{R}$ $=\operatorname{extend}(\mathbf{U}_{<j},\mathbf{W})$;
   3. $\mathbf{W}=\mathbf{A}^{\mathsf{T}}\mathbf{U}_j$, one product per column;
   4. $\mathbf{V}_{j+1}$ and block column $j$ of $\mathbf{S}$ $=\operatorname{extend}(\mathbf{V}_{\le j},\mathbf{W})$.
4. Return $\mathbf{U},\mathbf{V},\mathbf{G},\mathbf{R},\mathbf{S}$ and release the scratch block.

Storage is column-major, one word per entry: $\mathbf{U}$ has $q\ell m$ words, $\mathbf{V}$ has $(q+1)\ell n$ words, $\mathbf{G}$ has $\ell^2$ words, and the coefficients $\mathbf{R}$ and $\mathbf{S}$ are packed by block column. The scratch block has $\max(m,n)\,\ell$ words.
:::
