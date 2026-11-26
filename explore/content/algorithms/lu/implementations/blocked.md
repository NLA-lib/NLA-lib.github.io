---
uid: 42456bb0-c332-579f-97e9-bb211ca9aba4
kind: implementation
id: blocked
algorithm: lu
title: Blocked scalar elimination
summary: Clipped panels and packed scalar matrix products on the original Gaussian no-breakdown domain.
status: ready
implementation_declarations:
- NLAlib.LU.factorBlocked
- NLAlib.LU.blockedLoop
- NLAlib.LU.blockedStep
- NLAlib.LU.panelSchurStep
- NLAlib.Ops.ScalarMatrix.update
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

The input is an $N\times N$ real matrix in column-major storage, with entry $(i,j)$ at offset $jN+i$. The source is read only. The caller supplies separate blank $N^2$-cell lower and upper output buffers; all residual and temporary buffers are scoped scratch. The routine copies the source before zero-filling the factors. Buffer capacity, liveness, and separation are part of the stored-execution contract.

The dimensions are the order $N$, a positive block size $B$, and the exact block count $Q=\lceil N/B\rceil=(N+B-1)/B$. `NLAlib.LU.factorBlocked` clips the final panel, performs two saved-operand rectangle updates per panel pivot, and then applies an actual packed scalar matrix product to the trailing square.

```text
if N > 0:
    R = copy(A); L = zeros(N,N); U = zeros(N,N)
    for block = 0,...,Q-1:
        start = B*block; width = min(B,N-start); stop = start+width
        for k = start,...,stop-1:
            materialize lower column k and upper row k from R
            save whole pivot column c and row r; a = (-1)/R[k,k]
            rank_one_rectangle(R[k:N,k:stop], a,c[k:N],r[k:stop])
            rank_one_rectangle(R[k:stop,stop:N], a,c[k:stop],r[stop:N])
        X = pack(L[stop:N,start:stop])
        Y = pack(U[start:stop,stop:N])
        T = scalar_matrix_product(X,Y)
        R[stop:N,stop:N] = R[stop:N,stop:N] - T
return L,U
```

The materialization writes a literal one on the lower diagonal, uses guarded scalar divisions for its tail, and copies the upper row tail. `rank_one_rectangle` packs the rectangle, updates each entry in column-major order using `t=a*r[j]` then `R[i,j]+t*c[i]`, and copies it back. Both rectangles use the same original saved operands. The trailing product computes scalar dot products in increasing inner-index order, starting at literal zero, then subtracts the packed product entrywise. There is no atomic GEMM, factorization primitive, or host-computed factor witness.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

Scalar operations satisfy `ExactModel`; comparisons agree with decoded real values. Pivoted routines also require exact stored-index literals and bounded stored-index queries (`IsIndexLit`, `IsToNat`). The boxed certificates instantiate the scalar/index profile over real words with exact arithmetic.

## Operations and Storage

Work and sequential span count full unit-cost structural instructions: scalar operations, comparisons, index queries, addressing, loops, calls, and allocation. Storage is in abstract unit-width cells. Caller storage includes the original matrix and blank output capacities; scratch is additional. These are bounds on the actual Ops tree, including order zero, rather than floating-point operation counts or elapsed-time estimates.

::: theorem decl:NLAlib.LU.BlockedCertification.eval_countPoly_program name="Actual blocked instruction polynomial"
At dimensions $(N,B,Q)$, work and sequential span are bounded by the evaluated actual-tree polynomial
$$\begin{aligned}
W(N,B,Q)={}&395BQ+180NB^2Q+180NB^2Q^2\\
&+49B^2Q+49B^2Q^2+83N^2Q+22NQ\\
&+33N^2BQ+187NBQ+215Q+22N^2+75.
\end{aligned}$$
This conservative structural count includes scalar packing, multiplication, subtraction, clipping, and control. Oversized blocks can make it loose.
:::

::: theorem decl:NLAlib.LU.BlockedCertification.staticPeak_program_le name="Additional scratch"
The actual tree uses at most $5N^2+2N+3$ additional cells, independent of caller offsets. The caller supplies $3N^2$ cells for the source and two blank factor buffers.
:::

::: theorem decl:NLAlib.LU.BlockedCertification.algorithm_checked name="Exact blocked certificate"
For positive $B$, exact ceiling count $Q$, and original nonzero Gaussian pivots, the concrete boxed `Algorithm` checks the actual scalar program's specification, confinement, full instruction work, and additional scratch allowance.
:::

## Accuracy

::: theorem decl:NLAlib.LU.factorBlocked_meets name="Canonical factors on the original Gaussian domain"
Assume $B>0$, $Q=(N+B-1)/B$, and $\texttt{gaussState}(A,k)_{kk}\ne0$ for every $k<N$. The actual outputs are the canonical lower and upper factors of the original input, are unit lower and upper triangular, and satisfy $A=LU$. No execution premise or previously supplied factorization is assumed.
:::

The original Gaussian-pivot condition is the same as for unpivoted scalar LU; positive-order singular inputs are outside this domain. For $N=0$ it is vacuous and the valid block count is $Q=0$.

::: theorem decl:NLAlib.LU.eval_factorBlocked_zero name="Empty execution"
At order zero the actual guard returns the original memory without reading operands or entering a frame, independently of block dimensions, handles, aliases, and arithmetic. The factorization certificate additionally retains its declared positive-block and exact-count domain.
:::

## Not yet presented

A rounded guarantee for this blocked scalar matrix-product listing is not offered here.
