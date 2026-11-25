---
uid: 0a0a5104-3c54-5190-8069-fd563331d2d5
kind: implementation
id: rounded-shifted-qr
algorithm: qr-iteration
title: Finite precision (BGS II)
summary: The shifted QR program in rounded arithmetic with a random tape. It computes a Schur pair of a Hessenberg matrix, with any small-block Schur solver or with the BGS III program.
status: ready
library_algorithm: shifted-qr-rounded
library_results: false
arithmetic_models:
- id: any-small-block
  arithmetic: standard
  program: any-small-block
  aliases: [standard, small-eig-oracle]
- id: bgs-iii-program
  arithmetic: standard
  program: bgs-iii-small-block
  aliases: [small-eig-program]
search_aliases:
- Rounded shifted QR solver
- Finite-precision shifted QR
- Shifted QR without an oracle
- Rounded Hessenberg Schur form
---

The library certifies a shifted QR program for rounded arithmetic. It is a different program from the [exact-arithmetic program](/explore/algorithms/qr-iteration/implementations/shifted-qr/): scalar arithmetic is a machine in the standard model with unit roundoff $u$, terminal blocks are solved by a randomized small-block Schur solver, and the program draws shifts from a random tape. Its accuracy holds with a probability over the tape, not on every run. The analysis follows Theorem 6.3 of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR II*, which computes eigenvalues. The library's program computes a Schur form.

**The output is a Schur pair.** The matrix buffer ends holding an exactly upper triangular $\widehat{\mathbf{T}}$, and the accumulator buffer a computed $\widehat{\mathbf{U}}$. The eigenvalues are the diagonal of $\widehat{\mathbf{T}}$, a corollary of the Schur statement.

This page is one algorithm under two models, which differ in the small-block solver. In the **any small-block solver** model the solver is a routine parameter, and the theorem takes its contract as a hypothesis. In the **BGS III program** model it is the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/), a fixed program of scalar operations and draws, and no hypothesis on a solver or on random matrices remains. To start from a general matrix, see [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/), which uses this program as its core.

## Algorithm

The program is a deflation worklist. A block is split when one of its bottom $k$ subdiagonal entries is small; blocks of order at most the shift degree $k$ go to the small-block solver. Larger blocks go through the decoupling loop of Part II's Lemma 6.4, which alternates a randomized Ritz-value step, `Regularize`, with the shifting strategy $\mathrm{Sh}_{k,B}$. Every committed rotation is recorded in a log, so that it can be applied to the rest of the matrix and to the accumulator.

```text
input: H, upper Hessenberg of order N = n + 1; accumulator U; threshold word t; parameter words P
Fl := 0; push the block [0, N) on the worklist
repeat at most 2N rounds, while a block remains:
    pop a block of order d and copy it to the work matrix W
    if d <= k:
        (T_b, U_b) := small-block Schur solver on W
        store T_b at the block's position
        multiply the two coupling blocks and U by U_b
    else:
        decoupling loop, at most F rounds, recording its committed rotations in a log,
        until a bottom-k subdiagonal entry h of W has |h|^2 <= t_L:
            Regularize: Ritz values of the trailing k x k block, read from the diagonal of the
                small-block solver's T_b, each moved by an independent uniform sample of a small
                disk; return them if they pass the optimality test, otherwise try each as a
                degree-k shift in turn
            Sh_{k,B}: Find selects a promising shift r by binary search; take the rounded
                degree-k step with r if it contracts the potential psi_k by (1 - gamma);
                otherwise try the exceptional shifts of Exc around r, at a random
                translate of a disk net
        if the loop failed, or the scan of the bottom k entries against t finds none:
            Fl := 1; stop
        replay the log on the two coupling blocks and on U
        split W at the passing entry, write an exact 0 there, copy W back and push both blocks
if blocks remain after 2N rounds: Fl := 1
output: T^ in the matrix buffer, U^ in the accumulator buffer, the failure word Fl
```

