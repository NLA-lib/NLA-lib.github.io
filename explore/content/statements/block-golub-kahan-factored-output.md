---
kind: statement
id: block-golub-kahan-factored-output
uid: 4acf79f1-542a-5cb1-ad06-82ac78de683b
---

::: theorem result:block-golub-kahan-factored-output name="The factored output is the block Krylov approximation" id=factored-output
For an [exact run](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/),

$$\mathbf{U}\mathbf{S}^{\mathsf{H}}\mathbf{V}^{\mathsf{H}}=\mathsf{rbki}(\mathbf{A},\boldsymbol{\Omega},q),$$

the [projection of $\mathbf{A}$ onto the range](/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/) of $\mathbf{A}[\boldsymbol{\Omega},\mathbf{A}^{\mathsf{H}}\mathbf{A}\boldsymbol{\Omega},\ldots,(\mathbf{A}^{\mathsf{H}}\mathbf{A})^{q-1}\boldsymbol{\Omega}]$. Here $\mathbf{V}$ has all $q+1$ blocks. The same result group states the identity for the factors assembled from the packed coefficient blocks of an exact stored run of the program, over the reals.
:::
