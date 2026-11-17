---
kind: implementation
id: small-eig
algorithm: inverse-iteration
title: Randomized shifted inverse iteration (BGS III)
summary: All eigenvalues of a small matrix by Gaussian regularization, a random Hessenberg form and shifted inverse iteration, in rounded arithmetic.
status: ready
library_algorithm: small-eig
arithmetic_models:
- id: standard
  arithmetic: standard
search_aliases:
- SmallEig
- Small-eigenvalue solver
- Banks Garza-Vargas Srivastava III
- BGS III
---

The library certifies the small-eigenvalue solver of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR III* (Theorem 1.1, the algorithm `Eig`). It computes all eigenvalues of a complex matrix, with a backward error $\delta$ and a failure probability $\varphi$ over a random tape, in rounded arithmetic. It has no eigenvalue oracle: its primitives are scalar operations, comparisons, index operations and draws. It finds one eigenvalue at a time by shifted inverse iteration, carried out as repeated shifted QR steps with one shift, and deflates it.

The [finite-precision shifted QR program (BGS II)](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=small-eig-program) runs this program in place of its small-eigenvalue oracle.

## Algorithm

The input is a complex matrix $\mathbf M$ of order $N$, not necessarily Hessenberg. The program first regularizes it by a Gaussian perturbation. With high probability the perturbed matrix is diagonalizable, with a bounded eigenvector condition number and separated eigenvalues, and every later step relies on that. The program then deflates one eigenvalue at a time, using the worklist of the shifted QR program at bottom width $k=1$.

```text
input: M of order N; twelve parameter words Q; loop cap T
if N <= 1: copy the entry to the output; stop
set the 2N output words to 0
W := M + fl(gamma / sqrt N) G        G complex Gaussian, from 2N^2 draws of the Gaussian stream
reduce W to upper Hessenberg form (rounded, bottom-up)
worklist at bottom width 1, threshold word Q[6]:
    a block of order 1: store its entry as an eigenvalue
    a block of order d >= 2:
        RHess: draw a complex Gaussian direction g, rotate it to e_d by d - 1 rounded
            Givens rotations, and reduce to Hessenberg form again
        OneEig: from a uniform sample s of a disk of radius eta_2, for at most t rounds:
            estimate by DistSpec the distance to the spectrum of six perturbed points
            at distance tau around s, and move s to the best if its estimate is at most
            0.66 tau; stop when the estimate at s is at most 0.9 beta'
        Decouple: at most m_2 rounded shifted QR steps with the shift s, until the last
            subdiagonal entry passes the threshold
        split off the last row and column
DistSpec(H, s): m = 2^q rounded shifted QR steps with the shift s; the product of the
    moduli of the last diagonal entries of their triangular factors; q square roots
```

`RHess` makes the weights of the last row of an eigenvector matrix large, which `OneEig` and `Decouple` need. The direction is a complex Gaussian vector applied by rotations; the paper uses a uniform vector on the sphere applied by a reflector. `DistSpec` estimates the distance to the spectrum within $10\%$, because $m$ shifted QR steps compute $\|\mathbf e_n^{\mathsf T}(\mathbf H-s)^{-m}\|^{-1/m}$ approximately. This is inverse iteration.

Every loop is capped, by the words $m,t,m_2\le T$ and by $2N$ rounds of the worklist, and the order-one blocks are a base case. So the run terminates on every tape (`smallEigProg_terminates`). A failure inside the core leaves the zeroed output words stored.

The twelve parameter words are computed by the library from the order bound $n_{\max}$, the norm bound $\Sigma$, the backward error $\delta$, the failure probability $\varphi$ and the two tail records (`smallEigParams`). They are supplied as exact reals, and their computation is not charged.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The machine has the standard model with unit roundoff $u$ and no overflow or underflow, index literals, exact natural literals up to $n+1$, exact natural conversion and exact comparisons. The tape has two streams: $s_U$, uniform on $[0,1]$, read by the exact polar disk sampler ($R\sqrt{t_0}\,e^{2\pi i t_1}$ from two entries), and $s_G$, standard real Gaussian, read by draws that store the tape entry. The drawn values are exact; the arithmetic after a draw is rounded. The interpretation is measurable and reads the tape only in the windows of its calls.

The probability bounds need tails for the eigenvalue gap and the eigenvector condition number of $\mathbf M+\gamma n^{-1/2}\mathbf G$. The library proves them with the records $(10000e,5,1/2,2)$ and $(128e,3,2,2)$ (see [pseudospectral shattering](/explore/theory/pseudospectral-shattering/)), so the theorems below are unconditional. Each also has a general form with the records as hypotheses.

**Precision.** $u\le u_{\mathrm{SmallEig}}$, the minimum of five named per-block terms at $n_{\max}$ (`uSmallEig`). For fixed tail records there are constants $e_1,e_2$ with

$$\log_2\frac1{u_{\mathrm{SmallEig}}}\le e_1\log_2^2Y+e_2,\qquad Y=\frac{4n_{\max}\Sigma}{\delta\varphi}.$$

This is `logb_inv_uSmallEig_le`: $O(\log^2)$ bits, as in Theorem 1.1. The constants are not stated in closed form.