The run is capped on every tape: the worklist by $2N$ rounds, the decoupling loop by $F$ rounds, every search by its length. A capped loop that has not finished writes the failure word. The exact zeros written at the cuts are what make $\widehat{\mathbf{T}}$ exactly upper triangular; the backward-error witness accounts for the discarded entries.

### Inputs and buffers

Complex entries are stored as adjacent real and imaginary words. The program is supplied five buffers:

| Buffer | On input | On output |
| --- | --- | --- |
| Matrix, $2(n+1)^2$ words | $\mathbf{H}$ | $\widehat{\mathbf{T}}$ (the input is overwritten) |
| Threshold, $1$ word | Deflation threshold $t$ | Unchanged |
| Parameters, $n_p$ words | Parameter words | Unchanged |
| Accumulator, $2(n+1)^2$ words | A stored matrix $\mathbf{U}_0$ | $\widehat{\mathbf{U}}$ |
| Failure, $1$ word | Any | $0$ on success |

Its sizes are the order $n+1$, the shift degree $k$, the number $n_p$ of parameter words, the iteration cap $F$ and the cap $T$ of the small-block solver's loops. The certificate below starts from $\mathbf{U}_0=\mathbf{I}$.

### Parameters

The caller chooses five reals: a condition bound $B\ge1$, a separation $\Gamma>0$, a norm bound $\Sigma$, a backward error $0<\delta\le\Sigma$ and a failure probability $0<\varphi\le1$. The library computes the rest from them; the parameter words are supplied as exact reals and their computation is not charged.

