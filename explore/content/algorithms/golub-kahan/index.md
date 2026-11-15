---
kind: algorithm
id: golub-kahan
title: Golub–Kahan process
summary: Build a pair of Krylov bases and a block bidiagonal factorization of a rectangular operator.
status: outline
order: 8
theory:
- krylov-spaces
- subspaces
- singular-values
- perturbation-theory
- finite-precision-krylov
library_algorithm: block-golub-kahan
uses:
- gram-schmidt
search_aliases:
- Golub–Kahan bidiagonalization
- Golub-Kahan bidiagonalization
- block Golub–Kahan
- block Golub-Kahan
- band Golub–Kahan
- block Lanczos bidiagonalization
- Golub–Kahan–Lanczos
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
library_results: false
result_ids:
- block-golub-kahan-existence
- block-golub-kahan-krylov-range
- block-golub-kahan-band-structure
- block-golub-kahan-factored-output
---

Build a right basis $\mathbf V$ and a left basis $\mathbf U$ for a rectangular matrix $\mathbf A\in\Bbbk^{m\times n}$ from a start block $\mathbf\Omega\in\Bbbk^{n\times\ell}$, together with banded coefficient matrices $\mathbf R$ and $\mathbf S$ such that

$$\mathbf A\mathbf V_{<q}=\mathbf U\mathbf R,\qquad\mathbf A^{\mathsf{H}}\mathbf U=\mathbf V\mathbf S.$$

The process alternates products with $\mathbf A$ and $\mathbf A^{\mathsf{H}}$. It is a shared Krylov factorization for a rectangular operator, as the Lanczos process is for a Hermitian one; randomized block Krylov iteration specifies how to use it for low-rank approximation. The library states the block form, with block width $\ell$ (named `b` in the Lean statements); $\ell=1$ gives bidiagonalization from a single start vector.

This page holds the exact mathematical process and its theory. The program, its certificate, and the bounds for a rounded run are on the implementation page.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

The process is defined over an orthogonalization step given by a contract, not by a formula.

::: definition decl:NLAlib.IsBasisExtension name="Exact extension of a basis by a block"
Let $\mathbf Q$ be a stored basis with $n$ rows and $\mathbf W$ a block of $\ell$ columns. A new block $\mathbf Q'$ with coefficients $\mathbf H$ and $\mathbf R$ is an exact extension of $\mathbf Q$ by $\mathbf W$ when

