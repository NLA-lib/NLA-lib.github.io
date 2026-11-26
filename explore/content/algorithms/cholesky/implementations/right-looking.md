---
kind: implementation
id: right-looking
algorithm: cholesky
title: Right-looking scalar factorization
summary: A copied Gaussian residual supplies each Cholesky column and a full saved-pivot update.
status: ready
arithmetic_models:
- id: exact
  arithmetic: exact
  program: stored-scalar
- id: standard
  arithmetic: standard
  program: stored-scalar
- id: finite-range
  title: Guarded finite range with additive underflow
implementation_declarations:
- NLAlib.Cholesky.rightLooking
- NLAlib.Cholesky.rightWithScratch
- NLAlib.Cholesky.rightStep
- NLAlib.Cholesky.rightColumn
- NLAlib.LU.schurStep
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

`NLAlib.Cholesky.rightLooking` reads a real $N\times N$ matrix $\mathbf A$ and writes a square lower factor $\mathbf L$. Both buffers use column-major indexing: entry $(i,j)$ occupies word $jN+i$. The declared interface keeps the source unchanged; the common copy-first body also supports overlapping source and output in its separate write theorem.

```text
if N > 0:
    allocate residual R[N*N]
    copy A to R; fill L with literal zeros
    for k = 0,...,N-1:
        t = sqrt(R[k,k])
        copy R[k+1:N,k] to L[k+1:N,k]
        divide each copied word by t; L[k,k] = t
        save the full column c = R[:,k] and row r = R[k,:]
        a = literal(-1) / R[k,k]
        for j = 0,...,N-1:
            s = a * r[j]
            for i = 0,...,N-1:
                v = s * c[i]
                R[i,j] = R[i,j] + v
    release scoped scratch
```

The update touches the **whole residual**, including retired rows and columns. Products and sums are separate scalar calls. This evaluation order matters to the rounded bounds. Upper factor words stay at their initialized zero literals. At $N=0$ the raw body reads no operands, allocates nothing and leaves memory unchanged.