- The shift degree is $k=2^q$ for the least $q\ge1$ with $(4B)^{(8q+3)/(2^q-1)}\bigl(2(4B)^4\bigr)^{2/(2^q-1)}\le3$ (Part II's (eqn:setk) at $4B$). It satisfies $k=O(\log B\,\log\log B)$; at $B=1$ it is $128$.
- The decoupling threshold is $\omega=\min\bigl(\delta,\Gamma/(16(n+1)B)\bigr)/(12(n+1))$.
- The iteration cap is $F=\lceil\log(4\Sigma/\omega)/\log(1/0.8016)\rceil+1$, since each round of the loop decouples or contracts the potential by $1.002(1-\gamma)=0.8016$ at $\gamma=0.2$.
- The small-block solver must have backward error at most $\beta_0=4\Sigma\bigl(R/(16(2k+1)\Sigma)\bigr)^k$, which gives forward error $R=\omega^2/(8080\cdot4\Sigma)$ on its eigenvalues through the [Ostrowski–Elsner matching](/explore/theory/perturbation-theory/#ostrowski-elsner). $R$ is also the radius of the disk samples of `Regularize`. The solver's failure probability must be at most $\varphi_0=\varphi/(12F(n+1))$.

### Shape of the guarantee

In both models the conclusion has the same form. Except with probability $\varphi$ over the tape, the run sets the failure word to $0$, writes only the matrix, the accumulator and the failure word, and stores an upper triangular $\widehat{\mathbf{T}}$ and a $\widehat{\mathbf{U}}$ such that, for an exact unitary $\mathbf{W}$ and some $\|\mathbf{E}\|_2\le\delta$,

$$\widehat{\mathbf{T}}=\mathbf{W}^{\mathsf{H}}(\mathbf{H}+\mathbf{E})\mathbf{W},\qquad\|\widehat{\mathbf{U}}-\mathbf{U}_0\mathbf{W}\|_2\le\bigl((1+24u)^{R_{\mathrm{rot}}}-1\bigr)\|\mathbf{U}_0\|_2.$$

Here $R_{\mathrm{rot}}$ counts the rotations and rotation-equivalents accumulated on $\widehat{\mathbf{U}}$:

$$R_{\mathrm{rot}}=2(n+1)\bigl(F(k+1+n_p)\,k(n+1)+2k(k+2)\bigr)+(n+1)R_L,$$

where $R_L$ is the corresponding count of one call of the small-block solver. The guarantee is a backward error; a forward error for the eigenvalues needs a separate perturbation bound.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

Both models have the same machine: the standard model with unit roundoff $u$ and no overflow or underflow, exact natural literals up to $n+1$, exact index operations and comparisons. The disk sampler is exact: it reads a radius $R$ and two entries $(t_0,t_1)$ of a uniform stream and writes $R\sqrt{t_0}\,e^{2\pi i t_1}$. The interpretation is measurable and reads the tape only in the windows of its calls.

::: model any-small-block
**The small-block solver is a routine parameter `L`.** The program is `roundedShQRWith L`, and `roundedShQRSchurWith L` is the same program with the threshold as its first parameter word. The solver's contract (`RandomSchurLeafContract`) is a hypothesis: on every block $\mathbf{B}$ of order $d\le\min(k,n+1)$ with $\|\mathbf{B}\|_2\le4\Sigma$, reading twelve parameter words, it writes only the block and its accumulator and, except with probability $\varphi_L$, stores an upper triangular $\mathbf{T}_b$ and an accumulator $\mathbf{U}_b$ with

$$\mathbf{T}_b=\mathbf{V}_b^{\mathsf{H}}(\mathbf{B}+\mathbf{F})\mathbf{V}_b,\qquad\|\mathbf{F}\|_2\le\beta_L,\qquad\|\mathbf{U}_b-\mathbf{V}_b\|_2\le\varepsilon_L$$

for an exact unitary $\mathbf{V}_b$. The theorem assumes

$$0\le\beta_L\le\beta_0,\qquad0\le\varphi_L\le\varphi_0,\qquad0\le\varepsilon_L\le(1+24u)^{R_L}-1.$$

Any routine that meets this contract can be used, with its own $R_L$. The [BGS III program](/explore/algorithms/inverse-iteration/implementations/small-eig/) is one, and that instance is the other model of this page.

**Precision.** $u\le u_{\mathrm{ShQR}}$ (`uShQR`, the minimum of four named per-block terms) and $u\le u_{\mathrm{replay}}$ (`uShQRSchurReplay` at $R_L$), which keeps the replays, the leaf products and the leaf accumulators within a quarter of the error budget. The first term satisfies

$$\log_2\frac1{u_{\mathrm{ShQR}}}\le63\,k\log_2Y,\qquad Y=\frac{4(n+1)B\Sigma^2}{\delta\min(\Gamma,\Sigma)\varphi}.$$

The library states this with existential constants (`logb_inv_uShQR_le`); its proof takes $c_1=63$ and $c_2=0$. The replay term is the explicit quotient of the error budget by $16(n+1)\bigl(78\,n_sw+8(n+1)(k+2)+54R_L\bigr)\Sigma$, with $n_s=F(k+1+n_p)$ log slots of $w=k(n+1)$ entries.
::: end-model

::: model bgs-iii-program
**The small-block solver is the BGS III program.** The leaf and `Regularize` run the fixed program `smallEigProg` of [randomized shifted inverse iteration (BGS III)](/explore/algorithms/inverse-iteration/implementations/small-eig/) on the block. The operation model has no eigenvalue kernel. Its primitives are scalar arithmetic, index operations, comparisons, draws that store a tape entry, and the exact polar disk sampler. The tape has a second stream, $s_G$, with the standard real Gaussian law, from which the solver draws its Gaussian perturbations and directions. Twelve parameter words of the solver follow those of shifted QR, chosen for blocks of order at most $k$, norm at most $4\Sigma$, forward error $R$ and failure $\varphi_0$. Its rotation count is $R_L=k^2+2(k+1)\bigl((T+k)k+6\bigr)$ (`smallEigLeafRotations`).

The probability bounds of the solver need tails for the eigenvalue gap and the eigenvector condition number of a Ginibre perturbation $\mathbf{M}+\gamma n^{-1/2}\mathbf{G}$. The general theorems take them as hypotheses on two tail records. The library proves the records $(2048e,11/3,2/3,2)$ for the gap and $(128e,3,2,2)$ for the condition number, so the unconditional theorems below have no such hypothesis. See [pseudospectral shattering](/explore/theory/pseudospectral-shattering/).

**Precision.** $u\le u_0=\min(u_{\mathrm{ShQR}},u^{\mathrm{fwd}}_{\mathrm{SmallEig}},1/100,u_{\mathrm{replay}})$ (`uShQRSchur`), with the second term taken at the parameters above and the replay term at the $R_L$ above. For fixed tail records there are constants $e_1,e_2,e_3$ such that the first two terms, whose minimum is `uShQRSmallEig`, satisfy

$$\log_2\frac1{\min(u_{\mathrm{ShQR}},u^{\mathrm{fwd}}_{\mathrm{SmallEig}})}\le e_1k\log_2Y+e_2k^2\log_2^2Y+e_3,\qquad Y=\frac{4(n+1)B\Sigma^2}{\delta\min(\Gamma,\Sigma)\varphi}.$$

The constants are not stated in closed form (`logb_inv_uShQRSmallEig_le`). With $k=O(\log B\log\log B)$ this is $O(\log^4Y)$ bits, up to a factor $(\log\log Y)^2$. The library has no separate bit bound for the replay term at this level. [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) bounds its entire threshold, replay term included.
::: end-model

## Operations and Storage

The work of a certificate counts instructions: every scalar operation, comparison, index operation, draw, address computation, loop control and allocation costs one unit of work and span. The bounds hold on every tape and every admitted input; they are read off the fixed program. The supplied buffers hold $2(n+1)^2+1+n_p+2(n+1)^2+1$ words. Budget, scratch and resident memory are bounded by the static count of the program; this page gives no closed formula for them.

::: model any-small-block
The cost of the program depends on the solver `L`, and the library has no certificate for a general `L` at this level. [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/#swappable-stages) describes how a swapped stage swaps its cost term in the pipeline's certificate.
::: end-model

::: model bgs-iii-program
{{ statement:nlalib-shiftedqr-shqrsmalleigalgorithm-dfd2780d }}

The cap $T$ is the largest loop count of the solver, a logarithm of $k\Sigma/(\delta\varphi)$ up to constants. The monomial is an envelope of the paper's count of order $n^4+n^3\log^2$, not its shape.
::: end-model

## Accuracy

::: model any-small-block
{{ statement:shifted-qr-rounded-schur-any-leaf }}

{{ statement:nlalib-shiftedqr-roundedshqrwith-measurereal-not-spectrum-le }}

With a solver that completes on every tape, the program terminates on every tape, with no rounding model (`roundedShQRWith_terminates`).
::: end-model

::: model bgs-iii-program
{{ statement:nlalib-shiftedqr-roundedshqrschur-measurereal-not-schur-le }}

This statement keeps the tail records as hypotheses, and the proved records `ginibreGapTail` and `ginibreConditionTail` satisfy them. The corollaries below are stated at those records.

{{ statement:shifted-qr-rounded-small-eig-backward-error }}

The general form, `roundedShQRSmallEig_measureReal_not_spectrum_le`, takes the gap and condition tails as hypotheses on records $c_1,c_2$, so that other records can be used. The run terminates on every tape (`roundedShQRSmallEig_terminates`), with no unit roundoff, class or random-matrix hypothesis.

{{ statement:shifted-qr-rounded-small-eig-certificate-accuracy }}

The accepted output of this certificate is the eigenvalue statement. The Schur statement is the theorem on the program above; [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/#certificate) states the Schur form on one counted run.
::: end-model

## Not yet presented

- The formulas of the per-block precision terms of $u_{\mathrm{ShQR}}$ of $u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$ and of $u_{\mathrm{replay}}$, and the deflation threshold words $t$ and $t_L$. The page gives the bit counts instead.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- The relative-error forms (`roundedShQRSmallEig_relative` and its unconditional form) and the Hermitian corollaries at $B=1$, $k=128$ (`roundedShQRSmallEig_hermitian` and its unconditional form). They are in the Library.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling.
- A Hessenberg reduction of a general input: this program starts from an upper Hessenberg matrix. [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) adds it.

## Mathematical method

{{ generated:mathematical-method }}