## Operations and Storage

::: definition decl:NLAlib.SmallEig.smallEigAlgorithm name="Certificate of the small-eigenvalue solver" id=certificate
The fixed program `smallEigProgram`, with unit costs and no oracle, succeeds on every admitted input, every interpretation of the model and every tape. It stays within the static budget, scratch and memory, writes only the output, and leaves the output stored. At the sizes $(n,n_q,T)$, for a matrix of order $n+1$, $n_q$ parameter words and the loop cap $T$, its work and span are at most

$$373483\,(n+1)^4(T+1)^2.$$
:::

The bound counts every instruction at unit cost: scalar operations, comparisons, index operations, draws, address computations, loop control and allocation. The constant is larger than the $3473\,(n+1)^4(T+1)^2$ operations and tests of `smallEig_work_le`, because the certificate also counts the structural instructions. The cap $T$ is a logarithm of $n_{\max}\Sigma/(\delta\varphi)$ up to constants. So the work is of order $n^4$ up to logarithmic factors. The paper's count is of order $n^4+n^3\log^2$.

The factor $n^4$ comes from re-randomizing the Hessenberg form after each deflation: `RHess` runs at every node of the worklist, with fresh randomness, at a cost of order $d^3$ for a block of order $d$. One random Hessenberg form followed by one-step decoupling would cost of order $n^3$, but no proof is known for it. The library keeps the per-node re-randomization, and it is open whether it is needed.

## Accuracy

::: theorem decl:NLAlib.SmallEig.smallEig_measureReal_not_spectrum_le_unconditional name="Theorem 1.1: backward error" id=accuracy
Let the machine and the streams be as above, with $u\le u_{\mathrm{SmallEig}}$ at the proved tail records. Let $n+1\le n_{\max}$, let $\mathbf M$ be a complex matrix of order $n+1$ with $\|\mathbf M\|_2\le\Sigma$, and let $0<\delta\le\Sigma$ and $0<\varphi\le1$. Start `smallEigProg` from a memory holding $\mathbf M$ and the parameter words. Then, for a random tape with the stream laws,

$$\mathbb P\bigl[\text{the run fails, writes outside its output, or lists no }\operatorname{spec}(\mathbf M+\mathbf E)\text{ with }\|\mathbf E\|_2\le\delta\bigr]\le\varphi.$$
:::

The error is absolute and $\Sigma$ is an input. The paper's form is relative; it is `smallEig_relative` and its unconditional form, with $\|\mathbf M\|_2\le\Sigma\le c\|\mathbf M\|_2$ and error $\varepsilon\|\mathbf M\|_2$. The failure probability is split in four parts: the eigenvalue gap, the condition number, the norm of the perturbation and the worklist.

::: theorem decl:NLAlib.SmallEig.smallEigProg_randomSmallEigContract_unconditional name="Corollary 1.3: a forward-error routine" id=forward
Let the machine and the streams be as above, with exact natural literals up to $k'_{\max}\le k_{\max}$, and let $0<\beta\le\Sigma$ and $0<\varphi\le1$. Let $u\le u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$ at the proved tail records. Take the parameter words and the cap of the forward form at $k_{\max}$. Then `smallEigProg` is a randomized small-eigenvalue routine for upper Hessenberg blocks $\mathbf B$ of order $d\le k'_{\max}$ with $\|\mathbf B\|_2\le\Sigma$. Except with probability at most $\varphi$, it writes only its $2d$ output words and stores values $\mu_1,\dots,\mu_d$ with $|\mu_i-\lambda_i|\le\beta$ for a listing $\lambda_1,\dots,\lambda_d$ of the eigenvalues of $\mathbf B$ with multiplicity.
:::

One list of words, chosen at $k_{\max}$, serves every order up to $k'_{\max}$; in the paper the order is fixed. The proof runs the backward form at $\delta_b=\Sigma\bigl(\beta/(4(2k_{\max}+1)\Sigma)\bigr)^{k_{\max}}$ and converts the backward error to a forward one by the [Ostrowski–Elsner matching](/explore/theory/perturbation-theory/#ostrowski-elsner), which costs the exponent $k_{\max}$. The form on one input is `smallEig_measureReal_not_forward_le` and its unconditional form. This contract is the hypothesis that the [shifted QR program](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=small-eig-program) discharges with this program.

::: theorem result:small-eig-certificate-accuracy name="On one counted run" id=one-run
Under the hypotheses of Theorem 1.1, the probability is at most $\varphi$ that the counted run of `smallEigAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside its output, or lists no spectrum of a matrix $\mathbf M+\mathbf E$ with $\|\mathbf E\|_2\le\delta$. The work and span bound is the certificate's $373483\,(n+1)^4(T+1)^2$.
:::

## Not yet presented

- The formulas of the five per-block precision terms of $u_{\mathrm{SmallEig}}$, of $u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, and of the twelve parameter words.
- The guarantees of the blocks on their own: `RHess`, `OneEig`, `DistSpec`, `Decouple` and the core worklist. They are in the Library under `NLAlib.Eigensolvers.SmallEig`.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling.
- A rounded Gaussian or disk sampler: the drawn values are exact.

## Mathematical method

{{ generated:mathematical-method }}
