---
kind: statement
id: block-golub-kahan-factored-output
uid: 4acf79f1-542a-5cb1-ad06-82ac78de683b
---

::: theorem result:block-golub-kahan-factored-output name="The factored output is the block Krylov approximation" id=factored-output
Let $m,n,b,q\in\mathbb{N}$, let $\Bbbk$ be $\mathbb{R}$ or $\mathbb{C}$, let $\mathbf{A}\in\Bbbk^{m\times n}$ and $\boldsymbol{\Omega}\in\Bbbk^{n\times b}$, and let $\mathbf{U}\in\Bbbk^{m\times qb}$, $\mathbf{V}\in\Bbbk^{n\times(q+1)b}$, and $\mathbf{S}\in\Bbbk^{(q+1)b\times qb}$ be outputs of an [exact block Golub–Kahan run](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/) for $\mathbf{A}$ from $\boldsymbol{\Omega}$ with $q$ steps. For every such run,

$$\mathbf{U}\mathbf{S}^{\mathsf{H}}\mathbf{V}^{\mathsf{H}}=\mathsf{rbki}(\mathbf{A},\boldsymbol{\Omega},q),$$

where the right-hand side is the [projection of $\mathbf{A}$ onto the range](/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/) of $\mathbf{A}[\boldsymbol{\Omega},\mathbf{A}^{\mathsf{H}}\mathbf{A}\boldsymbol{\Omega},\ldots,(\mathbf{A}^{\mathsf{H}}\mathbf{A})^{q-1}\boldsymbol{\Omega}]$. Here $\mathbf{V}$ has all $q+1$ blocks.

Note: The corresponding identity for the factors assembled from packed coefficient blocks of an exact stored program run is stated for real matrices.
:::
