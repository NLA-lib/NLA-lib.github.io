---
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
The certified program is `Krylov.CG.HSCG.Carried.Rounded.Stored.scalarProgram`. It starts from $\mathbf x_0=\mathbf 0$, and its rounds are those of the listing with each vector operation and each matrix–vector product replaced by scalar loops over the stored entries. Its work is a count of instructions.

::: theorem result:cg-scalar-rounded-operation-count-energy-error name="Termination, operation count and energy-norm error" id=stored-scalar-rounded
Let $\mathbf A\in\mathbb R^{n\times n}$ be symmetric with spectrum in $[a,a^{\prime}]$, $a>0$, stored entry by entry, let $\mathbf b\in\mathbb R^n$, let $k$ be the iteration cap, and put $\kappa=a^{\prime}/a$. Scalar arithmetic is any machine in the standard model with unit roundoff $u$, and comparisons of stored numbers are exact. Let $E\le1/100$ be an allowance that dominates the rounding of one scalar operation ($16u\le E$), of one dot product, vector update and scaling of length $n$, and of one row-by-row matrix–vector product, and assume

$$3Ea^{\prime}\le a,\qquad k^2\sqrt k\,E\,\kappa^2\le10^{-5}.$$

Then, for every such input and every tape, the run succeeds, and:

- it executes at most $33n^2k+157nk+242k+50n+127$ instructions, each of unit cost: scalar operations, comparisons, index arithmetic, operand addressing, loop control and allocation;
- it performs some number $m\le k$ of rounds and stores an iterate $\widehat{\mathbf x}$ and a residual vector $\widehat{\mathbf r}$; if $m<k$, then $\widehat{\mathbf r}=\mathbf 0$;
- for every solution $\mathbf x$ of $\mathbf A\mathbf x=\mathbf b$,

$$\begin{aligned}&\|\mathbf x-\widehat{\mathbf x}\|_{\mathbf A}^2\\&\quad\le4\Bigl(\frac{\sqrt{2\kappa+1}-1}{\sqrt{2\kappa+1}+1}\Bigr)^{2m}\|\mathbf x\|_{\mathbf A}^2\\&\quad+\frac{12000\,m^2\sqrt m\,E\,\kappa\,a^{\prime}\,\|\mathbf b\|_2^2}{a^2}\\&\quad+\frac{135\,m^2E\,\kappa\,\|\mathbf b\|_2^2}{a}.\end{aligned}$$

Here $\|\mathbf v\|_{\mathbf A}^2=\mathbf v^{\mathsf T}\mathbf A\mathbf v$. The first term is the exact CG rate at the condition number $2\kappa+1$; the other two are the accumulated rounding. The bound is in the number $m$ of rounds performed: reaching the cap is not a convergence claim. The instruction count is an upper bound read off the fixed program.
:::
::: end-model

## Not yet presented

- A certificate for a general starting guess in the rounded models. The rounded theorems above are for the program that starts from $\mathbf x_0=\mathbf 0$.
- The exact and the BLAS-level rounded certificates of the stored program, in which the matrix is stored and the vector operations remain primitives.
- The finite-precision results about the CG run model are on the theory page [finite-precision Krylov methods](/explore/theory/finite-precision-krylov/), not on this page.
