---
uid: 18093f87-42c8-52fe-8f8f-1d428b506a86
kind: implementation
id: scaled
algorithm: plu
title: Scaled partial pivoting
summary: Cache original row norms once and transport them through row swaps.
status: ready
implementation_declarations:
- NLAlib.LU.factorScaled
- NLAlib.LU.scaledStep
- NLAlib.LU.scaledChoice
- NLAlib.LU.considerScaled
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

The row log $H_k$ records the selected **current-position** row at step $k$, with $k\le H_k<N$. It is a swap history, not the final permutation vector. Write $P=\texttt{luPivotPermutation}(H,N)$ for its composition. The permuted original matrix is $B=A.\texttt{submatrix}(P,\mathrm{id})$.

`NLAlib.LU.factorScaled` caches each **original** row's finite Pi norm,
$s_i=\|A_{i,:}\|_\infty=\max_j |A_{ij}|$, once before elimination. Scales follow row exchanges and are never recomputed from a Schur complement.

```text
if N > 0:
    R = copy(A); L = zeros(N,N); U = zeros(N,N)
    scales[i] = max_j abs(R[i,j])       # scalar row scans, original copy
    for k = 0,...,N-1:
        r = k; b = abs(R[k,k]); s = scales[k]
        for i = k+1,...,N-1:
            a = abs(R[i,k]); t = scales[i]
            if s == 0:
                if a > 0: r=i; b=a; s=t
            else:
                left = a*s; right = b*t
                if right < left: r=i; b=a; s=t
        swap rows k,r of R and L
        swap columns k,k of R and U
        swap scales[k],scales[r]
        H[k] = r
        scalar_step(k)
return L,U,H
```

The residual and cached scales share a scoped $N^2+N$-cell arena; one extra selected-index word is reused. Cross products implement the ratio comparison without executing a quotient. Zero original row scales imply zero residual rows, and the zero-incumbent branch avoids those products. Ties keep the first row. The mathematical selector maximizes $|R_{ik}|/s_i$, using the real-field convention $0/0=0$.

`scalar_step(k)` first writes `L[k,k] = 1`, divides the residual column tail by `R[k,k]` into `L[k+1:N,k]`, and copies `R[k,k:N]` into the upper row. A zero pivot writes zero lower-tail literals and skips division. For a nonzero pivot it then saves the **whole** pivot column `c` and row `r`, forms `a = (-1)/R[k,k]`, and updates the **whole** residual, column by column:

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

## Operations and Storage

Work and sequential span count full unit-cost structural instructions: scalar operations, comparisons, index queries, addressing, loops, calls, and allocation. Storage is in abstract unit-width cells. Caller storage includes the original matrix and blank output capacities; scratch is additional. These are bounds on the actual Ops tree, including order zero, rather than floating-point operation counts or elapsed-time estimates.


::: theorem decl:NLAlib.LU.ScaledCertification.eval_countPoly_program name="Instruction work and span"
The actual program's instruction polynomial evaluates to
$$W(N)=22N^3+479N^2+707N+109.$$
:::

::: theorem decl:NLAlib.LU.ScaledCertification.staticPeak_program_le name="Additional scratch"
Additional scratch is at most $N^2+3N+5$ cells. The caller supplies $3N^2+N$ resident cells, including all blank outputs.
:::

::: theorem decl:NLAlib.LU.ScaledCertification.algorithm_checked name="Exact stored-program certificate"
Under exact arithmetic, the concrete boxed `Algorithm` checks its specification, work, confinement, and additional-space bounds on its declared original-input domain. This certificate accounts for the actual program and its input/output capacities.
:::

## Accuracy

::: theorem decl:NLAlib.LU.factorScaled_meets name="Exact fixed-scale factorization"
For every original matrix, including singular matrices, zero rows, and order zero, the actual row history gives $B$ and the returned factors equal $\texttt{luLower}(B)$ and $\texttt{luUpper}(B)$, with $B=LU$. The output also satisfies `HasScaledPivotPrefix B N`, recording the completed weighted pivot property relative to original row norms. No nonzero original-pivot or successful-run assumption is required.
:::

::: definition decl:NLAlib.LU.factorScaledSpec name="Weighted output contract"
The output includes the actual active-index log, canonical factors of the corresponding original row permutation, reconstruction, and the weighted pivot property. It does **not** assert a uniform unweighted bound $|L_{ij}|\le1$: fixed-scale pivoting can produce larger multipliers.
:::

At $N=0$ the outer guard skips every call and allocation; all factors and the log are empty. A zero pivot writes zero lower-tail literals and skips unsafe reciprocal/division.

## Not yet presented

This page offers exact arithmetic. A rounded guarantee for the cross-product selector would require an additional analysis of pivot quality and arithmetic range.
