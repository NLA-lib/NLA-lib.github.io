---
kind: implementation
id: full-reorthogonalization
algorithm: golub-kahan
title: Block Golub–Kahan with full reorthogonalization
summary: One fixed program that draws the start block, applies the two products, and extends each basis against all of its stored blocks through an abstract extension operation.
status: outline
order: 1
arithmetic_models:
- id: exact
  arithmetic: exact
- id: rounded
  title: Rounded extension and products
library_algorithm: block-golub-kahan
library_results: false
result_ids:
- block-golub-kahan-orthogonality
- block-golub-kahan-residual
- block-golub-kahan-forward-error
- basis-extension-gram-defect
- gram-defect-projector-distance
search_aliases:
- block Golub–Kahan driver
- abstract basis extension
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
---

This page describes the library's program for the block Golub–Kahan process. The driver performs no arithmetic of its own: it draws the start block from a tape, applies $\mathbf A$ and its adjoint column by column, and calls an extension operation for every orthogonalization. Full reorthogonalization means that every extension is against all stored columns of its side. The matrix is real and is reached only through the two products. The block width is written $\ell$; the Lean statements name it `b`.

The guarantees are of three kinds, kept apart below: a certificate of the program under exact contracts, which identifies its stored output with an exact run of the process; bounds for a mathematical model of a rounded run; and, under Scope, what has not been connected.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.Krylov.GolubKahan.Band.solve name="Driver with an abstract extension operation" id=algorithm
The dimensions are $[m,n,\ell,q]$. The call $\operatorname{extend}(\mathbf Q,\mathbf W)$ extends the stored basis $\mathbf Q$ by the block $\mathbf W$ and returns the new block and its coefficients.

1. Draw an $n\times \ell$ start block $\mathbf W$ from the tape stream into scratch.
2. $\mathbf V_0,\ \mathbf G=\operatorname{extend}(\emptyset,\mathbf W)$.
3. For $j=0,\ldots,q-1$:
   1. $\mathbf W=\mathbf A\mathbf V_j$, one product per column;
   2. $\mathbf U_j$ and block column $j$ of $\mathbf R$ $=\operatorname{extend}(\mathbf U_{<j},\mathbf W)$;
   3. $\mathbf W=\mathbf A^{\mathsf{T}}\mathbf U_j$, one product per column;
   4. $\mathbf V_{j+1}$ and block column $j$ of $\mathbf S$ $=\operatorname{extend}(\mathbf V_{\le j},\mathbf W)$.
4. Return $\mathbf U,\mathbf V,\mathbf G,\mathbf R,\mathbf S$ and release the scratch block.

Storage is column-major, one word per entry: $\mathbf U$ has $q\ell m$ words, $\mathbf V$ has $(q+1)\ell n$ words, $\mathbf G$ has $\ell^2$ words, and the coefficients $\mathbf R$ and $\mathbf S$ are packed by block column. The scratch block has $\max(m,n)\,\ell$ words.
:::

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The driver uses three groups of operations: the extension of a stored basis by a block, the products with $\mathbf A$ and with its adjoint, and scalar draws from a tape stream. Each has a contract. The selector chooses the contracts for products and basis extension. Their assumptions are stated with the corresponding accuracy guarantees. The work and workspace of every primitive are parameters of the model.

A concrete orthogonalization scheme is a separate program certified against one of the two extension contracts and substituted for the operation by linking. The two-pass Gram–Schmidt extension is such a program.

## Operations and Storage

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.original_staticBudget name="Primitive operation counts" id=counts
At the sizes $(m,n,\ell,q)$, the primitive part of the static budget of the fixed program is

- $n\ell$ scalar draws from the tape stream;
- $q\ell$ products with $\mathbf A$;
- $q\ell$ products with its adjoint;
- $2q+1$ basis extensions: one of the start block against the empty basis and, for each $j<q$, one of $\ell$ columns of length $m$ against $j\ell$ stored columns and one of $\ell$ columns of length $n$ against $(j+1)\ell$ stored columns.

The full budget also counts the structural instructions (index arithmetic, addressing, allocation, and control); the library records it as the instruction count of the program, not as a closed formula.
:::

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.staticPeak_solveProgram_le_solvePeak name="Scratch storage" id=scratch
For every resource model, the scratch of the fixed program at the sizes $(m,n,\ell,q)$ is at most

$$\max(m,n)\,\ell+w+w_{\mathrm q},$$

where $w$ is the largest declared workspace among the primitive calls of the run: a draw, a product with $\mathbf A$, a product with its adjoint, and the $2q+1$ basis extensions at their dimensions. No common bound on the workspaces of the primitives is assumed. The block of $\max(m,n)\,\ell$ words holds the drawn block and then the products.

Here $w_{\mathrm q}$ is the maximum declared workspace of any query included in the program's instruction budget, with maximum zero when there are no queries. It is also zero when all admitted queries have zero workspace. Adding this reservation allows query scratch to overlap the largest live allocation, giving a conservative total in abstract word cells.
:::

