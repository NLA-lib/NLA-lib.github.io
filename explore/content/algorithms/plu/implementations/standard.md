---
uid: f3c63f17-5111-5a7d-b40a-026cbff974fb
kind: implementation
id: standard
algorithm: plu
title: Partial pivoting
summary: First-maximum active-column pivoting with exact and rounded guarantees.
status: ready
implementation_declarations:
- NLAlib.LU.factorPartial
- NLAlib.LU.partialChoice
- NLAlib.LU.factorRowPivoted
- NLAlib.LU.pivotedStep
- NLAlib.LU.step
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
- id: standard
  arithmetic: standard
  program: stored-scalar
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

The input is an $N\times N$ real matrix in column-major storage, with entry $(i,j)$ at offset $jN+i$. The source is read only. The caller supplies separate blank $N^2$-cell lower and upper output buffers; all residual and temporary buffers are scoped scratch. The routine copies the source before zero-filling the factors. Buffer capacity, liveness, and separation are part of the stored-execution contract.

The row log $H_k$ records the selected **current-position** row at step $k$, with $k\le H_k<N$. It is a swap history, not the final permutation vector. Write $P=\texttt{luPivotPermutation}(H,N)$ for its composition. The permuted original matrix is $B=A.\texttt{submatrix}(P,\mathrm{id})$, meaning $B_{ij}=A_{P(i),j}$.

`select_pivot` scans rows $k,\ldots,N-1$ of column $k$ and returns the first row of maximum absolute value, paired with column $k$. Strict improvements replace the incumbent; ties retain the earliest row.

```text
if N > 0:
    R = copy(A); L = zeros(N,N); U = zeros(N,N)
    for k = 0,...,N-1:
        (r,c) = select_pivot(R,k)
        swap rows k,r of R and L
        swap columns k,k of R and U
        H[k] = r       # internal column-history word is reused
        scalar_step(k)
return L,U,H
```

Row-only policies fix `c=k`, report only `H`, and reuse one internal column-history word instead of allocating a hidden length-$N$ log. All four matching exchanges are scalar copies, including equal-index exchanges. `scalar_step(k)` first writes `L[k,k] = 1`, divides the residual column tail by `R[k,k]` into `L[k+1:N,k]`, and copies `R[k,k:N]` into the upper row. A zero pivot writes zero lower-tail literals and skips division. For a nonzero pivot it then saves the **whole** pivot column `c` and row `r`, forms `a = (-1)/R[k,k]`, and updates the **whole** residual, column by column:

```text
for j = 0,...,N-1:
    t = a * r[j]
    for i = 0,...,N-1:
        R[i,j] = R[i,j] + t * c[i]
```

At a zero pivot this residual update is skipped. The saved operands and the displayed multiplication order matter in the rounded model. This is the actual scalar tree, including retired rows and columns.


{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

::: model exact
Scalar operations satisfy `ExactModel`; comparisons agree with decoded real values. Pivoted routines also require exact stored-index literals and bounded stored-index queries (`IsIndexLit`, `IsToNat`). The boxed certificates instantiate the scalar/index profile over real words with exact arithmetic.
::: end-model

::: model standard
The same scalar instruction tree is interpreted by `StdModel u dec M`, with $u\ge0$, exact decoded comparisons, exact stored-index queries and index literals, and exact natural literals through `literalBound`, with $N\le\texttt{literalBound}$. The standard relative-error laws assume arithmetic stays within their range; this is not a universal guarantee for native IEEE or `Float` execution.
::: end-model

## Operations and Storage

Work and sequential span count full unit-cost structural instructions: scalar operations, comparisons, index queries, addressing, loops, calls, and allocation. Storage is in abstract unit-width cells. Caller storage includes the original matrix and blank output capacities; scratch is additional. These are bounds on the actual Ops tree, including order zero, rather than floating-point operation counts or elapsed-time estimates.


::: theorem decl:NLAlib.LU.PartialCertification.eval_countPoly_program name="Instruction work and span"
The actual program's instruction polynomial evaluates to
$$W(N)=22N^3+323N^2+598N+112.$$
:::

::: theorem decl:NLAlib.LU.PartialCertification.staticPeak_program_le name="Additional scratch"
Additional scratch is at most $N^2+2N+7$ cells. The caller supplies $3N^2+N$ resident cells, including all blank outputs.
:::

::: theorem decl:NLAlib.LU.PartialCertification.algorithm_checked name="Exact stored-program certificate"
Under exact arithmetic, the concrete boxed `Algorithm` checks its specification, work, confinement, and additional-space bounds on its declared original-input domain. This certificate accounts for the actual program and its input/output capacities.
:::

## Accuracy

::: model exact
::: theorem decl:NLAlib.LU.factorPartial_meets name="Exact factors from actual pivot history"
For every original real matrix, the actual logs determine $B$ as above. The returned factors are its canonical lower and upper factors, satisfy $B=LU$, and obey $|L_{ij}|\le1$. The lower factor is unit triangular. Singular and empty matrices are included; a zero selected pivot has zero active column and skips unsafe division.
:::
::: end-model

::: model standard
::: theorem decl:NLAlib.LU.Rounded.factorPartial_meets name="Rounded stored factors and backward error"
Every original matrix is admitted, including singular and empty matrices, when $N\le\texttt{literalBound}$ and the stated scalar/index laws hold. The actual logs determine $B$, the permuted original matrix. The actual factors are unit lower and upper triangular, and $|L_{ij}|\le1+u$ for every $u\ge0$. If additionally $u<1$, then
$$|(B-LU)_{ij}|\le\gamma_{N+4}\sum_k |L_{ik}|\,|U_{kj}|,$$
where $\gamma_{N+4}=\texttt{Computation.roundingFactor}(N+4,u)=(1-u)^{-(N+4)}-1$.
No nonsingularity, nonzero computed-pivot, or successful-run premise is assumed.
:::

This is a `Routine.Meets` accuracy theorem for the actual program. The boxed `Algorithm` certificate above is the exact-model certificate; the rounded result does not construct a separate boxed certificate.
::: end-model

## Not yet presented

The standard model shown here requires its stated scalar and exact-index laws. A universal native IEEE execution or native throughput guarantee is not presented.