{{ generated:implementation-source }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

::: model exact
The scalar interpreter satisfies `IsScalar` and its machine satisfies `ExactModel`: decoded literals, roots, division, multiplication and addition are exact. The input domain is $\mathbf A\succ0$, including the empty matrix.
::: end-model

::: model standard
The same tree runs under `IsScalar` and `StdModel u`, which bounds each scalar primitive by relative error $u$. Require $0\le u\le1/10$, $0<\mu\le B$, $\mu\mathbf I\preceq\mathbf A$ and $\|\mathbf A\|_2\le B$. Define
$$
\rho_0=0,\qquad
\rho_{k+1}=\bigl(1+6B/\mu+2(B/\mu)^2\bigr)\rho_k+uB(2+80B/\mu).
$$
The additional input condition is $\rho_N<\mu/2$.

::: definition decl:NLAlib.choleskySchurErrorBound name="Propagated active-residual budget"
$\rho_k$ is the source-defined saved-pivot Schur error recurrence above.
:::
::: end-model

::: model finite-range
The interpreter satisfies `IsGuardedScalar` and the machine satisfies `MixedModel u τ`: on safe exact targets, each rounded result has absolute error at most $u|x|+\tau$. Unsafe targets may be rejected. The zero literal must decode to zero, and every $|x|\le\Omega$ must be safe. Require $\mu\mathbf I\preceq\mathbf A$ and $\|\mathbf A\|_2\le B$ together with the complete range conditions below.

Set $H=2B$, $m=\mu/2$, $\ell=1+u+\tau$, and
$$
C=(1+u)\ell/m+\tau,\quad T=(1+u)CH+\tau,\quad Q=(1+u)HT+\tau,
$$
$$
E_c=(u+\tau)/m+u\ell/m+\tau,\quad
E_t=HE_c+uCH+\tau,\quad E_q=HE_t+uHT+\tau,\quad
D=E_q+u(H+Q)+\tau.
$$
Define $\zeta_0=0$ and $\zeta_{k+1}=(1+6B/\mu+2(B/\mu)^2)\zeta_k+D$.

::: definition decl:NLAlib.Computation.CholeskyRangeConditions name="Input-only finite-range conditions"
Require $0\le u<1$, $\tau\ge0$, $0<\mu\le B$, $\zeta_N<\mu/2$, and $d=(1-u)\sqrt m-\tau>0$. All exact instruction targets fit the accepted range when
$$
1\le\Omega,\quad \ell/m\le\Omega,\quad CH\le\Omega,\quad HT\le\Omega,
\quad H+Q\le\Omega,\quad \sqrt H\le\Omega,\quad H/d\le\Omega.
$$
These sufficient inequalities depend only on the original input band, dimension and arithmetic parameters. They include the full residual, saved-row products, roots and normalized quotients.
:::

::: definition decl:NLAlib.choleskyMixedSchurErrorBound name="Full-residual mixed-error recurrence"
$\zeta_k$ is the recurrence above, retaining the additive allowance $\tau$ at every rounded instruction.
:::
::: end-model

## Operations and Storage

::: theorem decl:NLAlib.Cholesky.Certification.eval_countPoly_program name="Actual scalar instruction work"
The fixed tree has the evaluated instruction polynomial
$$W(N)=22N^3+115N^2+167N+56.$$
It bounds work and sequential span in the scalar/index resource model, including addressing, frames, queries and structural instructions. It is not a floating-point operation count or a wall-clock estimate. The program tree is the same for all three arithmetic models.
:::

::: theorem decl:NLAlib.Cholesky.Certification.staticPeak_program_le name="Additional scratch"
Additional scoped storage is at most $N^2+2N+3$ abstract scalar cells: the residual, two saved vectors and scalar temporaries. Caller source and blank factor capacities add $2N^2$ cells, giving total resident allowance $3N^2+2N+3$. These conservative bounds include order zero.
:::

## Accuracy

::: model exact
::: theorem decl:NLAlib.Cholesky.Certification.algorithm_checked name="Exact stored Cholesky certificate"
Every admitted positive-definite real input is factored successfully under the local exact arithmetic contracts. The actual output equals the canonical `choleskyLower` factor, is lower triangular with positive diagonal, and satisfies $\mathbf A=\mathbf L\mathbf L^{\mathsf T}$. Stored upper words are literal zeros. The source, all buffer extents and the tape position are retained; scratch is released. No successful-run or computed-pivot assumption is supplied.
:::
::: end-model

::: model standard
::: theorem decl:NLAlib.Cholesky.rightLooking_meets_relative name="Success and spectral residual under relative rounding"
Under the original input band and $\rho_N<\mu/2$, the actual tree succeeds. Put
$$e=\frac{2(1+B/\mu)\rho_N+16uB}{\sqrt\mu}.$$
The decoded output $\widehat{\mathbf L}$ is lower triangular, has positive diagonal and literal upper zeros, and satisfies the absolute spectral residual bound
$$\|\mathbf A-\widehat{\mathbf L}\widehat{\mathbf L}^{\mathsf T}\|_2
\le (Ne)(2\sqrt B+Ne).$$
The input conditions imply every required pivot margin; they do not assume a computed factor or successful trace.
:::
::: theorem decl:NLAlib.Cholesky.rightLooking_writes_relative name="Entrywise forward error of actual output words"
The same assumptions give $|\widehat L_{ij}-(\mathsf{choleskyLower}(\mathbf A))_{ij}|\le e$ for every entry, together with the off-output frame and restored tape position.
:::
::: end-model

::: model finite-range
::: theorem decl:NLAlib.Cholesky.rightLooking_meets_mixed name="Success and residual with finite range and underflow"
Under all stated guarded-machine and input range assumptions, the actual tree succeeds without rejected arithmetic. Put
$$
e=\frac{2(1+B/\mu)\zeta_N}{\sqrt\mu}
 +(u\sqrt H+\tau)\left(1+\frac H{d\sqrt m}\right)+\frac{uH}d+\tau.
$$
The actual lower factor has positive diagonal and literal upper zeros, with
$$\|\mathbf A-\widehat{\mathbf L}\widehat{\mathbf L}^{\mathsf T}\|_2\le(Ne)(2\sqrt B+Ne).$$
The corresponding write theorem also bounds each factor-entry forward error by $e$. All safety is derived from the original input inequalities.
:::

::: theorem decl:NLAlib.Cholesky.rightLooking_meets_binaryFinite name="Represented bounded-binary specialization"
For a binary format with at least two exponent bits and an integer rounding map with absolute error at most $1/2$, the represented finite-word machine instantiates this guarantee with $u=2^{-\mathrm{mantissaBits}}$ and $\tau=2^{\mathrm{minExponent}}/2$. Its interpreter rejects targets beyond `maxFinite`; require $\Omega\le\mathrm{maxFinite}$ and all preceding range conditions. This is a theorem about that mathematical binary-word backend, not a native IEEE execution guarantee.
:::
::: end-model

## Not yet presented

The library also has an in-place adapter and factor-based solve routines. Their interfaces and solve guarantees are not curated on this factorization page.