The run consumes exactly $n\ell$ words of the tape. Resident memory is the five output blocks plus the scratch. The cost of an extension is that of the scheme linked for it; after linking, each of the $2q+1$ extension calls is replaced by a supplied bound on the cost of the scheme at its dimensions.

## Scope

In exact arithmetic the stored product equals $\mathsf{rbki}(\mathbf A,\mathbf\Omega,q)$, so every statement about that matrix applies to exact factors; for a standard Gaussian start block these are the bounds on the randomized block Krylov iteration page. The following are not stated in the library, and nothing on this page should be read as claiming them.

- A concrete linked certificate. The driver has a generic linking theorem, and the two-pass Gram–Schmidt extension program has an exact and a rounded statement of its own, but the certificate of the driver linked with that program over an exact or a rounded level-one model, with its typing side condition and recomputed costs, is not written.
- A rounded canonical certificate. The rounded run is stated as total execution of the implementation and as a counted run of a linked program, not as a packaged certificate.
- An end-to-end rounded accuracy theorem. The forward bound compares the returned factors with the projection onto the computed left range. The Gaussian bounds for randomized block Krylov iteration are exact-arithmetic statements and are not transferred to a rounded run.
- Complex scalars for the program. The exact process and the exact extension contract are over real or complex scalars; the stored-run predicates, the certificate, the rounded run model, and the rounded analysis of the Gram–Schmidt extension are over the reals.

## Accuracy

::: model exact

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.certifies name="Total exact certificate over an abstract extension" id=execution
For all sizes $(m,n,\ell,q)$, every real $m\times n$ matrix $\mathbf A$, every interpretation whose products are the exact products with $\mathbf A$ and its adjoint and whose basis extension meets the exact contract, and every tape, the counted run of the fixed program succeeds within its static budget and resource bounds. It consumes $n\ell$ words of the tape, releases its scratch, and leaves five output blocks that decode to an exact run for $\mathbf A$ from the start block decoded from the tape.

There is no rank, nonbreakdown, or successful-run hypothesis. The extension operation is abstract in this statement: it certifies the driver for any interpretation meeting the exact contract and does not name a concrete orthogonalization program.
:::

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.IsExactStoredRun.mul_conjTranspose_mul_conjTranspose_eq_rbki name="Stored factors of an exact run" id=stored-factors
Let $\mathbf U$, $\mathbf V$, and the packed coefficient block columns $\mathbf S_j$ be the stored blocks of an exact run for a real matrix $\mathbf A$ from the start block $\mathbf\Omega$, and let $\mathbf S$ be the assembled $(q+1)\ell\times q\ell$ matrix. Then

$$\mathbf U\mathbf S^{\mathsf{H}}\mathbf V^{\mathsf{H}}=\mathsf{rbki}(\mathbf A,\mathbf\Omega,q).$$

This is an exact-arithmetic identity for the decoded output.
:::

::: theorem decl:NLAlib.BlockKrylov.storedOutput_eq_rbki name="The stored output on the tape of a given start block" id=stored-output
Let a program be certified for the block Golub–Kahan problem with a postcondition that implies the exact-run postcondition, and let $\mathbf A$ be the real $m\times n$ input matrix. For every real $n\times\ell$ matrix $\mathbf X$, the stored product of the run on the tape carrying $\mathbf X$ is

$$\mathbf U\mathbf S^{\mathsf{H}}\mathbf V^{\mathsf{H}}=\mathsf{rbki}(\mathbf A,\mathbf X,q).$$

The equality holds for every $\mathbf X$, not almost surely. The library uses it to transfer a tail bound or an expectation for $\mathsf{rbki}(\mathbf A,\mathbf X,q)$ to the stored output of the counted run, and restates two bounds for a standard Gaussian $\mathbf X$ in that form: the gapped tail bound for every block size and the gapped expectation bound for $t+2\le\ell$. These are exact-arithmetic accuracy statements: they use the exact certificate.
:::

::: end-model

::: model rounded

The rounded statements are over the reals. They concern a mathematical run model: a relation satisfied by stored matrices, with error parameters. Under rounded contracts for the products and the extension, the library states that the same program runs in total mode and that its stored blocks decode to such a run, and it states the orthogonality and forward bounds below for the decoded output words. These are statements under assumed contracts for an abstract extension operation.

::: definition decl:NLAlib.IsBasisExtensionErr name="Rounded extension of a basis by a block"
For a matrix $\mathbf Q$, let $\mathbf D(\mathbf Q)=\mathbf Q^{\mathsf{T}}\mathbf Q-\operatorname{diag}(\mathbf s)$ be its Gram defect on the support, where $s_j=0$ at a zero column and $s_j=1$ otherwise. A rounded extension of $\mathbf Q$ by a block $\mathbf W$ of $\ell$ columns, with parameters $(\eta_0,\mu,\varepsilon)$, consists of $\mathbf Q'$, $\mathbf H$, and an upper triangular $\mathbf R$ such that a zero column of $\mathbf W$ gives a zero column of $\mathbf Q'$ and, whenever $\mathbf Q$ lies in the window

$$\sqrt{\|\mathbf{D}(\mathbf{Q})\|_{\mathrm{F}}^2+3\ell\mu^2}\le\eta_0,$$

