---
kind: implementation
id: small-eig
algorithm: inverse-iteration
title: Randomized shifted inverse iteration (BGS III)
summary: A Schur pair and all eigenvalues of a small matrix by Gaussian regularization, a random Hessenberg form and shifted inverse iteration, in rounded arithmetic.
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

The library certifies the small-eigenvalue solver of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR III* (Theorem 1.1, the algorithm `Eig`). The paper computes eigenvalues. The library's program computes a Schur pair of a complex matrix: an upper triangular $\widehat{\mathbf T}_b$ in the matrix buffer, whose diagonal holds the computed eigenvalues, and an accumulator $\widehat{\mathbf U}_b$, with a backward error $\delta$ and a failure probability $\varphi$ over a random tape, in rounded arithmetic. It has no eigenvalue oracle: its primitives are scalar operations, comparisons, index operations and draws. It finds one eigenvalue at a time by shifted inverse iteration, carried out as repeated shifted QR steps with one shift, and deflates it.

The [finite-precision shifted QR program (BGS II)](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=bgs-iii-program) runs this program as its small-block Schur solver, and so does [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/).

## Algorithm

The input is a complex matrix $\mathbf M$ of order $N$, not necessarily Hessenberg. The program first regularizes it by a Gaussian perturbation. With high probability the perturbed matrix is diagonalizable, with a bounded eigenvector condition number and separated eigenvalues, and every later step relies on that. The program then deflates one eigenvalue at a time, using the worklist of the shifted QR program at bottom width $k=1$.

```text
input: M of order N, overwritten; twelve parameter words Q; loop cap T
U_b := I
if N <= 1: keep the block; stop
W := M + fl(gamma / sqrt N) G        G complex Gaussian, from 2N^2 draws of the Gaussian stream
reduce W to upper Hessenberg form (rounded, bottom-up), logging the rotations; replay them on U_b
worklist at bottom width 1, threshold word Q[6]:
    a block of order 1: keep its entry on the diagonal
    a block of order d >= 2:
        RHess: draw a complex Gaussian direction g, rotate it to e_d by d - 1 rounded
            Givens rotations, and reduce to Hessenberg form again
        OneEig: from a uniform sample s of a disk of radius eta_2, for at most t rounds:
            estimate by DistSpec the distance to the spectrum of six perturbed points
            at distance tau around s, and move s to the best if its estimate is at most
            0.66 tau; stop when the estimate at s is at most 0.9 beta'
        Decouple: at most m_2 rounded shifted QR steps with the shift s, until the last
            subdiagonal entry passes the threshold
        replay the logged rotations on the couplings and on U_b
        write an exact 0 at the cut and split off the last row and column
output: T_b (upper triangular) in the matrix buffer, U_b; the eigenvalues are diag(T_b)
DistSpec(H, s): m = 2^q rounded shifted QR steps with the shift s; the product of the
    moduli of the last diagonal entries of their triangular factors; q square roots
```

`RHess` makes the weights of the last row of an eigenvector matrix large, which `OneEig` and `Decouple` need. The direction is a complex Gaussian vector applied by rotations; the paper uses a uniform vector on the sphere applied by a reflector. `DistSpec` estimates the distance to the spectrum within $10\%$, because $m$ shifted QR steps compute $\|\mathbf e_n^{\mathsf T}(\mathbf H-s)^{-m}\|^{-1/m}$ approximately. This is inverse iteration.

Every loop is capped, by the words $m,t,m_2\le T$ and by $2N$ rounds of the worklist, and the order-one blocks are a base case. So the run terminates on every tape (`smallEigProg_terminates`).

The twelve parameter words are computed by the library from the order bound $n_{\max}$, the norm bound $\Sigma$, the backward error $\delta$, the failure probability $\varphi$ and the two tail records (`smallEigParams`). They are supplied as exact reals, and their computation is not charged.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The machine has the standard model with unit roundoff $u$ and no overflow or underflow, index literals, exact natural literals up to $n+1$, exact natural conversion and exact comparisons. The tape has two streams: $s_U$, uniform on $[0,1]$, read by the exact polar disk sampler ($R\sqrt{t_0}\,e^{2\pi i t_1}$ from two entries), and $s_G$, standard real Gaussian, read by draws that store the tape entry. The drawn values are exact; the arithmetic after a draw is rounded. The interpretation is measurable and reads the tape only in the windows of its calls.

