---
kind: statement
id: nlalib-mgs-factorprogram-8f827d72
uid: 8f827d72-be63-547b-b653-014c1f9c9eeb
---

::: definition decl:NLAlib.MGS.factorProgram name="In-place modified Gram–Schmidt" id=algorithm
1. Allocate two scalar scratch cells.
2. For each column $j=0,\ldots,m-1$:
   1. Use the stored column as the current residual $\mathbf{v}$.
   2. For each earlier column $i=0,\ldots,j-1$:
      1. Compute the Hermitian coefficient $r=\mathbf{q}_i^{\mathsf{H}}\mathbf{v}$.
      2. Store the negated coefficient in scratch.
      3. Update the current column in place by $\mathbf{v}\leftarrow\mathbf{v}-r\mathbf{q}_i$.
   3. Compute $t=\mathbf{v}^{\mathsf{H}}\mathbf{v}$.
   4. Store a zero literal in the comparison cell.
   5. If $t$ is nonzero, replace it by $\sqrt t$ and divide the column by that value.
   6. Otherwise leave the zero residual unchanged.
3. Release the two scratch cells and return the overwritten matrix.

Each projection coefficient uses the already updated residual. This is the modified update order; forming all coefficients before the updates would be a classical pass.
:::
