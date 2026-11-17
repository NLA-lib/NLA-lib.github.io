---
kind: implementation
id: rounded-shifted-qr
algorithm: qr-iteration
title: Finite precision (BGS II)
summary: The shifted QR program in rounded arithmetic with a random tape, with the small-eigenvalue solver either an oracle or the BGS III program.
status: ready
library_algorithm: shifted-qr-rounded
library_results: false
arithmetic_models:
- id: small-eig-oracle
  title: Standard rounding · SmallEig oracle
  aliases: [standard]
- id: small-eig-program
  title: Standard rounding · SmallEig = BGS III program
search_aliases:
- Rounded shifted QR solver
- Finite-precision shifted QR
- Shifted QR without an oracle
---

The library certifies a shifted QR program for rounded arithmetic. It is a different program from the [exact-arithmetic program](/explore/algorithms/qr-iteration/implementations/shifted-qr/): scalar arithmetic is a machine in the standard model with unit roundoff $u$, terminal blocks and Ritz values are computed by a randomized small-eigenvalue solver `SmallEig`, and the program draws shifts from a random tape. Its accuracy holds with a probability over the tape, not on every run. This is Theorem 6.3 of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR II*, with the quantifiers of their Theorem 1.4, corrected.

The page has two models, which differ in what `SmallEig` is. In the **SmallEig oracle** model it is a primitive of the operation model, specified by a contract (Part II's Definition 1.2) that the theorem assumes. In the **SmallEig = BGS III program** model it is the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/), a fixed program of scalar operations and draws, and the theorem has no oracle hypothesis.

## Algorithm

The program is a deflation worklist. A block is split when one of its bottom $k$ subdiagonal entries is small; blocks of order at most the shift degree $k$ are solved by `SmallEig`. Larger blocks go through the decoupling loop of Part II's Lemma 6.4, which alternates a randomized Ritz-value step, `Regularize`, with the shifting strategy $\mathrm{Sh}_{k,B}$.

```text
input: H, upper Hessenberg of order N = n + 1; threshold word t; parameter words P
Fl := 0; push the block [0, N) on the worklist
repeat at most 2N rounds, while a block remains:
    pop a block of order d and copy it to the work matrix W
    if d <= k:
        store SmallEig(W): d eigenvalues, in the output at the block's position
    else:
        decoupling loop, at most F rounds, until a bottom-k subdiagonal entry h of W
        has |h|^2 <= t_L:
            Regularize: Ritz values of the trailing k x k block by SmallEig, each moved by
                an independent uniform sample of a small disk; return them if they pass
                the optimality test, otherwise try each as a degree-k shift in turn
            Sh_{k,B}: Find selects a promising shift r by binary search; take the rounded
                degree-k step with r if it contracts the potential psi_k by (1 - gamma);
                otherwise try the exceptional shifts of Exc around r, at a random
                translate of a disk net
        if the loop failed, or the scan of the bottom k entries against t finds none:
            Fl := 1; stop
        split W at the passing entry, copy it back and push both blocks
if blocks remain after 2N rounds: Fl := 1
```

The run is capped on every tape: the worklist by $2N$ rounds, the decoupling loop by $F$ rounds, every search by its length. A capped loop that has not finished writes the failure word. Splitting discards the small subdiagonal entry logically; the backward-error witness accounts for it, and the entry's words stay in the matrix.

### Inputs and buffers

Complex entries are stored as adjacent real and imaginary words. The program is supplied five buffers:

| Buffer | Content |
| --- | --- |
| Matrix | The $2(n+1)^2$ words of $\mathbf H$, overwritten by the run |
| Threshold | One deflation threshold word $t$ |
| Parameters | $n_p$ parameter words |
| Output | Room for $2(n+1)$ words: the computed eigenvalues |
| Failure | One failure word |

Its sizes are the order $n+1$, the shift degree $k$, the number $n_p$ of parameter words and the iteration cap $F$, and in the second model also the cap $T$ of `SmallEig`'s loops.

### Parameters

The caller chooses five reals: a condition bound $B\ge1$, a separation $\Gamma>0$, a norm bound $\Sigma$, a backward error $0<\delta\le\Sigma$ and a failure probability $0<\varphi\le1$. The library computes the rest from them; the parameter words are supplied as exact reals and their computation is not charged.

- The shift degree is $k=2^q$ for the least $q\ge1$ with $(4B)^{(8q+3)/(2^q-1)}\bigl(2(4B)^4\bigr)^{2/(2^q-1)}\le3$ (Part II's (eqn:setk) at $4B$). It satisfies $k=O(\log B\,\log\log B)$; at $B=1$ it is $128$.
- The decoupling threshold is $\omega=\min\bigl(\delta,\Gamma/(16(n+1)B)\bigr)/(12(n+1))$.
- The iteration cap is $F=\lceil\log(4\Sigma/\omega)/\log(1/0.8016)\rceil+1$, since each round of the loop decouples or contracts the potential by $1.002(1-\gamma)=0.8016$ at $\gamma=0.2$.
- `SmallEig` must have forward error at most $R=\omega^2/(8080\cdot4\Sigma)$, the radius of the disk samples of `Regularize`, and failure probability at most $\varphi/(12F(n+1))$.

### Shape of the guarantee

In both models the event bounded by $\varphi$ is the same: the run fails, writes outside the matrix, the output and the failure word, or does not set the failure word to $0$ and store all eigenvalues, with algebraic multiplicity, of some $\mathbf H+\mathbf E$ with $\|\mathbf E\|_2\le\delta$. The guarantee is a backward error; a forward error for the eigenvalues needs a separate perturbation bound. A relative form with $\|\mathbf E\|_2\le\delta\|\mathbf H\|_2$ follows when $\|\mathbf H\|_2\le\Sigma\le c\|\mathbf H\|_2$.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

Both models have the same machine: the standard model with unit roundoff $u$ and no overflow or underflow, exact natural literals up to $n+1$, exact index operations and comparisons. The disk sampler is exact: it reads a radius $R$ and two entries $(t_0,t_1)$ of a uniform stream and writes $R\sqrt{t_0}\,e^{2\pi i t_1}$. The interpretation is measurable and reads the tape only in the windows of its calls.

::: model small-eig-oracle
**`SmallEig` is an oracle.** The operation model has two eigenvalue kernels, `SmallEig` and `Ritz`, and the program calls only `SmallEig`. Its contract (`IsRandomSmallEig`, Part II's Definition 1.2): at order $d$ it reads the $2d^2$ words of a matrix and a window of $W(d)$ entries of the uniform stream, and writes $2d$ words. There are measurable bad sets of windows, of probability at most $\varphi_{\mathrm{se}}$ at every upper Hessenberg input. Off the bad set, the output is within $\beta_{\mathrm{se}}$ of a listing of the eigenvalues with multiplicity. On the bad set, it may return any words. The theorem assumes

$$0\le\beta_{\mathrm{se}}\le R,\qquad0\le\varphi_{\mathrm{se}}\le\frac{\varphi}{12F(n+1)}.$$

The kernel's work, span and workspace are weights that the caller supplies, and they may be zero. The contract is realized separately by exact eigenvalues and by a tape law. That a single interpretation is both measurable and meets the contract is assumed, not exhibited: no small eigensolver is implemented in this model.

**Precision.** $u\le u_{\mathrm{ShQR}}$, the minimum of four named per-block terms (`uShQR`). The number of bits satisfies

$$\log_2\frac1{u_{\mathrm{ShQR}}}\le63\,k\log_2Y,\qquad Y=\frac{4(n+1)B\Sigma^2}{\delta\min(\Gamma,\Sigma)\varphi}.$$

The library states this with existential constants (`logb_inv_uShQR_le`); its proof takes $c_1=63$ and $c_2=0$. Since $k=O(\log B\log\log B)$, the bits are $O(\log B\,\log\log B\,\log Y)$.
::: end-model

::: model small-eig-program
**`SmallEig` is the BGS III program.** The leaf and `Regularize` run the fixed program `smallEigProg` of [randomized shifted inverse iteration (BGS III)](/explore/algorithms/inverse-iteration/implementations/small-eig/) on the block. The operation model has no eigenvalue kernel. Its primitives are scalar arithmetic, index operations, comparisons, draws that store a tape entry, and the exact polar disk sampler. The tape has a second stream, $s_G$, with the standard real Gaussian law, from which `SmallEig` draws its Gaussian perturbations and directions. Twelve parameter words of `SmallEig` follow those of shifted QR, chosen for blocks of order at most $k$, norm at most $4\Sigma$, forward error $R$ and failure $\varphi/(12F(n+1))$.

The probability bounds of `SmallEig` need tails for the eigenvalue gap and the eigenvector condition number of a Ginibre perturbation $\mathbf M+\gamma n^{-1/2}\mathbf G$. The general theorem takes them as hypotheses on two tail records, and the unconditional theorem below uses the records proved in the library, $(10000e,5,1/2,2)$ for the gap and $(128e,3,2,2)$ for the condition number. See [pseudospectral shattering](/explore/theory/pseudospectral-shattering/).

**Precision.** $u\le u_0=\min(u_{\mathrm{ShQR}},u^{\mathrm{fwd}}_{\mathrm{SmallEig}})$ (`uShQRSmallEig`), where the second term is taken at the parameters above. For fixed tail records there are constants $e_1,e_2,e_3$ with

$$\log_2\frac1{u_0}\le e_1k\log_2Y+e_2k^2\log_2^2Y+e_3,\qquad Y=\frac{4(n+1)B\Sigma^2}{\delta\min(\Gamma,\Sigma)\varphi}.$$

The constants are not stated in closed form (`logb_inv_uShQRSmallEig_le`). With $k=O(\log B\log\log B)$ this is $O(\log^4Y)$ bits, up to a factor $(\log\log Y)^2$.
::: end-model

## Operations and Storage

The work of both certificates counts instructions: every scalar operation, comparison, index operation, draw, address computation, loop control and allocation costs one unit of work and span. The bounds hold on every tape and every admitted input; they are read off the fixed program. The supplied buffers hold $2(n+1)^2+1+n_p+2(n+1)+1$ words. Budget, scratch and resident memory are bounded by the static count of the program; this page gives no closed formula for them.

::: model small-eig-oracle
::: definition decl:NLAlib.ShiftedQR.roundedShQRAlgorithm name="Certificate with the SmallEig oracle" id=certificate
Let the sizes $(n,k,n_p,F)$ be admitted: natural literals up to $n+1$ are exact on the machine, $k\le n$, and $k$, $n_p$ and $F$ are those of some parameter reals. Let the bad sets be measurable, $\beta\ge0$, and let the supplied kernel span be at most the supplied kernel work.

Then, on every admitted input, every interpretation that meets the model and every tape, the run of the fixed program succeeds within the static budget, scratch and memory of the program. Its work is at most

$$196218\,(n+1)^3(k+1)^3(n_p+1)(F+1)+8\,b^4\,\overline{w},\qquad b=n+k+n_p+F+2,$$

where $\overline{w}$ is the largest supplied kernel work over dimension lists of at most one entry, of size at most $b^2$. Its span satisfies the same bound with the supplied kernel span. The first term bounds the instructions; the second is at most $8b^4$ kernel calls at their largest weight. The run writes only the matrix, the output and the failure word.

Accuracy does not hold on every tape, even when the failure word is $0$: on a bad window `SmallEig` may return any words, and a terminal block stores them as its eigenvalues.
:::

The kernel weights are chosen by the caller, so this work bound is not a cost of the whole computation: it does not count the work of `SmallEig`.
::: end-model

::: model small-eig-program
::: definition decl:NLAlib.ShiftedQR.roundedShQRSmallEigAlgorithm name="Certificate with the BGS III program" id=certificate-small-eig
The fixed program `shqrSmallEigProgram`, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the output and the failure word. At the sizes $(n,k,n_p,F,T)$ its work and span are at most

$$675307\,(n+1)^3(k+1)^4(n_p+1)(F+1)(T+1)^2.$$

The instructions of `SmallEig` are among those counted: the bound covers the whole computation, apart from the parameter words, which are supplied.
:::

The cap $T$ is the largest loop count of `SmallEig`, a logarithm of $k\Sigma/(\delta\varphi)$ up to constants. The monomial is an envelope of the paper's count of order $n^4+n^3\log^2$, not its shape.
::: end-model

## Accuracy

::: model small-eig-oracle
::: theorem result:shifted-qr-rounded-backward-error name="Backward error with the SmallEig oracle" id=accuracy
Let $\mathbf H$ be upper Hessenberg of order $n+1$ with

- $\mathbf H\mathbf V=\mathbf V\operatorname{diag}(\mathbf d)$ for an invertible $\mathbf V$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le B$;
- $|d_i-d_j|\ge\Gamma>0$ for $i\ne j$;
- $\|\mathbf H\|_2\le\Sigma$, $0<\delta\le\Sigma$, $0<\varphi\le1$, and $k$ the shift degree at $4B$.

Let the machine and the sampler be as above, with $u\le u_{\mathrm{ShQR}}$. Let the interpretation meet the `SmallEig` contract on the uniform stream with $0\le\beta_{\mathrm{se}}\le R$ and $0\le\varphi_{\mathrm{se}}\le\varphi/(12F(n+1))$. Let the tape have independent entries with the stream laws, the uniform stream on $[0,1]$. Start the program `roundedShQR` from a memory holding $\mathbf H$, the threshold word and the parameter words. Then

$$\mathbb P\bigl[\text{the run fails, writes outside the matrix, the output and the failure word, or does not set the failure word to }0\text{ and store }\operatorname{spec}(\mathbf H+\mathbf E)\text{ for some }\|\mathbf E\|_2\le\delta\bigr]\le\varphi.$$
:::

The run terminates on every tape, with no numerical hypothesis (`roundedShQR_terminates`).

::: theorem result:shifted-qr-rounded-certificate-accuracy name="On one counted run, with the SmallEig oracle" id=one-run
Under the hypotheses of the certificate and of the theorem above, the probability is at most $\varphi$ that the counted run of the certificate's program fails, exceeds its budget, scratch or memory, has work or span above the certificate's bound, writes outside the matrix, the output and the failure word, or does not set the failure word to $0$ and store the eigenvalues of some $\mathbf H+\mathbf E$ with $\|\mathbf E\|_2\le\delta$.
:::
::: end-model

::: model small-eig-program
::: theorem decl:NLAlib.ShiftedQR.roundedShQRSmallEig_measureReal_not_spectrum_le_unconditional name="Backward error with the BGS III program, unconditional" id=accuracy-small-eig
Let $\mathbf H$ be upper Hessenberg of order $n+1$ with

- $\mathbf H\mathbf V=\mathbf V\operatorname{diag}(\mathbf d)$ for an invertible $\mathbf V$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le B$;
- $|d_i-d_j|\ge\Gamma>0$ for $i\ne j$;
- $\|\mathbf H\|_2\le\Sigma$, $0<\delta\le\Sigma$, $0<\varphi\le1$, and $k$ the shift degree at $4B$.

Let the machine and the sampler be as above, with $u\le u_0$ at the proved tail records, and let draws store the tape entry. Let the tape have independent entries, the stream $s_U$ uniform on $[0,1]$ and the stream $s_G$ standard real Gaussian. Start the program `roundedShQRSmallEig` from a memory holding $\mathbf H$, the threshold word and the parameter words. Then

$$\mathbb P\bigl[\text{the run fails, writes outside the matrix, the output and the failure word, or lists no }\operatorname{spec}(\mathbf H+\mathbf E)\text{ with }\|\mathbf E\|_2\le\delta\bigr]\le\varphi.$$

The theorem has no hypothesis on a small-eigenvalue solver and none on random matrices.
:::

The general form, `roundedShQRSmallEig_measureReal_not_spectrum_le`, takes the gap and condition tails as hypotheses on records $c_1,c_2$, so a sharper record plugs in. The proved gap exponent is $1/2$; the printed one is $2$. The run terminates on every tape (`roundedShQRSmallEig_terminates`), with no unit roundoff, class or random-matrix hypothesis.

::: theorem result:shifted-qr-rounded-small-eig-certificate-accuracy name="On one counted run, with the BGS III program" id=one-run-small-eig
Under the hypotheses of the theorem above, the probability is at most $\varphi$ that the counted run of `roundedShQRSmallEigAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside the matrix, the output and the failure word, or lists no spectrum of a matrix $\mathbf H+\mathbf E$ with $\|\mathbf E\|_2\le\delta$. The work and span bound is the certificate's $675307\,(n+1)^3(k+1)^4(n_p+1)(F+1)(T+1)^2$.
:::
::: end-model

## Not yet presented

- The formulas of the per-block precision terms of $u_{\mathrm{ShQR}}$ and of $u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, and the deflation threshold words $t$ and $t_L$. The page gives the bit counts instead.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- The relative-error forms (`roundedShQR_relative`, `roundedShQRSmallEig_relative` and its unconditional form) and the Hermitian corollaries at $B=1$, $k=128$ (`roundedShQR_hermitian`, `roundedShQRSmallEig_hermitian`). They are in the Library.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling. In the oracle model it also omits `SmallEig`'s cost.
- A Hessenberg reduction of a general input: the program starts from an upper Hessenberg matrix.

## Mathematical method

{{ generated:mathematical-method }}