The probability bounds need tails for the eigenvalue gap and the eigenvector condition number of $\mathbf M+\gamma n^{-1/2}\mathbf G$. The library proves them with the records $(2048e,11/3,2/3,2)$ and $(128e,3,2,2)$ (see [pseudospectral shattering](/explore/theory/pseudospectral-shattering/)), so the theorems below are unconditional. Each also has a general form with the records as hypotheses.

**Precision.** $u\le u_{\mathrm{SmallEig}}$, the minimum of five named per-block terms at $n_{\max}$ (`uSmallEig`). For fixed tail records there are constants $e_1,e_2$ with

$$\log_2\frac1{u_{\mathrm{SmallEig}}}\le e_1\log_2^2Y+e_2,\qquad Y=\frac{4n_{\max}\Sigma}{\delta\varphi}.$$

This is `logb_inv_uSmallEig_le`: $O(\log^2)$ bits, as in Theorem 1.1. The constants are not stated in closed form.

## Operations and Storage

::: definition decl:NLAlib.SmallEig.smallEigAlgorithm name="Certificate of the small-eigenvalue solver" id=certificate
The fixed program `smallEigProgram`, with unit costs and no oracle, succeeds on every admitted input, every interpretation of the model and every tape. It stays within the static budget, scratch and memory, writes only the matrix buffer and the accumulator, and leaves both stored. At the sizes $(n,n_q,T)$, for a matrix of order $n+1$, $n_q$ parameter words and the loop cap $T$, its work and span are at most

$$517058\,(n+1)^4(T+1)^2.$$
:::

The bound counts every instruction at unit cost: scalar operations, comparisons, index operations, draws, address computations, loop control and allocation. The constant is larger than the $80390\,(n+1)^4(T+1)^2$ of the instrumented program in `smallEig_work_le`, because the certificate also counts the frame of the program. The cap $T$ is a logarithm of $n_{\max}\Sigma/(\delta\varphi)$ up to constants. So the work is of order $n^4$ up to logarithmic factors. The paper's count is of order $n^4+n^3\log^2$.

The factor $n^4$ comes from re-randomizing the Hessenberg form after each deflation: `RHess` runs at every node of the worklist, with fresh randomness, at a cost of order $d^3$ for a block of order $d$. One random Hessenberg form followed by one-step decoupling would cost of order $n^3$, but no proof is known for it. The library keeps the per-node re-randomization, and it is open whether it is needed.

## Accuracy

::: theorem decl:NLAlib.SmallEig.smallEigProg_pwrites_schur name="The output is a Schur pair" id=accuracy-schur
Let the machine and the streams be as above, with tail records that bound the two Ginibre tails, $u\le u_{\mathrm{SmallEig}}$ at those records, $n+1\le n_{\max}$, $\|\mathbf M\|_2\le\Sigma$, $0<\delta\le\Sigma$ and $0<\varphi\le1$. From a memory holding $\mathbf M$ and the parameter words, except with probability at most $\varphi$, the run writes only the matrix and the accumulator and stores an upper triangular $\widehat{\mathbf T}_b$ and an accumulator $\widehat{\mathbf U}_b$ with

$$\widehat{\mathbf T}_b=\mathbf V^{\mathsf H}(\mathbf M+\mathbf E)\mathbf V,\qquad\|\mathbf E\|_2\le\delta,\qquad\|\widehat{\mathbf U}_b-\mathbf V\|_2\le(1+24u)^{R}-1$$

for an exact unitary $\mathbf V$, with $R=n_{\max}^2+2(n_{\max}+1)\bigl((T+n_{\max})n_{\max}+6\bigr)$ (`smallEigLeafRotations`). The proved tail records satisfy the hypothesis. The eigenvalue theorems below are corollaries: the diagonal of $\widehat{\mathbf T}_b$ lists them.
:::

::: theorem decl:NLAlib.SmallEig.smallEig_measureReal_not_spectrum_le_unconditional name="Theorem 1.1: eigenvalues, backward error" id=accuracy
Let the machine and the streams be as above, with $u\le u_{\mathrm{SmallEig}}$ at the proved tail records. Let $n+1\le n_{\max}$, let $\mathbf M$ be a complex matrix of order $n+1$ with $\|\mathbf M\|_2\le\Sigma$, and let $0<\delta\le\Sigma$ and $0<\varphi\le1$. Start `smallEigProg` from a memory holding $\mathbf M$ and the parameter words. Then, for a random tape with the stream laws,

