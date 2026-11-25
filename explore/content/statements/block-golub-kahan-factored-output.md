---
kind: statement
id: block-golub-kahan-factored-output
uid: 4acf79f1-542a-5cb1-ad06-82ac78de683b
---

::: theorem result:block-golub-kahan-factored-output name="The factored output is the block Krylov approximation" id=factored-output
For an exact run,

$$\mathbf{U}\mathbf{S}^{\mathsf{H}}\mathbf{V}^{\mathsf{H}}=\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q),$$

the projection of $\mathbf{A}$ onto the range of $\mathbf{A}[\mathbf\Omega,\mathbf{A}^{\mathsf{H}}\mathbf{A}\mathbf\Omega,\ldots,(\mathbf{A}^{\mathsf{H}}\mathbf{A})^{q-1}\mathbf\Omega]$. Here $\mathbf{V}$ has all $q+1$ blocks. The same result group states the identity for the factors assembled from the packed coefficient blocks of an exact stored run of the program, over the reals.
:::