1. $\|\mathbf W-\mathbf Q\mathbf H-\mathbf Q'\mathbf R\|_{\mathrm F}\le\varepsilon\|\mathbf W\|_{\mathrm F}$;
2. every column $\mathbf q'_c$ of $\mathbf Q'$ is zero, or satisfies $\bigl|\|\mathbf q'_c\|^2-1\bigr|\le\mu$ and $\|\mathbf Q^{\mathsf{T}}\mathbf q'_c\|^2+\sum_{c'<c}(\mathbf q'_{c'}\cdot\mathbf q'_c)^2\le\mu^2$.

The bound on a kept column is absolute, so the scheme owns the decision to drop a column.
:::

::: definition decl:NLAlib.IsBlockGolubKahanErr name="Rounded run of the block Golub–Kahan process"
A rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$ and product parameter $\varepsilon_{\mathrm{mv}}$ has the same stored shape as an exact run. Block $0$ of $\mathbf V$ is a rounded extension of the empty basis by $\mathbf\Omega$. For each $j<q$ there are computed products $\mathbf P\approx\mathbf A\mathbf V_j$ and $\mathbf P'\approx\mathbf A^{\mathsf{T}}\mathbf U_j$ whose columns satisfy

$$\|(\mathbf P-\mathbf A\mathbf V_j)\mathbf e_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf A\|_2\|\mathbf V_j\mathbf e_c\|,\qquad\|(\mathbf P'-\mathbf A^{\mathsf{T}}\mathbf U_j)\mathbf e_c\|\le\varepsilon_{\mathrm{mv}}\|\mathbf A\|_2\|\mathbf U_j\mathbf e_c\|,$$

such that $\mathbf U_j$ is a rounded extension of $\mathbf U_{<j}$ by $\mathbf P$ and $\mathbf V_{j+1}$ is a rounded extension of $\mathbf V_{\le j}$ by $\mathbf P'$, with coefficients stored as in the exact process.
:::

::: theorem result:block-golub-kahan-orthogonality name="Orthogonality of the computed bases" id=orthogonality
Let $\mathbf U$ ($q\ell$ columns) and $\mathbf V$ ($(q+1)\ell$ columns) be the bases of a rounded run with scheme parameters $(\eta_0,\mu,\varepsilon)$, and let $\mathbf D(\cdot)$ be the Gram defect on the support. If $\mu\ge0$ and $\sqrt{3q\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{U})\|_{\mathrm{F}}\le\sqrt{3q\ell}\,\mu.$$

If $\mu\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$, then

$$\|\mathbf{D}(\mathbf{V})\|_{\mathrm{F}}\le\sqrt{3(q+1)\ell}\,\mu.$$

The bounds measure orthonormality of the nonzero columns; dropped columns are allowed.
:::

::: theorem result:block-golub-kahan-residual name="Residuals of the two block relations" id=residuals
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. With $\mathbf V_{<q}$ the first $q$ blocks of $\mathbf V$,

$$\|\mathbf{A}\mathbf{V}_{<q}-\mathbf{U}\mathbf{R}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2,$$

$$\|\mathbf{A}^{\mathsf{T}}\mathbf{U}-\mathbf{V}\mathbf{S}\|_{\mathrm{F}}\le\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\,\|\mathbf{A}\|_2.$$
:::

::: theorem result:block-golub-kahan-forward-error name="Forward bound for the returned factors" id=forward-error
For a rounded run with parameters $(\eta_0,\mu,\varepsilon)$ and $\varepsilon_{\mathrm{mv}}$, suppose $\mu,\varepsilon,\varepsilon_{\mathrm{mv}}\ge0$ and $\sqrt{3(q+1)\ell}\,\mu\le\eta_0$. Let $\mathbf P_{\mathbf U}$ be the orthogonal projector onto the range of the computed $\mathbf U$. Then, in the Frobenius norm and in the spectral norm,

$$\|\mathbf{A}-\mathbf{U}\mathbf{S}^{\mathsf{T}}\mathbf{V}^{\mathsf{T}}\|\le\|(\mathbf{I}-\mathbf{P}_{\mathbf{U}})\mathbf{A}\|+\Bigl(\sqrt{3q\ell}\,\mu+\sqrt{1+\eta_0}\,\bigl(\varepsilon_{\mathrm{mv}}+\varepsilon(1+\varepsilon_{\mathrm{mv}})\bigr)\sqrt{q\ell(1+\eta_0)}\Bigr)\|\mathbf{A}\|_2,$$

where the two unsubscripted norms are the same norm and the last factor is the spectral norm in both cases. The comparison is with the projection of $\mathbf A$ onto the computed left range. The statement does not bound the distance from that range to the exact block Krylov range.
:::

The orthogonality bounds rest on a one-step estimate for the Gram defect under a rounded extension, and the forward bound on a comparison of $\mathbf Q\mathbf Q^{\mathsf{T}}$ with the range projector of $\mathbf Q$; both are listed under Further results.

### Further results

{{ generated:results }}

::: end-model

## Mathematical method

{{ generated:mathematical-method }}
