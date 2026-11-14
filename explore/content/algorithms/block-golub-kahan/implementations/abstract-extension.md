---
kind: implementation
id: abstract-extension
algorithm: block-golub-kahan
title: Block Golub–Kahan driver over an abstract basis extension
summary: One fixed program that draws the start block, applies the two products, and delegates every orthogonalization to an extension operation.
status: outline
order: 1
library_algorithm: block-golub-kahan
library_results: false
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
---

This page describes the library's program for block Golub–Kahan bidiagonalization with full reorthogonalization. The driver performs no arithmetic of its own: it draws the start block from a tape, applies $\mathbf A$ and its adjoint column by column, and calls an extension operation for every orthogonalization. The matrix is real and is reached only through the two products.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.Krylov.GolubKahan.Band.solve name="Driver with an abstract extension operation" id=algorithm
The dimensions are $[m,n,\ell,q]$, with $\ell$ the block width (named `b` in the Lean source). The call $\operatorname{extend}(\mathbf Q,\mathbf W)$ extends the stored basis $\mathbf Q$ by the block $\mathbf W$ and returns the new block and its coefficients.

1. Draw an $n\times \ell$ start block $\mathbf W$ from the tape stream into scratch.
2. $\mathbf V_0,\ \mathbf G=\operatorname{extend}(\emptyset,\mathbf W)$.
3. For $j=0,\ldots,q-1$:
   1. $\mathbf W=\mathbf A\mathbf V_j$, one product per column;
   2. $\mathbf U_j$ and block column $j$ of $\mathbf R$ $=\operatorname{extend}(\mathbf U_{<j},\mathbf W)$;
   3. $\mathbf W=\mathbf A^{\mathsf{T}}\mathbf U_j$, one product per column;
   4. $\mathbf V_{j+1}$ and block column $j$ of $\mathbf S$ $=\operatorname{extend}(\mathbf V_{\le j},\mathbf W)$.
4. Return $\mathbf U,\mathbf V,\mathbf G,\mathbf R,\mathbf S$ and release the scratch block.

Every extension is against all stored columns of its side. Storage is column-major, one word per entry: $\mathbf U$ has $q\ell m$ words, $\mathbf V$ has $(q+1)\ell n$ words, $\mathbf G$ has $\ell^2$ words, and the coefficients $\mathbf R$ and $\mathbf S$ are packed by block column. The scratch block has $\max(m,n)\,\ell$ words.
:::

## Model of arithmetic

The driver uses three groups of operations: the extension of a stored basis by a block, the products with $\mathbf A$ and with its adjoint, and scalar draws from a tape stream. Each has a contract. The exact extension contract is the relation defining an exact basis extension on the mathematical method page; the rounded contract is the rounded extension with parameters $(\eta_0,\mu,\varepsilon)$. Products are either exact or within normwise allowances.

A concrete orthogonalization scheme is a separate program certified against one of the two extension contracts and substituted for the operation by linking. The two-pass Gram–Schmidt extension is such a program.

## Operations and Storage

The library's guide records the primitive part of the static budget of the driver: $n\ell$ scalar draws, $q\ell$ products with $\mathbf A$, $q\ell$ products with its adjoint, and $2q+1$ basis extensions (one of the start block and two per step). The full budget also counts structural instructions. The run consumes exactly $n\ell$ words of the tape. The exact Lean budget and scratch statements are in the source guide and the library reference.

## Accuracy

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.certifies name="Total exact certificate over an abstract extension" id=execution
For all sizes $(m,n,\ell,q)$, every real $m\times n$ matrix $\mathbf A$, every interpretation whose products are the exact products with $\mathbf A$ and its adjoint and whose basis extension meets the exact contract, and every tape, the counted run of the fixed program succeeds within its static budget and resource bounds. It consumes $n\ell$ words of the tape, releases its scratch, and leaves five output blocks that decode to an exact run for $\mathbf A$ from the start block decoded from the tape.

There is no rank, nonbreakdown, or successful-run hypothesis. The extension operation is abstract in this statement: it certifies the driver for any interpretation meeting the exact contract and does not name a concrete orthogonalization program.
:::

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.IsExactStoredRun.mul_conjTranspose_mul_conjTranspose_eq_rbki name="Stored factors of an exact run" id=stored-factors
Let $\mathbf U$, $\mathbf V$, and the packed coefficient block columns $\mathbf S_j$ be the stored blocks of an exact run for a real matrix $\mathbf A$ from the start block $\mathbf\Omega$, and let $\mathbf S$ be the assembled $(q+1)\ell\times q\ell$ matrix. Then

$$\mathbf U\mathbf S^{\mathsf{H}}\mathbf V^{\mathsf{H}}=\operatorname{RBKI}(\mathbf A,\mathbf\Omega,q).$$

This is an exact-arithmetic identity for the decoded output.
:::

Under rounded contracts for the products and the extension, the library states that the same program runs in total mode and that its stored blocks decode to a rounded run; the orthogonality and forward bounds of the mathematical method page are stated for the decoded output words in the contract's parameters. These are statements about the run under assumed contracts for an abstract extension operation.

## Scope

The library does not yet state the certificate of this driver linked with the two-pass Gram–Schmidt extension program, a packaged rounded certificate, or an end-to-end rounded accuracy theorem. The mathematical method page lists these limits.

## Mathematical method

{{ generated:mathematical-method }}
