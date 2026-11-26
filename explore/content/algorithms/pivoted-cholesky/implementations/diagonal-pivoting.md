---
kind: implementation
id: diagonal-pivoting
algorithm: pivoted-cholesky
title: First-maximum diagonal pivoting
summary: Scan the residual diagonal, exchange both residual coordinates and factor rows, then run a zero-safe Cholesky step.
status: ready
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
implementation_declarations:
- NLAlib.Cholesky.pivotedRightLooking
- NLAlib.Cholesky.pivotedStep
- NLAlib.Cholesky.diagonalChoice
- NLAlib.Cholesky.pivotedAdvance
- NLAlib.Cholesky.rightStepTotal
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

`NLAlib.Cholesky.pivotedRightLooking` reads a real $N\times N$ PSD matrix $\mathbf A$ and writes a square lower factor $\mathbf L$ plus an $N$-word pivot log $H$. Matrix buffers are column-major: $(i,j)$ is at $jN+i$. The log stores absolute **current-position** indices, not a final permutation vector.

```text
if N > 0:
    allocate R[N*N]; copy A to R; fill L with literal zeros
    for k = 0,...,N-1:
        gather diagonal R[k,k],...,R[N-1,N-1]
        scan for its first maximum absolute value
        read selected absolute index r through a bounded stored-index query
        swap rows k,r and columns k,r of R
        swap the full rows k,r of L
        store the dimension literal r in H[k]
        if R[k,k] == 0:
            fill L[k:N,k] with literal zeros
        else:
            t = sqrt(R[k,k])
            copy R[k+1:N,k] to L[k+1:N,k]
            divide copied words by t; L[k,k] = t
            save c = R[:,k] and s = R[k,:]
            a = literal(-1) / R[k,k]
            for j = 0,...,N-1:
                b = a * s[j]
                for i = 0,...,N-1:
                    v = b * c[i]
                    R[i,j] = R[i,j] + v
    release scoped scratch
```

PSD residual diagonals are nonnegative, so maximum absolute diagonal agrees with maximum diagonal. Ties select the first available index. Every step runs, including zero-pivot steps; there is no tolerance or early rank truncation. A zero pivot performs no division. At $N=0$ the raw body reads no operands, allocates nothing and leaves memory unchanged.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

Exact decoded scalar arithmetic (`ExactModel` and `IsScalar`) is combined with exact comparison, dimension-literal and bounded stored-index contracts. The declared domain is the original PSD input, including singular matrices and the zero matrix. Factor and log output buffers are separate; the declared interface preserves the source.

## Operations and Storage

::: theorem decl:NLAlib.Cholesky.PivotedCertification.eval_countPoly_program name="Pivoted scalar instruction work"
The evaluated tree polynomial is
$$W(N)=22N^3+283N^2+504N+60.$$
It bounds work and sequential span in the scalar/index model, including actual diagonal scans, index reads, symmetric exchanges, arithmetic and structural instructions.
:::

::: theorem decl:NLAlib.Cholesky.PivotedCertification.staticPeak_program_le name="Scratch and caller capacity"
Additional scratch is at most $N^2+2N+4$ scalar cells. Caller source, blank factor and blank pivot log add $2N^2+N$, giving total resident allowance $3N^2+3N+4$. Scratch is scoped; these are abstract cell bounds rather than bytes or hardware performance estimates.
:::

## Accuracy

::: theorem decl:NLAlib.Cholesky.PivotedCertification.algorithm_checked name="Exact PSD factor and actual pivot log"
Every admitted PSD input is factored successfully under the local exact contracts. The actual log gives $p_k\in\{k,\ldots,N-1\}$, the first maximal current residual diagonal at step $k$. Starting with the identity ordering, successively exchange positions $k,p_k$; write the final ordering as $\sigma$. The actual output is the canonical Cholesky factor of $\mathbf B$, where $B_{ij}=A_{\sigma(i),\sigma(j)}$. Equivalently, for $P_{i,\sigma(i)}=1$,
$$\mathbf P\mathbf A\mathbf P^{\mathsf T}=\mathbf L\mathbf L^{\mathsf T}.$$
The factor is lower triangular with nonnegative diagonal and literal upper zeros. Source and buffer extents are retained, tape position is restored and scratch is released. No computed-pivot or successful-run premise is assumed.
:::

## Not yet presented

This full exact factorization certificate does not supply a tolerance-driven low-rank stopping rule or a rounded execution guarantee.