1. $\mathbf W=\mathbf Q\mathbf H+\mathbf Q'\mathbf R$ with $\mathbf R$ upper triangular;
2. the columns of $\mathbf Q'$ are combinations of the columns of $\mathbf Q$ and $\mathbf W$;
3. a zero column of $\mathbf W$ gives a zero column of $\mathbf Q'$;
4. the rows of $\mathbf H$ and $\mathbf R$ at zero columns of $\mathbf Q$ and $\mathbf Q'$ are zero;
5. if the nonzero columns of $\mathbf Q$ are orthonormal, so are the nonzero columns of $[\mathbf Q,\mathbf Q']$.

This is a relation, not a function: the scheme decides which columns of $\mathbf Q'$ are zero, so dependent columns may be dropped. No condition is imposed on $\mathbf Q$ itself.
:::

::: definition decl:NLAlib.IsBlockGolubKahan name="Block Golub–Kahan process"
Write $\operatorname{extend}(\mathbf Q,\mathbf W)$ for any exact extension of $\mathbf Q$ by $\mathbf W$. All blocks have width $\ell$ and are stored side by side.

1. $\mathbf V_0,\ \mathbf R_0=\operatorname{extend}(\emptyset,\mathbf\Omega)$.
2. For $j=0,\ldots,q-1$:
   1. $\mathbf U_j=\operatorname{extend}(\mathbf U_{<j},\ \mathbf A\mathbf V_j)$, with coefficients stored in block column $j$ of $\mathbf R$;
   2. $\mathbf V_{j+1}=\operatorname{extend}(\mathbf V_{\le j},\ \mathbf A^{\mathsf{H}}\mathbf U_j)$, with coefficients stored in block column $j$ of $\mathbf S$.

The output is $\mathbf{U}\in\Bbbk^{m\times q\ell}$, $\mathbf{V}\in\Bbbk^{n\times(q+1)\ell}$, $\mathbf{R}_0\in\Bbbk^{\ell\times \ell}$, $\mathbf{R}\in\Bbbk^{q\ell\times q\ell}$, and $\mathbf{S}\in\Bbbk^{(q+1)\ell\times q\ell}$; the rows of each coefficient block column below the newly extended block are zero. Every block is extended against all earlier blocks of its side. Because an extension is a relation, the process is a relation between the input $(\mathbf A,\mathbf\Omega,q)$ and the stored matrices $(\mathbf U,\mathbf V,\mathbf R_0,\mathbf R,\mathbf S)$, over real or complex scalars. An exact run is any output related to the input; the statements below hold for every exact run.
:::

## Mathematical guarantees

These statements hold in exact arithmetic, for every $\mathbf A$, every start block, and every exact extension scheme. Dependent start columns, rank-deficient $\mathbf A$, and breakdown inside the run are included: a dropped direction is a zero column of the stored basis.

::: theorem decl:NLAlib.IsBlockGolubKahan.mul_blockPrefix_right_eq name="First block relation" id=first-relation
For an exact run, with $\mathbf V_{<q}$ the first $q$ blocks of the right basis,

$$\mathbf A\mathbf V_{<q}=\mathbf U\mathbf R.$$
:::

::: theorem decl:NLAlib.IsBlockGolubKahan.conjTranspose_mul_left_eq name="Second block relation" id=second-relation
For an exact run, with $\mathbf V$ the right basis of all $q+1$ blocks,

$$\mathbf A^{\mathsf{H}}\mathbf U=\mathbf V\mathbf S.$$
:::

::: theorem decl:NLAlib.IsBlockGolubKahan.gramDefect_right_eq_zero name="Orthonormal bases" id=orthonormal-bases
For an exact run, the nonzero columns of the right basis are orthonormal:

$$\mathbf V^{\mathsf{H}}\mathbf V=\operatorname{diag}(\mathbf s),\qquad s_c=0\ \text{at a zero column of }\mathbf V,\quad s_c=1\ \text{otherwise}.$$

The library states the same identity for the left basis $\mathbf U$.
:::

::: theorem decl:NLAlib.IsBlockGolubKahan.range_blockPrefix_right name="The right basis spans the block Krylov spaces" id=krylov-range
For an exact run and every $j\le q$, the first $j+1$ blocks of $\mathbf V$ span

$$\mathcal K_{j+1}(\mathbf A^{\mathsf{H}}\mathbf A,\mathbf\Omega)=\operatorname{range}[\mathbf\Omega,\ \mathbf A^{\mathsf{H}}\mathbf A\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{j}\mathbf\Omega].$$

Zero columns are included in the stored blocks and contribute nothing to the range. The same result group, listed under Further results, states that the first $j$ blocks of $\mathbf U$ span $\mathbf A\,\mathcal K_j(\mathbf A^{\mathsf{H}}\mathbf A,\mathbf\Omega)$ and that $\mathbf U\mathbf U^{\mathsf{H}}$ is the orthogonal projector onto the range of $\mathbf A[\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{q-1}\mathbf\Omega]$.
:::

::: theorem result:block-golub-kahan-band-structure name="Band structure of the coefficients" id=band-structure
For an exact run with block width $\ell$:

1. $\mathbf R$ is upper triangular and vanishes above its $\ell$-th superdiagonal: $R_{ic}=0$ for $i>c$ and for $c>i+\ell$.
2. $\mathbf S$ vanishes above its diagonal and below its $\ell$-th subdiagonal: $S_{ic}=0$ for $i<c$ and for $i>c+\ell$.

Thus $\mathbf R$ and $\mathbf S^{\mathsf{H}}$ are zero outside the band $0\le\text{column}-\text{row}\le \ell$. For $\ell=1$, $\mathbf S^{\mathsf{H}}$ is upper bidiagonal.
:::

::: theorem result:block-golub-kahan-existence name="A run exists for every input" id=existence
For every $\mathbf A$, every start block $\mathbf\Omega$, and every $q$, there are matrices $\mathbf U,\mathbf V,\mathbf R_0,\mathbf R,\mathbf S$ forming an exact run. The definition is therefore never vacuous.
:::

::: theorem result:block-golub-kahan-factored-output name="The factored output is the block Krylov approximation" id=factored-output
For an exact run,

$$\mathbf U\mathbf S^{\mathsf{H}}\mathbf V^{\mathsf{H}}=\mathsf{rbki}(\mathbf A,\mathbf\Omega,q),$$

the projection of $\mathbf A$ onto the range of $\mathbf A[\mathbf\Omega,\mathbf A^{\mathsf{H}}\mathbf A\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{q-1}\mathbf\Omega]$. Here $\mathbf V$ has all $q+1$ blocks. The same result group states the identity for the factors assembled from the packed coefficient blocks of an exact stored run of the program, over the reals.
:::

## Components

The orthogonalization step is a parameter of the process. The scheme the library supplies for it is a column-wise two-pass classical Gram–Schmidt extension with threshold deflation, described as an implementation of Gram–Schmidt orthogonalization.

{{ generated:components }}

## Uses and composed algorithms

The process returns bases and coefficients. Using the factors for an approximation task is a further algorithmic step with its own page.

{{ generated:applications }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
