---
kind: implementation
id: modified
algorithm: gram-schmidt
title: Modified Gram–Schmidt
summary: Orthogonalize the stored columns in place, updating each residual after every projection.
status: ready
order: 1
source_guides:
- docs/algorithms/Gram-Schmidt.md
---

The checked program overwrites an $n\times m$ input matrix with the mathematical Gram–Schmidt columns. Dependent columns are allowed: a zero residual stays zero. This endpoint returns the basis matrix, rather than storing a triangular coefficient matrix.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.MGS.program name="In-place modified Gram–Schmidt" id=algorithm
1. Allocate two scalar scratch cells.
2. For each column $j=0,\ldots,m-1$:
   1. Use the stored column as the current residual $\mathbf v$.
   2. For each earlier column $i=0,\ldots,j-1$:
      1. Compute the Hermitian coefficient $r=\mathbf q_i^{\mathsf{H}}\mathbf v$.
      2. Store the negated coefficient in scratch.
      3. Update the current column in place by $\mathbf v\leftarrow\mathbf v-r\mathbf q_i$.
   3. Compute $t=\mathbf v^{\mathsf{H}}\mathbf v$.
   4. Store a zero literal in the comparison cell.
   5. If $t$ is nonzero, replace it by $\sqrt t$ and divide the column by that value.
   6. Otherwise leave the zero residual unchanged.
3. Release the two scratch cells and return the overwritten matrix.

Each projection coefficient uses the already updated residual. This is the modified update order; forming all coefficients before the updates would be a classical pass.
:::

## Model of arithmetic

This page presents exact real or complex field arithmetic with Hermitian dot products, vector updates, division by a scalar, square roots, and real-part comparisons. The primitive contracts permit the in-place column views used by the program. The normalization guard handles dependent columns and zero dimensions.

A cell is one abstract field value. Translating a complex value to physical real/imaginary storage is a separate representation choice.

## Operations and Storage

The column sweeps make $m(m-1)/2$ projection dot products, the same number of vector updates and scalar negations, and $m$ additional self-dot products. There are $m$ zero literals and equality tests, and at most $m$ square roots and vector normalizations. For $n,m\ge1$, with linear-cost length-$n$ vector primitives, numerical work is $O(nm^2)$. The canonical certificate also covers zero dimensions and counts structural instructions.

::: theorem decl:NLAlib.MGS.factor_peak_le name="In-place scratch bound" id=storage
If every primitive workspace is at most $w$ cells, the complete matrix program uses at most $2+w$ scratch cells above the supplied $nm$-cell matrix. Thus resident capacity is at most

$$nm+2+w.$$

With zero primitive workspace, the scoped scratch allocation is exactly two cells. This bound requires no full-rank assumption and includes the zero-residual branch.
:::

## Accuracy

::: theorem decl:NLAlib.MGS.writes_factor name="Exact execution correspondence" id=execution
Under the exact primitive contracts and the theorem's live, readable, writable matrix-buffer conditions, the program terminates and overwrites the matrix with exactly the mathematical $\operatorname{gramSchmidtQ}$ of the input. No full-rank or successful-execution premise is assumed. Rectangular matrices, dependent columns, and zero dimensions are admitted.

The shared mathematical method describes how the nonzero columns span the original range. Rounded orthogonality bounds for two classical passes concern a different implementation and are not substituted for this exact MGS statement.
:::

## Mathematical method

{{ generated:mathematical-method }}
