---
uid: 482a436a-f199-5ac7-99f2-9beae17f0e93
kind: implementation
id: ordinary
algorithm: conjugate-gradient
title: Ordinary CG
summary: The standard carried-residual implementation of CG.
status: ready
order: 0
renderer: cg
source_variant: carried
arithmetic_models:
- id: exact
  arithmetic: exact
  program: blas-matvec
- id: relative
  arithmetic: standard
  program: relative-blas-matvec
- id: standard
  arithmetic: standard
  program: blas-matvec
  aliases: [sequential, pairwise]
- id: stored-scalar
  arithmetic: standard
  program: stored-scalar
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

The standard carried-residual implementation of CG.

{{ generated:cg-definition }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The first three models are for the program of the listing, built from vector operations and a matrix–vector product that is a primitive. They differ in what those operations may return. The last model is for a program lowered from it: the matrix is stored entry by entry, and every matrix–vector product and vector operation is written out as scalar loops, so its only primitives are scalar operations and comparisons.

## Operations and Storage

These counts are at the level of vector operations and hold for the three models built from BLAS and matvec calls. The stored scalar program has its own instruction count, stated with its theorem.

{{ generated:cg-resources }}

## Accuracy

::: model exact
{{ generated:cg-accuracy-exact }}
::: end-model

::: model relative
{{ generated:cg-accuracy-relative }}
::: end-model

::: model standard
{{ generated:cg-accuracy-standard }}
::: end-model

::: model stored-scalar
The certified program is `Krylov.CG.HSCG.Carried.Rounded.Stored.scalarProgram`. It starts from $\mathbf{x}_0=\mathbf 0$, and its rounds are those of the listing with each vector operation and each matrix–vector product replaced by scalar loops over the stored entries. Its work is a count of instructions.

{{ statement:cg-scalar-rounded-operation-count-energy-error }}
::: end-model

## Not yet presented

- A certificate for a general starting guess in the rounded models. The rounded theorems above are for the program that starts from $\mathbf{x}_0=\mathbf 0$.
- The exact and the BLAS-level rounded certificates of the stored program, in which the matrix is stored and the vector operations remain primitives.
- The finite-precision results about the CG run model are on the theory page [finite-precision Krylov methods](/explore/theory/finite-precision-krylov/), not on this page.
