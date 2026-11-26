---
kind: implementation
id: semidefinite
algorithm: cholesky
title: Zero-guarded semidefinite factorization
summary: Exact right-looking Cholesky includes singular PSD matrices by skipping division at zero pivots.
status: ready
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
implementation_declarations:
- NLAlib.Cholesky.semidefiniteRightLooking
- NLAlib.Cholesky.semidefiniteRightWithScratch
- NLAlib.Cholesky.rightLoopTotal
- NLAlib.Cholesky.rightStepTotal
- NLAlib.Cholesky.rightStep
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

`NLAlib.Cholesky.semidefiniteRightLooking` reads a real PSD matrix $\mathbf A$ and writes its canonical square lower factor $\mathbf L$. Source and output each occupy $N^2$ column-major words, with $(i,j)$ at offset $jN+i$.

```text
if N > 0:
    allocate R[N*N]; copy A to R; fill L with literal zeros
    for k = 0,...,N-1:
        if R[k,k] == 0:
            fill L[k:N,k] with literal zeros
        else:
            t = sqrt(R[k,k])
            copy R[k+1:N,k] to L[k+1:N,k]
            divide the copied suffix by t; L[k,k] = t
            save c = R[:,k] and r = R[k,:]
            a = literal(-1) / R[k,k]
            for j = 0,...,N-1:
                s = a * r[j]
                for i = 0,...,N-1:
                    v = s * c[i]
                    R[i,j] = R[i,j] + v
    release scoped scratch
```

A zero pivot skips both normalization and the residual update. For PSD input the corresponding active residual column is zero, so this branch remains mathematically valid. Nonzero pivots are positive. The source is copied before factor initialization; the separate write theorem permits source/output overlap. At $N=0$ the raw body reads no operands, allocates nothing and preserves memory, even for arbitrary raw handles.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The scalar machine satisfies `ExactModel`, the interpreter satisfies `IsScalar`, and its zero comparison satisfies `IsCmp`. The input condition is $\mathbf A\succeq0$; no invertibility or nonzero-pivot hypothesis is required. The zero matrix, singular matrices and order zero are included.

## Operations and Storage

::: theorem decl:NLAlib.Cholesky.SemidefiniteCertification.eval_countPoly_program name="Guarded scalar instruction work"
The evaluated tree polynomial is
$$W(N)=22N^3+121N^2+198N+56.$$
This bounds abstract work and sequential span including tests, addressing and structural instructions. Zero branches may execute less work; the bound includes them.
:::

::: theorem decl:NLAlib.Cholesky.SemidefiniteCertification.staticPeak_program_le name="Scratch and caller storage"
Additional scoped storage is at most $N^2+2N+3$ scalar cells. Source and blank factor capacities add $2N^2$, so total resident storage is bounded by $3N^2+2N+3$ cells. These bounds include the empty case and describe the sequential abstract machine.
:::

## Accuracy

::: theorem decl:NLAlib.Cholesky.SemidefiniteCertification.algorithm_checked name="Singular-inclusive exact certificate"
Every real PSD input is factored successfully. The actual output equals `choleskyLower` of the original input, is lower triangular with **nonnegative** diagonal, and satisfies $\mathbf A=\mathbf L\mathbf L^{\mathsf T}$. Stored upper words are literal zeros. Only the output changes; source and buffer extents are retained, scratch is released, and the tape position is restored. Success follows from the original PSD condition and local arithmetic contracts.
:::

## Not yet presented

This page presents the exact guarded program. The relative and finite-range results on the ordinary positive-definite page do not establish rounded success for this zero-testing tree.