$$\mathbb P\bigl[\text{the run fails, writes outside the matrix and the accumulator, or does not store an upper triangular }\widehat{\mathbf T}_b\text{ whose diagonal lists }\operatorname{spec}(\mathbf M+\mathbf E)\text{ with }\|\mathbf E\|_2\le\delta\bigr]\le\varphi.$$
:::

The error is absolute and $\Sigma$ is an input. The paper's form is relative; it is `smallEig_relative` and its unconditional form, with $\|\mathbf M\|_2\le\Sigma\le c\|\mathbf M\|_2$ and error $\varepsilon\|\mathbf M\|_2$. The failure probability is split in four parts: the eigenvalue gap, the condition number, the norm of the perturbation and the worklist.

::: theorem result:small-eig-forward-error name="Corollary 1.3: forward error" id=forward
Let the machine and the streams be as above, with exact natural literals up to $k_{\max}$, and let $0<\beta\le\Sigma$ and $0<\varphi\le1$. Let $u\le u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$ at the proved tail records. Take the parameter words and the cap of the forward form at $k_{\max}$. For $\mathbf M$ of order $n+1\le k_{\max}$ with $\|\mathbf M\|_2\le\Sigma$, except with probability at most $\varphi$, the run writes only the matrix and the accumulator and stores $\widehat{\mathbf T}_b$ with $|(\widehat{\mathbf T}_b)_{ii}-\lambda_i|\le\beta$ for a listing $\lambda_1,\dots,\lambda_{n+1}$ of the eigenvalues of $\mathbf M$ with multiplicity.
:::

One list of words, chosen at $k_{\max}$, serves every order up to $k_{\max}$; in the paper the order is fixed. The proof runs the backward form at $\delta_b=\Sigma\bigl(\beta/(4(2k_{\max}+1)\Sigma)\bigr)^{k_{\max}}$ and converts the backward error to a forward one by the [Ostrowski–Elsner matching](/explore/theory/perturbation-theory/#ostrowski-elsner), which costs the exponent $k_{\max}$.

::: theorem decl:NLAlib.SmallEig.smallEigProg_randomSchurLeafContract name="The program is a small-block Schur solver" id=schur-leaf
On the machine and streams above, with exact natural literals up to $d_{\max}\le k_{\max}$, tail records bounding the two Ginibre tails, $0<\beta\le\Sigma$, $0<\varphi\le1$ and $u\le u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, the program with the forward words meets the small-block Schur contract on orders at most $d_{\max}$ and norms at most $\Sigma$: except with probability $\varphi$ it stores an upper triangular $\mathbf T_b$ and an accumulator $\mathbf U_b$ with $\mathbf T_b=\mathbf V_b^{\mathsf H}(\mathbf B+\mathbf F)\mathbf V_b$, $\|\mathbf F\|_2\le\delta_b$ and $\|\mathbf U_b-\mathbf V_b\|_2\le(1+24u)^{R_L}-1$, for an exact unitary $\mathbf V_b$ and $R_L=k_{\max}^2+2(k_{\max}+1)\bigl((T+k_{\max})k_{\max}+6\bigr)$.
:::

This contract is the hypothesis that the [shifted QR program](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=bgs-iii-program) and [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) discharge with this program.

::: theorem result:small-eig-certificate-accuracy name="On one counted run" id=one-run
Under the hypotheses of Theorem 1.1, the probability is at most $\varphi$ that the counted run of `smallEigAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside the matrix and the accumulator, or does not store an upper triangular $\widehat{\mathbf T}_b$ whose diagonal lists the spectrum of a matrix $\mathbf M+\mathbf E$ with $\|\mathbf E\|_2\le\delta$. The work and span bound is the certificate's $517058\,(n+1)^4(T+1)^2$.
:::

## Not yet presented

- The formulas of the five per-block precision terms of $u_{\mathrm{SmallEig}}$, of $u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, and of the twelve parameter words.
- The guarantees of the blocks on their own: `RHess`, `OneEig`, `DistSpec`, `Decouple` and the core worklist. They are in the Library under `NLAlib.Eigensolvers.SmallEig`.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling.
- A rounded Gaussian or disk sampler: the drawn values are exact.

## Mathematical method

{{ generated:mathematical-method }}
