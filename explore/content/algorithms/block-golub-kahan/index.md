---
kind: algorithm
id: block-golub-kahan
title: Block Golub–Kahan bidiagonalization
summary: Build left and right block Krylov bases with full reorthogonalization and return factors of a low-rank approximation.
status: outline
order: 13
theory:
- krylov-spaces
- subspaces
- perturbation-theory
- finite-precision-krylov
library_algorithm: block-golub-kahan
uses:
- gram-schmidt
search_aliases:
- block Lanczos bidiagonalization
- band Golub–Kahan
- block Golub-Kahan
- Golub–Kahan–Lanczos
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
library_results: false
result_ids:
- block-golub-kahan-factored-output
- block-golub-kahan-existence
- block-golub-kahan-krylov-range
- block-golub-kahan-band-structure
- block-golub-kahan-orthogonality
- block-golub-kahan-residual
- block-golub-kahan-forward-error
- basis-extension-gram-defect
- gram-defect-projector-distance
---

Block Golub–Kahan bidiagonalization with full reorthogonalization takes a rectangular matrix $\mathbf A\in\Bbbk^{m\times n}$, a start block $\mathbf\Omega\in\Bbbk^{n\times \ell}$, and a number of block steps $q$. It alternates products with $\mathbf A$ and $\mathbf A^{\mathsf{H}}$ with an orthogonalization of each new block against all stored blocks of its side, and stores a left basis $\mathbf U$, a right basis $\mathbf V$, and two coefficient matrices $\mathbf R$ and $\mathbf S$. The block width is written $\ell$ on this page; the Lean statements name it `b`.

The library states the process over an abstract orthogonalization step, a basis extension, given by a contract rather than by a formula. The results in the first part of this page hold in exact arithmetic for every step meeting the exact contract. The results in the second part hold for a rounded run described by error parameters of the step and of the products. Which guarantees have been connected to a concrete program is stated under Scope.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.IsBasisExtension name="Exact extension of a basis by a block"
Let $\mathbf Q$ be a stored basis with $n$ rows and $\mathbf W$ a block of $\ell$ columns. A new block $\mathbf Q'$ with coefficients $\mathbf H$ and $\mathbf R$ is an exact extension of $\mathbf Q$ by $\mathbf W$ when

