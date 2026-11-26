---
uid: dae5bf0f-7815-5308-bd17-d9a904e63990
kind: implementation
id: threshold
algorithm: plu
title: Threshold pivoting
summary: Keep the diagonal when it meets a fixed rational threshold; otherwise use a column maximum.
status: ready
implementation_declarations:
- NLAlib.LU.factorThreshold
- NLAlib.LU.thresholdChoice
- NLAlib.LU.thresholdCandidate
- NLAlib.LU.pivotedStep
- NLAlib.LU.step
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

The input is an $N\times N$ real matrix in column-major storage, with entry $(i,j)$ at offset $jN+i$. The source is read only. The caller supplies separate blank $N^2$-cell lower and upper output buffers; all residual and temporary buffers are scoped scratch. The routine copies the source before zero-filling the factors. Buffer capacity, liveness, and separation are part of the stored-execution contract.

The row log $H_k$ records the selected **current-position** row at step $k$, with $k\le H_k<N$. It is a swap history, not the final permutation vector. Write $P=\texttt{luPivotPermutation}(H,N)$ for its composition. The permuted original matrix is $B=A.\texttt{submatrix}(P,\mathrm{id})$, meaning $B_{ij}=A_{P(i),j}$.

Fix a rational $0<\tau\le1$ when constructing the routine. `select_pivot` first scans for the first maximum row $m$ in active column $k$, computes the scalar product $\tau |R_{mk}|$, and selects $r=k$ if $\tau |R_{mk}|\le|R_{kk}|$; otherwise $r=m$. Equality accepts the diagonal. The column choice is $c=k$. The rational literal and its multiplication are actual counted instructions.

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

Scalar operations satisfy `ExactModel`; comparisons agree with decoded real values. Pivoted routines also require exact stored-index literals and bounded stored-index queries (`IsIndexLit`, `IsToNat`). The boxed certificates instantiate the scalar/index profile over real words with exact arithmetic.
The threshold literal is the exact rational $\tau$, with $0<\tau\le1$.

## Operations and Storage

Work and sequential span count full unit-cost structural instructions: scalar operations, comparisons, index queries, addressing, loops, calls, and allocation. Storage is in abstract unit-width cells. Caller storage includes the original matrix and blank output capacities; scratch is additional. These are bounds on the actual Ops tree, including order zero, rather than floating-point operation counts or elapsed-time estimates.


::: theorem decl:NLAlib.LU.ThresholdCertification.eval_countPoly_program name="Instruction work and span"
The actual program's instruction polynomial evaluates to
$$W(N)=22N^3+323N^2+725N+112.$$
:::

::: theorem decl:NLAlib.LU.ThresholdCertification.staticPeak_program_le name="Additional scratch"
Additional scratch is at most $N^2+2N+7$ cells. The caller supplies $3N^2+N$ resident cells, including all blank outputs.
:::

::: theorem decl:NLAlib.LU.ThresholdCertification.algorithm_checked name="Exact stored-program certificate"
Under exact arithmetic, the concrete boxed `Algorithm` checks its specification, work, confinement, and additional-space bounds on its declared original-input domain. This certificate accounts for the actual program and its input/output capacities.
:::

## Accuracy

::: theorem decl:NLAlib.LU.factorThreshold_meets name="Exact factors from actual pivot history"
For every original real matrix, the actual logs determine $B$ as above. The returned factors are its canonical lower and upper factors, satisfy $B=LU$, and obey $|L_{ij}|\le\tau^{-1}$. The lower factor is unit triangular. Singular and empty matrices are included; a zero selected pivot has zero active column and skips unsafe division.
:::

## Not yet presented

A rounded model is not offered for this threshold listing: rounding the threshold product requires a separate pivot-quality analysis.
