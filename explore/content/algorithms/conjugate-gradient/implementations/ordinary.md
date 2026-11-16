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
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm


The standard carried-residual implementation of CG.

{{ generated:cg-definition }}

## Operations and Storage

{{ generated:cg-resources }}

## Accuracy

{{ generated:cg-accuracy }}

## Stored scalar program in rounded arithmetic

The sections above describe the matrix-free program: its matrix–vector product is a primitive, and the model selector chooses the contracts of its vector operations. The library also certifies the same recurrence, started at $\mathbf x_0=\mathbf 0$, as a different program. The matrix is stored entry by entry, and every matrix–vector product and vector operation is written out as scalar loops. Its only primitives are scalar operations and comparisons, so its work is a count of instructions and its arithmetic is the standard model alone. It is not one of the models of the selector.

::: theorem result:cg-scalar-rounded-operation-count-energy-error name="Termination, operation count and energy-norm error" id=stored-scalar-rounded
Let $\mathbf A\in\mathbb R^{n\times n}$ be symmetric with spectrum in $[a,a^{\prime}]$, $a>0$, stored entry by entry, let $\mathbf b\in\mathbb R^n$, let $k$ be the iteration cap, and put $\kappa=a^{\prime}/a$. Scalar arithmetic is any machine in the standard model with unit roundoff $u$, and comparisons of stored numbers are exact. Let $E\le1/100$ be an allowance that dominates the rounding of one scalar operation ($16u\le E$), of one dot product, vector update and scaling of length $n$, and of one row-by-row matrix–vector product, and assume

$$3Ea^{\prime}\le a,\qquad k^2\sqrt k\,E\,\kappa^2\le10^{-5}.$$

Then, for every such input and every tape, the run succeeds, and:

- it executes at most $33n^2k+157nk+242k+50n+127$ instructions, each of unit cost: scalar operations, comparisons, index arithmetic, operand addressing, loop control and allocation;
- it performs some number $m\le k$ of rounds and stores an iterate $\widehat{\mathbf x}$ and a residual vector $\widehat{\mathbf r}$; if $m<k$, then $\widehat{\mathbf r}=\mathbf 0$;
- for every solution $\mathbf x$ of $\mathbf A\mathbf x=\mathbf b$,

$$\|\mathbf x-\widehat{\mathbf x}\|_{\mathbf A}^2\le4\Bigl(\frac{\sqrt{2\kappa+1}-1}{\sqrt{2\kappa+1}+1}\Bigr)^{2m}\|\mathbf x\|_{\mathbf A}^2+\frac{12000\,m^2\sqrt m\,E\,\kappa\,a^{\prime}\,\|\mathbf b\|_2^2}{a^2}+\frac{135\,m^2E\,\kappa\,\|\mathbf b\|_2^2}{a}.$$

Here $\|\mathbf v\|_{\mathbf A}^2=\mathbf v^{\mathsf T}\mathbf A\mathbf v$. The first term is the exact CG rate at the condition number $2\kappa+1$; the other two are the accumulated rounding. The bound is in the number $m$ of rounds performed: reaching the cap is not a convergence claim. The instruction count is an upper bound read off the fixed program.
:::