1. $\mathbf W=\mathbf Q\mathbf H+\mathbf Q'\mathbf R$ with $\mathbf R$ upper triangular;
2. the columns of $\mathbf Q'$ are combinations of the columns of $\mathbf Q$ and $\mathbf W$;
3. a zero column of $\mathbf W$ gives a zero column of $\mathbf Q'$;
4. the rows of $\mathbf H$ and $\mathbf R$ at zero columns of $\mathbf Q$ and $\mathbf Q'$ are zero;
5. if the nonzero columns of $\mathbf Q$ are orthonormal, so are the nonzero columns of $[\mathbf Q,\mathbf Q']$.

This is a relation, not a function: the scheme decides which columns of $\mathbf Q'$ are zero, so dependent columns may be dropped. No condition is imposed on $\mathbf Q$ itself.
:::

::: definition decl:NLAlib.IsBlockGolubKahan name="Block Golub–Kahan bidiagonalization with full reorthogonalization"
Write $\operatorname{extend}(\mathbf Q,\mathbf W)$ for any exact extension of $\mathbf Q$ by $\mathbf W$. All blocks have width $\ell$ and are stored side by side.

1. $\mathbf V_0,\ \mathbf R_0=\operatorname{extend}(\emptyset,\mathbf\Omega)$.
2. For $j=0,\ldots,q-1$:
   1. $\mathbf U_j=\operatorname{extend}(\mathbf U_{<j},\ \mathbf A\mathbf V_j)$, with coefficients stored in block column $j$ of $\mathbf R$;
   2. $\mathbf V_{j+1}=\operatorname{extend}(\mathbf V_{\le j},\ \mathbf A^{\mathsf{H}}\mathbf U_j)$, with coefficients stored in block column $j$ of $\mathbf S$.

The output is $\mathbf{U}\in\Bbbk^{m\times q\ell}$, $\mathbf{V}\in\Bbbk^{n\times(q+1)\ell}$, $\mathbf{R}_0\in\Bbbk^{\ell\times \ell}$, $\mathbf{R}\in\Bbbk^{q\ell\times q\ell}$, and $\mathbf{S}\in\Bbbk^{(q+1)\ell\times q\ell}$; the rows of each coefficient block column below the newly extended block are zero. Full reorthogonalization means that every block is extended against all earlier blocks of its side. Because an extension is a relation, the process is the relation $\operatorname{IsBlockGolubKahan}(\mathbf A,\mathbf\Omega,q;\mathbf U,\mathbf V,\mathbf R_0,\mathbf R,\mathbf S)$ between the input and the stored matrices, over real or complex scalars; the statements below hold for every output related to the input.
:::

## Components

The orthogonalization step is a parameter of the process. The library's first scheme for it is a column-wise two-pass classical Gram–Schmidt extension with threshold deflation, described as an implementation of Gram–Schmidt orthogonalization.

{{ generated:components }}

## Guarantees in exact arithmetic

::: theorem result:block-golub-kahan-factored-output name="The factored output is the block Krylov approximation"
Let $\mathbf U,\mathbf V,\mathbf R_0,\mathbf R,\mathbf S$ be related to $\mathbf A$, $\mathbf\Omega$, and $q$ by the process in exact arithmetic. Then

$$\mathbf U\mathbf S^{\mathsf{H}}\mathbf V^{\mathsf{H}}=\operatorname{RBKI}(\mathbf A,\mathbf\Omega,q),$$

the projection of $\mathbf A$ onto the range of $\mathbf A[\mathbf\Omega,\mathbf A^{\mathsf{H}}\mathbf A\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{q-1}\mathbf\Omega]$. Here $\mathbf V$ has all $q+1$ blocks. The identity holds for every $\mathbf A$, every start block, and every exact extension scheme: dependent start columns, rank-deficient $\mathbf A$, and breakdown inside the run are included. The same result group states the identity for the factors assembled from the packed coefficient blocks of an exact stored run of the program, over the reals.
:::

::: theorem result:block-golub-kahan-existence name="A run exists for every input"
For every $\mathbf A$, every start block $\mathbf\Omega$, and every $q$, there are matrices $\mathbf U,\mathbf V,\mathbf R_0,\mathbf R,\mathbf S$ related to them by the process in exact arithmetic. The definition is therefore never vacuous.
:::

::: theorem decl:NLAlib.IsBlockGolubKahan.range_blockPrefix_right name="The right basis spans the block Krylov spaces"
For an exact run and every $j\le q$, the first $j+1$ blocks of $\mathbf V$ span

$$\mathcal K_{j+1}(\mathbf A^{\mathsf{H}}\mathbf A,\mathbf\Omega)=\operatorname{range}[\mathbf\Omega,\ \mathbf A^{\mathsf{H}}\mathbf A\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{j}\mathbf\Omega].$$

Zero columns are included in the stored blocks and contribute nothing to the range. The same result group, listed under Further results, states that the first $j$ blocks of $\mathbf U$ span $\mathbf A\,\mathcal K_j(\mathbf A^{\mathsf{H}}\mathbf A,\mathbf\Omega)$ and that $\mathbf U\mathbf U^{\mathsf{H}}$ is the orthogonal projector onto the range of $\mathbf A[\mathbf\Omega,\ldots,(\mathbf A^{\mathsf{H}}\mathbf A)^{q-1}\mathbf\Omega]$.
:::

::: theorem result:block-golub-kahan-band-structure name="Band structure of the coefficients"
For an exact run with block width $\ell$:

1. $\mathbf R$ is upper triangular and vanishes above its $\ell$-th superdiagonal: $R_{ic}=0$ for $i>c$ and for $c>i+\ell$.
2. $\mathbf S$ vanishes above its diagonal and below its $\ell$-th subdiagonal: $S_{ic}=0$ for $i<c$ and for $i>c+\ell$.

Thus $\mathbf R$ and $\mathbf S^{\mathsf{H}}$ are zero outside the band $0\le\text{column}-\text{row}\le \ell$. For $\ell=1$, $\mathbf S^{\mathsf{H}}$ is upper bidiagonal.
:::

## The rounded run

The rounded statements are over the reals. They concern a mathematical run model: a relation satisfied by stored matrices, with error parameters. They do not by themselves assert that a particular program produces such a run.

::: definition decl:NLAlib.IsBasisExtensionErr name="Rounded extension of a basis by a block"
For a matrix $\mathbf Q$, let $\mathbf D(\mathbf Q)=\mathbf Q^{\mathsf{T}}\mathbf Q-\operatorname{diag}(\mathbf s)$ be its Gram defect on the support, where $s_j=0$ at a zero column and $s_j=1$ otherwise. A rounded extension of $\mathbf Q$ by a block $\mathbf W$ of $\ell$ columns, with parameters $(\eta_0,\mu,\varepsilon)$, consists of $\mathbf Q'$, $\mathbf H$, and an upper triangular $\mathbf R$ such that a zero column of $\mathbf W$ gives a zero column of $\mathbf Q'$ and, whenever $\mathbf Q$ lies in the window

$$\sqrt{\|\mathbf{D}(\mathbf{Q})\|_{\mathrm{F}}^2+3\ell\mu^2}\le\eta_0,$$

1. $\|\mathbf W-\mathbf Q\mathbf H-\mathbf Q'\mathbf R\|_{\mathrm F}\le\varepsilon\|\mathbf W\|_{\mathrm F}$;
2. every column $\mathbf q'_c$ of $\mathbf Q'$ is zero, or satisfies $\bigl|\|\mathbf q'_c\|^2-1\bigr|\le\mu$ and $\|\mathbf Q^{\mathsf{T}}\mathbf q'_c\|^2+\sum_{c'<c}(\mathbf q'_{c'}\cdot\mathbf q'_c)^2\le\mu^2$.

The bound on a kept column is absolute, so the scheme owns the decision to drop a column.
:::

::: definition decl:NLAlib.IsBlockGolubKahanErr name="Rounded run of block Golub–Kahan bidiagonalization"
A rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$ and product parameter $\varepsilon_{\mathrm{mv}}$ has the same stored shape as an exact run. Block $0$ of $\mathbf V$ is a rounded extension of the empty basis by $\mathbf\Omega$. For each $j<q$ there are computed products $\mathbf P\approx\mathbf A\mathbf V_j$ and $\mathbf P'\approx\mathbf A^{\mathsf{T}}\mathbf U_j$ whose columns satisfy

$$\|(\mathbf P-\mathbf A\mathbf V_j)\mathbf e_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf A\|_2\|\mathbf V_j\mathbf e_c\|,\qquad\|(\mathbf P'-\mathbf A^{\mathsf{T}}\mathbf U_j)\mathbf e_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf A\|_2\|\mathbf U_j\mathbf e_c\|,$$

such that $\mathbf U_j$ is a rounded extension of $\mathbf U_{<j}$ by $\mathbf P$ and $\mathbf V_{j+1}$ is a rounded extension of $\mathbf V_{\le j}$ by $\mathbf P'$, with coefficients stored as in the exact process.
:::

::: theorem result:block-golub-kahan-orthogonality name="Orthogonality of the computed bases"
Let $\mathbf U$ ($q\ell$ columns) and $\mathbf V$ ($(q+1)\ell$ columns) be the bases of a rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$, and let $\mathbf D(\cdot)$ be the Gram defect on the support. If $\mu\ge0$ and $\sqrt{3q\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{U})\|_{\mathrm{F}}\le\sqrt{3q\ell}\,\mu.$$

If $\mu\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{V})\|_{\mathrm{F}}\le\sqrt{3(q+1)\ell}\,\mu.$$

The bounds measure orthonormality of the nonzero columns; dropped columns are allowed.
:::

::: theorem result:block-golub-kahan-residual name="Residuals of the two block relations"
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. With $\mathbf V_{<q}$ the first $q$ blocks of $\mathbf V$,

$$\|\mathbf{A}\mathbf{V}_{<q}-\mathbf{U}\mathbf{R}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2,$$

$$\|\mathbf{A}^{\mathsf{T}}\mathbf{U}-\mathbf{V}\mathbf{S}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2.$$
:::

::: theorem result:block-golub-kahan-forward-error name="Forward bound for the returned factors"
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. Let $\mathbf P_{\mathbf U}$ be the orthogonal projector onto the range of the computed $\mathbf U$. Then, in the Frobenius norm and in the spectral norm,

$$\|\mathbf{A}-\mathbf{U}\mathbf{S}^{\mathsf{T}}\mathbf{V}^{\mathsf{T}}\|\le\|(\mathbf{I}-\mathbf{P}_{\mathbf{U}})\mathbf{A}\|+\Bigl(\sqrt{3q\ell}\,\mu+\sqrt{1+\eta_0}\,\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\Bigr)\|\mathbf{A}\|_2,$$

where the two unsubscripted norms are the same norm and the last factor is the spectral norm in both cases. The comparison is with the projection of $\mathbf A$ onto the computed left range. The statement does not bound the distance from that range to the exact block Krylov range.
:::

The orthogonality bounds rest on a one-step estimate for the Gram defect under a rounded extension, and the forward bound on a comparison of $\mathbf Q\mathbf Q^{\mathsf{T}}$ with the range projector of $\mathbf Q$; both are listed under Further results.

## Scope

In exact arithmetic the factored output equals $\operatorname{RBKI}(\mathbf A,\mathbf\Omega,q)$, so every statement about that matrix applies to exact factors; for a standard Gaussian start block these are the bounds on the randomized block Krylov iteration page. The implementation page describes the library's program for this process over an abstract extension operation and its exact certificate. The following are not stated in the library, and nothing on this page should be read as claiming them.

- A concrete linked certificate. The driver has a generic linking theorem, and the two-pass Gram–Schmidt extension program has an exact and a rounded statement of its own, but the certificate of the driver linked with that program over an exact or a rounded level-one model, with its typing side condition and recomputed costs, is not written.
- A rounded canonical certificate. The rounded run is stated as total execution of the implementation and as a counted run of a linked program, not as a packaged certificate.
- An end-to-end rounded accuracy theorem. The forward bound compares the returned factors with the projection onto the computed left range. The Gaussian bounds for randomized block Krylov iteration are exact-arithmetic statements and are not transferred to a rounded run.
- Complex scalars for the program. The exact process and the exact extension contract are over real or complex scalars; the stored-run predicates, the certificate, the rounded run model, and the rounded analysis of the Gram–Schmidt extension are over the reals.

## Used by other algorithms

{{ generated:applications }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
