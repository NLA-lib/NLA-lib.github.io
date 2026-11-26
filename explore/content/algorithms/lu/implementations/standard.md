---
uid: a3ce44c0-c010-5c89-92ae-a0bc3dac2aee
kind: implementation
id: standard
algorithm: lu
title: Unpivoted elimination
summary: Stored scalar Gaussian elimination with original nonzero Gaussian pivots.
status: ready
implementation_declarations:
- NLAlib.LU.factor
- NLAlib.LU.step
- NLAlib.LU.materializeColumn
- NLAlib.LU.schurStep
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

The input is an $N\times N$ real matrix in column-major storage, with entry $(i,j)$ at offset $jN+i$. The source is read only. The caller supplies separate blank $N^2$-cell lower and upper output buffers; all residual and temporary buffers are scoped scratch. The routine copies the source before zero-filling the factors. Buffer capacity, liveness, and separation are part of the stored-execution contract.

The routine `NLAlib.LU.factor` performs:

```text
R = copy(A); L = zeros(N,N); U = zeros(N,N)
for k = 0,...,N-1:
    scalar_step(k)
return L,U
```

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


::: theorem decl:NLAlib.LU.Certification.eval_countPoly_program name="Instruction work and span"
The actual program's instruction polynomial evaluates to
$$W(N)=22N^3+141N^2+241N+46.$$
:::

::: theorem decl:NLAlib.LU.Certification.staticPeak_program_le name="Additional scratch"
Additional scratch is at most $N^2+2N+3$ cells. The caller supplies $3N^2$ resident cells, including all blank outputs.
:::

::: theorem decl:NLAlib.LU.Certification.algorithm_checked name="Exact stored-program certificate"
Under exact arithmetic, the concrete boxed `Algorithm` checks its specification, work, confinement, and additional-space bounds on its declared original-input domain. This certificate accounts for the actual program and its input/output capacities.
:::

## Accuracy

::: theorem decl:NLAlib.LU.factor_meets name="Canonical unpivoted factors"
Assume every **original canonical Gaussian pivot** is nonzero:
$\texttt{gaussState}(A,k)_{kk}\ne0$ for every $k<N$.
The actual outputs equal $\texttt{luLower}(A)$ and $\texttt{luUpper}(A)$.
:::

::: theorem decl:NLAlib.LU.Certification.isLU_of_factorSpec_post name="Reconstruction"
Under this same original-input pivot condition, the certified output is unit lower triangular and upper triangular and satisfies $A=LU$.
:::

The condition is vacuous at $N=0$, and the output factors are empty. Singular positive-order inputs are outside this certificate's domain, even though the scalar zero-pivot branches are defined.

## Not yet presented

This page offers the reviewed exact model. A rounded guarantee for this unpivoted listing is not curated here.
