---
uid: 47f2edd8-f71a-55b8-9383-6f705f4eeac3
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

This page describes the library's program for the block Golub–Kahan process. The driver performs no arithmetic of its own: it draws the start block from a tape, applies $\mathbf{A}$ and its adjoint column by column, and calls an extension operation for every orthogonalization. Full reorthogonalization means that every extension is against all stored columns of its side. The matrix is real and is reached only through the two products. The block width is written $\ell$; the Lean statements name it `b`.

The guarantees are of three kinds, kept apart below: a certificate of the program under exact contracts, which identifies its stored output with an exact run of the process; bounds for a mathematical model of a rounded run; and, under Scope, what has not been connected.

{{ generated:source-guides }}

## Algorithm

{{ statement:nlalib-krylov-golubkahan-band-solve-23f709a3 }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The driver uses three groups of operations: the extension of a stored basis by a block, the products with $\mathbf{A}$ and with its adjoint, and scalar draws from a tape stream. Each has a contract. The selector chooses the contracts for products and basis extension. Their assumptions are stated with the corresponding accuracy guarantees. The work and workspace of every primitive are parameters of the model.

A concrete orthogonalization scheme is a separate program certified against one of the two extension contracts and substituted for the operation by linking. The two-pass Gram–Schmidt extension is such a program.

## Operations and Storage

{{ statement:nlalib-krylov-golubkahan-band-certification-original-staticbudget }}

{{ statement:nlalib-krylov-golubkahan-band-certification-staticpeak-solveprogram-le-solvepeak }}

The run consumes exactly $n\ell$ words of the tape. Resident memory is the five output blocks plus the scratch. The cost of an extension is that of the scheme linked for it; after linking, each of the $2q+1$ extension calls is replaced by a supplied bound on the cost of the scheme at its dimensions.

## Scope

In exact arithmetic the stored product equals $\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)$, so every statement about that matrix applies to exact factors; for a standard Gaussian start block these are the bounds on the randomized block Krylov iteration page. The following are not stated in the library, and nothing on this page should be read as claiming them.

- A concrete linked certificate. The driver has a generic linking theorem, and the two-pass Gram–Schmidt extension program has an exact and a rounded statement of its own, but the certificate of the driver linked with that program over an exact or a rounded level-one model, with its typing side condition and recomputed costs, is not written.
- A rounded canonical certificate. The rounded run is stated as total execution of the implementation and as a counted run of a linked program, not as a packaged certificate.
- An end-to-end rounded accuracy theorem. The forward bound compares the returned factors with the projection onto the computed left range. The Gaussian bounds for randomized block Krylov iteration are exact-arithmetic statements and are not transferred to a rounded run.
- Complex scalars for the program. The exact process and the exact extension contract are over real or complex scalars; the stored-run predicates, the certificate, the rounded run model, and the rounded analysis of the Gram–Schmidt extension are over the reals.

## Accuracy

::: model exact

{{ statement:nlalib-krylov-golubkahan-band-certification-certifies }}

{{ statement:nlalib-krylov-golubkahan-band-isexactstoredrun-mul-conjtranspose-mul-conjtranspose-eq-rbki }}

{{ statement:nlalib-blockkrylov-storedoutput-eq-rbki }}

::: end-model

::: model rounded

The rounded statements are over the reals. They concern a mathematical run model: a relation satisfied by stored matrices, with error parameters. Under rounded contracts for the products and the extension, the library states that the same program runs in total mode and that its stored blocks decode to such a run, and it states the orthogonality and forward bounds below for the decoded output words. These are statements under assumed contracts for an abstract extension operation.

{{ statement:nlalib-isbasisextensionerr-fb78aa8d }}

{{ statement:nlalib-isblockgolubkahanerr-593daa98 }}

{{ statement:block-golub-kahan-orthogonality }}

{{ statement:block-golub-kahan-residual }}

{{ statement:block-golub-kahan-forward-error }}

The orthogonality bounds rest on a one-step estimate for the Gram defect under a rounded extension, and the forward bound on a comparison of $\mathbf{Q}\mathbf{Q}^{\mathsf{T}}$ with the range projector of $\mathbf{Q}$; both are listed under Further results.

### Further results

{{ generated:results }}

::: end-model

## Mathematical method

{{ generated:mathematical-method }}
