---
kind: implementation
id: blocked
algorithm: cholesky
title: Blocked LU followed by square-root scaling
summary: Clipped scalar LU panels and packed matrix updates produce the lower factor, then each column is scaled by its pivot root.
status: ready
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
implementation_declarations:
- NLAlib.Cholesky.factorBlocked
- NLAlib.Cholesky.blockedWithScratch
- NLAlib.LU.blockedStep
- NLAlib.Cholesky.scaleLuColumns
- NLAlib.Cholesky.scaleLuColumn
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

`NLAlib.Cholesky.factorBlocked` receives $N$, positive block width $B$, and $Q=\lceil N/B\rceil=(N+B-1)/B$. It reads a real SPD matrix $\mathbf A$ and writes a square factor $\mathbf L$. Both caller matrices are column-major, with entry $(i,j)$ at $jN+i$.

```text
if N > 0:
    allocate temporary upper factor U[N*N]
    run the blocked scalar LU routine:
        copy A into a scoped residual R before output initialization
        fill L and U with literal zeros (unit diagonals are written by panel steps)
        for block h = 0,...,Q-1:
            start = h*B; width = min(B,N-start); stop = start+width
            for k = start,...,stop-1:
                materialize the lower column and upper row from R
                perform saved-operand panel elimination on the panel rectangles
            pack the lower and upper trailing rectangles
            multiply them with scalar matrix-product loops
            subtract that product from R[stop:N,stop:N]
        release residual and matrix-update workspaces
    for k = 0,...,N-1:
        t = sqrt(U[k,k])
        fill L[0:k,k] with literal zeros
        for i = k,...,N-1: L[i,k] = L[i,k] * t
    release U and root temporary
```

This implementation obtains a unit lower LU factor first and scales its columns. The panel's bottom-right residual correction is delayed until its packed matrix product. All matrix products are actual scalar loops. The last panel is clipped when $B$ does not divide $N$, and widths larger than $N$ are allowed. Copying precedes output writes, so the separate write theorem permits source/output overlap. At $N=0$ the raw body performs no operand frame, allocation or scalar call; the declared input still requires $B>0$ and $Q=0$.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The scalar interpreter satisfies `IsScalar` and `IsCmp`; its machine satisfies `ExactModel`. The original input is positive definite. That condition supplies all nonzero Gaussian pivots and all positive roots needed by the adapter.

## Operations and Storage

::: theorem decl:NLAlib.Cholesky.BlockedCertification.eval_countPoly_program name="Actual blocked-tree instruction polynomial"
With dimensions $(N,B,Q)$, the evaluated work polynomial is
$$
\begin{aligned}
W={}&44N+395BQ+180NB^2Q+180NB^2Q^2\\
 &+49B^2Q+49B^2Q^2+83N^2Q+22NQ\\
 &+33N^2BQ+187NBQ+215Q+44N^2+118.
\end{aligned}
$$
It bounds full scalar/index work and sequential span, including packing, arithmetic and structural instructions. Symbolic clipping produces a conservative bound; oversized blocks can make it loose. No BLAS throughput or elapsed-time claim follows from this count.
:::

::: theorem decl:NLAlib.Cholesky.BlockedCertification.staticPeak_program_le name="Blocked scratch storage"
Additional scoped scratch is at most $6N^2+2N+3$ abstract scalar cells, including the upper factor, blocked LU workspaces and root scaling temporary. Caller source and blank factor add $2N^2$, for total resident allowance $8N^2+2N+3$. These bounds include order zero.
:::

## Accuracy

::: theorem decl:NLAlib.Cholesky.BlockedCertification.algorithm_checked name="Exact blocked Cholesky certificate"
For every original real SPD input and valid block controls, the actual program succeeds and returns the canonical `choleskyLower` factor. The factor has positive diagonal and satisfies $\mathbf A=\mathbf L\mathbf L^{\mathsf T}$; its stored upper words are literal zeros. The declared interface preserves the source and every buffer extent, releases scratch and restores the tape position. This includes clipped final panels and empty matrices, without a supplied successful run.
:::

## Not yet presented

The rounded results on the ordinary right-looking page concern a different tree. This page exposes the reviewed exact blocked certificate.
