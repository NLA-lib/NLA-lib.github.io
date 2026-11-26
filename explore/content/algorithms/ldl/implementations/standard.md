---
kind: implementation
id: standard
algorithm: ldl
title: Scalar LU followed by diagonal extraction
summary: Compute canonical Gaussian factors and copy the upper diagonal into the LDL pivot vector.
status: ready
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
implementation_declarations:
- NLAlib.LDL.factor
- NLAlib.LU.factor
- NLAlib.LU.step
- NLAlib.Ops.copyDiagonal
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

`NLAlib.LDL.factor` reads a real symmetric $N\times N$ matrix $\mathbf A$ and writes a square unit lower factor $\mathbf L$ and an $N$-word diagonal vector $\mathbf d$. Matrix buffers use column-major indexing, with $(i,j)$ at $jN+i$.

```text
if N > 0:
    allocate U[N*N]
    run the scalar LU factor routine:
        allocate R[N*N]; copy A to R
        fill both L and U with literal zeros
        for k = 0,...,N-1:
            write literal 1 to L[k,k]
            if R[k,k] == 0: fill L[k+1:N,k] with literal zeros
            else: copy R[k+1:N,k] to L[k+1:N,k] and divide by R[k,k]
            materialize U[k,k:N] from the residual pivot row
            if R[k,k] != 0:
                save c = R[:,k] and r = R[k,:]
                a = literal(-1) / R[k,k]
                for j = 0,...,N-1:
                    s = a * r[j]
                    for i = 0,...,N-1:
                        v = s * c[i]
                        R[i,j] = R[i,j] + v
        release R and saved-operand scratch
    for i = 0,...,N-1: copy U[i,i] to d[i]
    release U
```

The real scalar tree uses guarded normalization and Schur steps; the admitted input makes every pivot nonzero. LDL is obtained from the actual Gaussian factor outputs and a diagonal-copy loop. At $N=0$ the raw body reads no operands, allocates nothing and leaves all memory unchanged.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The interpreter satisfies exact scalar and comparison contracts (`IsScalar`, `IsCmp`); its machine satisfies `ExactModel`. The source must be symmetric and all **original canonical Gaussian pivots** must be nonzero:
$$G_0=\mathbf A,\qquad G_{k+1}=\mathsf{eliminationStep}(G_k,k),\qquad (G_k)_{kk}\ne0\quad(0\le k<N).$$
This is an input-only mathematical condition, not a premise about a computed execution. Indefinite matrices satisfying it are included. For $N=0$ the pivot condition is vacuous. A nonempty zero matrix is outside this program's certified domain.

## Operations and Storage

::: theorem decl:NLAlib.LDL.Certification.eval_countPoly_program name="Scalar LDL instruction work"
The evaluated instruction polynomial is
$$W(N)=22N^3+141N^2+255N+93.$$
It bounds abstract work and sequential span, including diagonal extraction, addressing, comparisons and structural instructions.
:::

::: theorem decl:NLAlib.LDL.Certification.staticPeak_program_le name="Additional scoped storage"
Scratch is bounded by $2N^2+2N+3$ scalar cells: the temporary upper factor, residual, two saved vectors and scalar temporaries. Caller source, blank lower factor and blank diagonal vector add $2N^2+N$, for total resident allowance $4N^2+3N+3$. These conservative bounds include order zero and describe the sequential scalar/index model.
:::

## Accuracy

::: theorem decl:NLAlib.LDL.Certification.algorithm_checked name="Exact Hermitian LDL certificate"
Every admitted real symmetric input is factored successfully. The actual lower output is canonical `luLower`, and $d_i=(G_i)_{ii}$ is the original Gaussian pivot. The decoded outputs satisfy
$$\mathbf A=\mathbf L\operatorname{diag}(\mathbf d)\mathbf L^{\mathsf T},$$
with $\mathbf L$ unit lower triangular and every $d_i\ne0$. Only the two declared outputs change. The source and all extents are preserved, scoped scratch is released and the tape position is restored. The certificate assumes neither an execution trace nor computed-factor correctness.
:::

## Not yet presented

This page presents the reviewed exact unpivoted program. Symmetric pivoting with $1\times1$ and $2\times2$ diagonal blocks and rounded LDL analysis need their own implementation connections.
