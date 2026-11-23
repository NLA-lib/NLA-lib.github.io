---
kind: implementation
id: dense-schur
algorithm: qr-iteration
title: BGS + Dense Schur (end-to-end)
summary: For any dense complex matrix, a computed Schur pair with exactly triangular T, backward and orthogonality bounds, polylogarithmic bits, a counted run and a verified single-shot form.
status: ready
library_algorithm: dense-schur
library_results: false
arithmetic_models:
- id: bgs-iii-program
  arithmetic: standard
  program: bgs-iii-small-block
- id: any-small-block
  arithmetic: standard
  program: any-small-block
search_aliases:
- dense Schur
- Schur decomposition
- end-to-end eigensolver
- Dense Schur solver
- Schur form of a general matrix
- Verified Schur solver
---

**The guarantee** (`NLAlib.Schur.denseSchur_measureReal_not_schur_le`, [stated in full below](#accuracy)). For **any** $\mathbf A\in\mathbb C^{(n+1)\times(n+1)}$, any $0<\delta\le1$ and $0<\varphi\le1$, at a unit roundoff $u\le u_0(n,\delta,\varphi)$, the program `denseSchur` stores, with probability at least $1-\varphi$ over its random tape, a computed $\widehat{\mathbf U}$ and an **exactly upper triangular** $\widehat{\mathbf T}$ with

$$\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\delta\|\mathbf A\|_2,\qquad\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru\le\delta.$$

There is no hypothesis on $\mathbf A$: it need not be Hessenberg, diagonalizable or well conditioned, and no bound on its norm is supplied. $R$ is an explicit count of the rotations accumulated on $\widehat{\mathbf U}$. On **every** tape the run terminates and the orthogonality bound holds; only the backward bound carries the probability. The diagonal of $\widehat{\mathbf T}$ lists the eigenvalues of a matrix within $2\delta\|\mathbf A\|_2$ of $\mathbf A$.

| | |
| --- | --- |
| Bits | $\log_2(1/u_0)\le c_1L^4(\log_2L+1)^2+c_2$, with $L=\log_2\frac{4(n+1)}{\delta\varphi}$ |
| Work | At most $C(n+1)^3L^9(\log_2L+1)^6$ instructions, on every tape, that is $O(n^3L^9(\log L)^6)$ |
| Certificate | One counted run, with no oracle: [`denseSchurAlgorithm`](#certificate) |
| Verified form | On every tape, flag $0$ implies the guarantee; $\mathbb P[\text{flag}\ne0]\le\varphi$: [the verified solver](#verified-every-tape) |

**Relation to the papers.** This solver builds on the finite-precision shifted QR of [BGS II](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/) and the small-block program of [BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/). It goes beyond them: those papers compute eigenvalues only, while this program also computes the Schur vectors and proves the Schur form.

## Algorithm

The program scales the matrix, regularizes it by a small Gaussian perturbation, reduces it to Hessenberg form, runs shifted QR with accumulation, and scales back.

```text
input: A of order N = n + 1; parameter words P, computed from (n, delta, phi)
s := fl(||A||_F)
if s is not positive:                      (only A = 0)
    U := I; Fl := 0; stop
A := fl(A * fl(1 / s))
A := A + fl(gamma / sqrt N) G              G complex Gaussian, from the Gaussian stream
U := I
(A, U) := Hessenberg reduction of A, with its rotations replayed on U
(A, U, Fl) := rounded shifted QR in Schur mode on (A, U), with a small-block Schur solver
A := fl(s A)
output: T^ in the matrix buffer, U^, the flag Fl
```

The parameter words depend only on $(n,\delta,\varphi)$. They are supplied as exact reals, and their computation is not charged. Complex entries are stored as adjacent real and imaginary words. The supplied buffers are the matrix ($2(n+1)^2$ words, overwritten by $\widehat{\mathbf T}$), the parameter words, the accumulator ($2(n+1)^2$ words, written with $\widehat{\mathbf U}$) and the one-word flag.

The internal parameters are $\delta'=\delta/(16\sqrt{n+1})$ for the regularizer and the core, a class $(B,\Gamma)$ reached by the regularizer, the class $(2B,\Gamma/2)$ and norm bound $8$ for the core, its shift degree $k$, iteration cap $F$ and small-block loop cap $T$. The rotation count is

$$R=(n+1)^2+2(n+1)\bigl(F(k+1+n_p)\,k(n+1)+2k(k+2)\bigr)+(n+1)R_L,$$

with $n_p$ the core's words after its threshold and $R_L$ the count of one call of the small-block solver.

### Stages

Each stage is a routine parameter of the pipeline `schurPipelineWith` with its own contract. A different routine that meets a contract can replace the stage.

| Stage | Routine in `denseSchur` | Contract | What the stage provides here |
| --- | --- | --- | --- |
| Norm estimate | `frobNormStage` | `FrobNormEstimateContract` | $\tfrac12\|\mathbf A\|_{\mathsf F}\le s\le2\|\mathbf A\|_{\mathsf F}$ |
| Regularizer | `ginibrePerturb` | `RandomRegularizerContract` | Error $\delta'/2$, failure $3\varphi/8$, output in the class $(B,\Gamma)$ |
| Hessenberg reducer | `hessenbergReduceQ` | `HessenbergReducerContract` | Accumulator error $27(n+1)^2u$, backward error $50(n+1)^2u$ relative to the norm |
| Schur core | `roundedShQRSchurWith L` ([BGS II](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/)) | `RandomSchurCoreContract` | Backward error $\delta'$, failure $\varphi/2$, accumulator error $(1+24u)^{R_c}-1$ |
| Small-block solver `L` | `smallEigProg` ([BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/)) | `RandomSchurLeafContract` | Schur pair of a block of order at most $k$ and norm at most $32$ |

::: theorem decl:NLAlib.Schur.schurPipelineWith_measureReal_not_schur_le name="Any stages that meet their contracts compose" id=swappable-stages
Let a norm estimate with constants $c_1,c_2$, a regularizer with error $\delta_R$ and failure $\varphi_R$ into a class $C$, a reducer with errors $(\varepsilon_{H,U},\varepsilon_{H,T})$, and a Schur core from a class $C'$ with errors $(\varepsilon_{C,U},\varepsilon_{C,T})$ and failure $\varphi_C$ meet their contracts, the regularizer on norms at most $2/c_1$ and the core on norms at most $4/c_1$. Let the reducer's similarity carry $C$ into $C'$. Put $\varepsilon=(1+\varepsilon_{H,U})(1+\varepsilon_{C,U})-1$, and assume $c_1>0$, $8(n+1)u\le1/4$, $\delta_R\le1/c_1$, $0\le\varepsilon_{H,T}\le1/8$, $\varepsilon_{H,U},\varepsilon_{C,U}\ge0$, $\varepsilon\le1/16$ and $\varphi_R,\varphi_C\ge0$. Then, except with probability $\varphi_R+\varphi_C$, the pipeline stores the flag $0$ and a Schur output of $\mathbf A$ with

$$\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\Bigl(2c_2\sqrt{n+1}\bigl(\delta_R+3\varepsilon_{H,T}/c_1+\varepsilon_{C,T}+8\varepsilon/c_1\bigr)+8(n+1)u\Bigr)\|\mathbf A\|_2,$$

$$\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le2\varepsilon+\varepsilon^2.$$
:::

The certificate from component data, `schurPipelineAlgorithm`, has work and span equal to the sum of the stages' work bounds and a glue term $128(n+2)^2$, so a swapped stage swaps its cost term.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

Both models have the same machine: the standard model with unit roundoff $u$ and no overflow or underflow, exact natural literals up to $n+1$, exact index operations and comparisons, and draws that store the tape entry. The tape has a stream $s_U$ uniform on $[0,1]$, read by an exact polar disk sampler, and a stream $s_G$ with the standard real Gaussian law. The interpretation is measurable and reads the tape only in the windows of its calls.

::: model bgs-iii-program
**The small-block solver is the [BGS III program](/explore/algorithms/inverse-iteration/implementations/small-eig/).** The operation model has no eigenvalue kernel. The random-matrix tails the analysis needs are proved in the library ([pseudospectral shattering](/explore/theory/pseudospectral-shattering/)), so no hypothesis on them appears.

**Precision.** $u\le u_0$ = `uDenseSchur`$(n,\delta,\varphi)$, an explicit minimum of nine terms. There are absolute constants $c_1,c_2$ with

$$\log_2\frac1{u_0}\le c_1L^4(\log_2L+1)^2+c_2,\qquad L=\log_2\frac{4(n+1)}{\delta\varphi}.$$

The constants are not stated in closed form (`logb_inv_uDenseSchur_le`).
::: end-model

::: model any-small-block
**The small-block solver is a routine parameter `L`.** The program is `denseSchurWith sG L`. Its contract (`RandomSchurLeafContract`) is a hypothesis: on blocks of order at most $\min(k,n+1)$ and norm at most $32$, with twelve parameter words and the cap $T$, except with probability $\varphi_L$ it stores an upper triangular $\mathbf T_b$ and an accumulator $\mathbf U_b$ with $\mathbf T_b=\mathbf V_b^{\mathsf H}(\mathbf B+\mathbf F)\mathbf V_b$, $\|\mathbf F\|_2\le\beta_L$ and $\|\mathbf U_b-\mathbf V_b\|_2\le\varepsilon_L$ for an exact unitary $\mathbf V_b$. The theorem assumes $0\le\beta_L\le$ `denseSchurLeafAccuracy`, $0\le\varphi_L\le$ `denseSchurLeafFailure` and $0\le\varepsilon_L\le(1+24u)^{R_L}-1$.

**Precision.** $u\le$ `uDenseSchurWith`$(n,\delta,\varphi,n_p,R_L)$, an explicit minimum of eight terms. The bit bound above is stated for the BGS III solver only.
::: end-model

## Operations and Storage

Work counts instructions: every scalar operation, comparison, index operation, draw, address computation, loop control and allocation costs one unit of work and span. The bounds hold on every tape. Budget, scratch and resident memory are bounded by the static count of the program; this page gives no closed formula for them.

::: model bgs-iii-program
::: definition decl:NLAlib.Schur.denseSchurAlgorithm name="Certificate of the dense Schur solver" id=certificate
The fixed program, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the accumulator and the flag. At the sizes $(n,n_r,n_q,k,F,T)$ its work and span are at most `denseSchurWork`,

$$120(n+1)^2+201(n+1)^2+2998(n+1)^3+380748(n+1)^3(k+1)^4(n_r+n_q+1)(F+1)(T+1)^2+128(n+2)^2.$$

The terms are the norm estimate, the regularizer, the reduction, the core with its small-block solver, and the glue. The parameter words are supplied and their computation is not charged.
:::

The instrumented static count of the program is at most $384547(n+1)^3(k+1)^4(n_r+n_q+1)(F+1)(T+1)^2$ (`denseSchur_work_le`). At the parameters of the solver it is at most $C(n+1)^3L^9(\log_2L+1)^6$ (`denseSchur_work_le_polylog`), with $L$ as above and an absolute constant $C$ that is not stated in closed form.
::: end-model

::: model any-small-block
The library states no closed work bound for a general `L`. The certificate from component data adds the work bound supplied for each stage, as described under [the stages](#swappable-stages).
::: end-model

## Accuracy

::: model bgs-iii-program
::: theorem result:dense-schur-backward-error name="The dense Schur theorem" id=accuracy
Let the machine and the streams be as above, $0<\delta\le1$, $0<\varphi\le1$ and $u\le u_0$. For every complex $\mathbf A$ of order $n+1$, start `denseSchur` from a memory holding $\mathbf A$ and the words of `denseSchurParams`. Then the probability is at most $\varphi$ that the run fails, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ and $\widehat{\mathbf U},\widehat{\mathbf T}$ with $\widehat{\mathbf T}$ upper triangular,

$$\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\delta\|\mathbf A\|_2\quad\text{and}\quad\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru.$$

Here $R$ is `denseSchurRotations`, and $58Ru\le\delta$.
:::

::: theorem decl:NLAlib.Schur.denseSchur_terminates name="Termination and orthogonality on every tape" id=every-tape
On the same machine, for $0<\delta\le1$, any $\varphi$, every $\mathbf A$ and $u\le u_0$, the run succeeds on **every** tape, writes only $\mathbf A$, $\widehat{\mathbf U}$ and the flag, and stores $\widehat{\mathbf U}$ with $\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru$.
:::

::: theorem result:dense-schur-eigenvalues name="Corollary: eigenvalues" id=eigenvalues
Under the hypotheses of the dense Schur theorem, except with probability at most $\varphi$, the run stores the flag $0$ and an upper triangular $\widehat{\mathbf T}$ whose diagonal lists the eigenvalues, with multiplicity, of $\mathbf A+\mathbf E$ for some $\|\mathbf E\|_2\le2\delta\|\mathbf A\|_2$.
:::

::: theorem result:dense-schur-exact-unitary name="Corollary: an exact unitary" id=exact-unitary
Under the same hypotheses, except with probability at most $\varphi$, the run stores the flag $0$, $\widehat{\mathbf U}$ and an upper triangular $\widehat{\mathbf T}$, and there is an exact unitary $\mathbf V$ with

$$\mathbf A+\mathbf E=\mathbf V\widehat{\mathbf T}\mathbf V^{\mathsf H},\qquad\|\widehat{\mathbf U}-\mathbf V\|_2\le58Ru,\qquad\|\mathbf E\|_2\le2\delta\|\mathbf A\|_2.$$
:::

::: theorem result:dense-schur-certificate-accuracy name="On one counted run" id=one-run
Under the hypotheses of the dense Schur theorem, the probability is at most $\varphi$ that the counted run of `denseSchurAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ and a Schur pair with the two bounds of that theorem. The work and span bound is `denseSchurWork`.
:::
::: end-model

::: model any-small-block
::: theorem result:dense-schur-small-block-oracle name="The dense Schur theorem with any small-block solver" id=accuracy-any-leaf
Let the machine and the streams be as above, $0<\delta\le1$, $0<\varphi\le1$, let `L` meet the small-block contract with $\beta_L,\varphi_L,\varepsilon_L$ in the ranges above, and let $u\le$ `uDenseSchurWith`. For every complex $\mathbf A$ of order $n+1$, from a memory holding $\mathbf A$ and the words of `denseSchurParamsWith` with the solver's twelve words, the probability is at most $\varphi$ that `denseSchurWith sG L` fails, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ and $\widehat{\mathbf U},\widehat{\mathbf T}$ with $\widehat{\mathbf T}$ upper triangular,

$$\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\delta\|\mathbf A\|_2\quad\text{and}\quad\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru,$$

with $R$ = `denseSchurRotationsWith` at the solver's $R_L$.
:::
::: end-model

### The verified solver

The theorems above are Monte Carlo: on a bad tape the run may store the flag $0$ with an inaccurate pair. A Schur form can be checked afterwards, so the library also proves a verified solver, `verifiedSchurWith Solve`. It copies $\mathbf A$, runs the Schur solver `Solve`, and then runs the residual check `schurResidualCheck` on the copy and the output. **On every tape, the flag $0$ implies the accuracy guarantee. Only the chance of a nonzero flag is probabilistic.** The solver runs once: the library proves no retry loop.

The check takes a tolerance $\theta$ and a guard word $\kappa$. It overwrites the strict lower triangle of $\widehat{\mathbf T}$ with exact zeros, computes $\mathbf D=\mathrm{fl}(\mathbf A-\mathrm{fl}(\mathrm{fl}(\widehat{\mathbf U}\widehat{\mathbf T})\widehat{\mathbf U}^{\mathsf H}))$, and estimates the Frobenius norms $\hat r,\hat a,\hat w,\hat t$ of $\mathbf D,\mathbf A,\widehat{\mathbf U},\widehat{\mathbf T}$. With the guard $\hat g=\mathrm{fl}(\mathrm{fl}(\mathrm{fl}(\hat w\hat w)\hat t)\kappa)$, it stores the flag $0$ if $\mathrm{fl}(\hat r+\hat g)\le\mathrm{fl}(\hat a\theta)$ and $1$ otherwise. The guard covers the rounding of the check itself. The check costs at most $1619(n+1)^3$ instructions.

::: theorem decl:NLAlib.Schur.verifiedSchurWith_writes name="The check works with any Schur solver" id=verified-any-solver
Let `Solve` be any routine that, from every input memory and on every tape, terminates, writes only $\mathbf A$, $\widehat{\mathbf U}$ and the flag, and stores a matrix and an accumulator with $\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le e_U$. On a machine in the standard model with index literals and exact comparisons, let $64(n+2)^3u\le1$, $\kappa\ge32(n+2)^2u$, $\theta\ge0$ and $2\theta\sqrt{n+1}\le\delta$. Then for every $\mathbf A$, on **every** tape, `verifiedSchurWith Solve` terminates, writes only $\mathbf A$, $\widehat{\mathbf U}$ and the flag, keeps the orthogonality bound and stores the flag $0$ or $1$. If the flag is $0$, then $\widehat{\mathbf T}$ is upper triangular and

$$\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\delta\|\mathbf A\|_2.$$
:::

::: theorem decl:NLAlib.Schur.verifiedSchurWith_measureReal_not_flag_le name="An accurate solver passes the check" id=verified-passes
On that machine, with a measurable interpretation that reads the tape only in its windows, let $64(n+2)^3u\le1$, $0\le\kappa\le64(n+2)^2u$, $4096(n+2)^3u\le\theta\le1$, $e_U\le1/2$ and $\sqrt{n+1}\,\delta'\le\theta/8$. Let `Solve` end, from every input memory and except with probability at most $\varphi$, in a measurable postcondition that implies a Schur output of $\mathbf A$ with errors $\delta',e_U$, survives rewriting the flag to $0$ and survives the release of scratch. Then the probability is at most $\varphi$ that `verifiedSchurWith Solve` fails, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ with that postcondition.
:::

::: model bgs-iii-program
**The instance.** The program `verifiedSchur` is `verifiedSchurWith (denseSchur sG)`. It runs the dense solver at the internal accuracy $\delta_{\mathrm{int}}=\delta/(16(n+1))$, with $\theta=\delta/(2\sqrt{n+1})$ and $\kappa=32(n+2)^2u$, so one parameter word depends on the machine's unit roundoff. The precision threshold is

$$u\le u_{\mathrm{ver}}=\min\Bigl(u_0(n,\delta_{\mathrm{int}},\varphi),\ \frac{\theta}{4096(n+2)^3}\Bigr)\qquad(\texttt{uVerifiedSchur}).$$

::: theorem result:verified-schur-every-tape name="Verified solver: flag 0 implies accuracy, on every tape" id=verified-every-tape
Let the machine be as above, $0<\delta\le1$, any $\varphi$ and $u\le u_{\mathrm{ver}}$. For every complex $\mathbf A$ of order $n+1$, from a memory holding $\mathbf A$ and the words of `verifiedSchurParams`, on **every** tape the run of `verifiedSchur` terminates, writes only $\mathbf A$, $\widehat{\mathbf U}$ and the flag, stores the flag $0$ or $1$ and has $\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru$, with $R$ = `denseSchurRotations` at $\delta_{\mathrm{int}}$. If the flag is $0$, then $\widehat{\mathbf T}$ is upper triangular and $\|\mathbf A-\widehat{\mathbf U}\widehat{\mathbf T}\widehat{\mathbf U}^{\mathsf H}\|_2\le\delta\|\mathbf A\|_2$.
:::

::: theorem result:verified-schur-failure name="Verified solver: the flag is nonzero with probability at most φ" id=verified-failure
Let the machine and the streams be as in the dense Schur theorem, $0<\delta\le1$, $0<\varphi\le1$ and $u\le u_{\mathrm{ver}}$. For every complex $\mathbf A$ of order $n+1$, the probability is at most $\varphi$ that the run fails, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ and a Schur pair with backward error $\delta_{\mathrm{int}}\|\mathbf A\|_2$ and $\|\widehat{\mathbf U}^{\mathsf H}\widehat{\mathbf U}-\mathbf I\|_2\le58Ru$. In particular $\mathbb P[\text{flag}\ne0]\le\varphi$.
:::

::: definition decl:NLAlib.Schur.verifiedSchurAlgorithm name="Certificate of the verified solver" id=verified-certificate
The fixed program `verifiedSchurProgram`, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the accumulator and the flag. Its every-tape claim is the flag-conditional Schur form. At the sizes $(n,n_r,n_q,k,F,T)$ its work and span are at most `verifiedSchurWork`,

$$384547(n+1)^3(k+1)^4(n_r+n_q+1)(F+1)(T+1)^2+1619(n+1)^3+32(n+1)^2+128.$$
:::

::: theorem result:verified-schur-certificate name="Verified solver, on one counted run" id=verified-one-run
Under the hypotheses of the failure bound, the probability is at most $\varphi$ that the counted run of `verifiedSchurAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside $\mathbf A$, $\widehat{\mathbf U}$ and the flag, or does not store the flag $0$ with a Schur output of $\mathbf A$.
:::
::: end-model

::: model any-small-block
The library instantiates the verified solver at the BGS III program. For another small-block solver, the two general theorems above apply once `denseSchurWith sG L` is shown to meet their hypotheses; the library does not state that instance.
::: end-model

## Not yet presented

- A bit bound for the verified threshold $u_{\mathrm{ver}}$; the bit bound above is for $u_0$.
- The formulas of the terms of the precision threshold $u_0$ that come from the regularizer, the core and the small-block solver, and of the parameter words.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling.
- A rounded Gaussian or disk sampler: the drawn values are exact.

## Mathematical method

{{ generated:mathematical-method }}
