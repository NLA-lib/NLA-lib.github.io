---
uid: 78b0fd5e-2147-58a6-98dd-2e3b46c51952
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

The library certifies the small-eigenvalue solver of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR III* (Theorem 1.1, the algorithm `Eig`). The paper computes eigenvalues. The library's program computes a Schur pair of a complex matrix: an upper triangular $\widehat{\mathbf{T}}_b$ in the matrix buffer, whose diagonal holds the computed eigenvalues, and an accumulator $\widehat{\mathbf{U}}_b$, with a backward error $\delta$ and a failure probability $\varphi$ over a random tape, in rounded arithmetic. It has no eigenvalue oracle: its primitives are scalar operations, comparisons, index operations and draws. It finds one eigenvalue at a time by shifted inverse iteration, carried out as repeated shifted QR steps with one shift, and deflates it.

The [finite-precision shifted QR program (BGS II)](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=bgs-iii-program) runs this program as its small-block Schur solver, and so does [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/).

## Algorithm

The input is a complex matrix $\mathbf{M}$ of order $N$, not necessarily Hessenberg. The program first regularizes it by a Gaussian perturbation. With high probability the perturbed matrix is diagonalizable, with a bounded eigenvector condition number and separated eigenvalues, and every later step relies on that. The program then deflates one eigenvalue at a time, using the worklist of the shifted QR program at bottom width $k=1$.

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

`RHess` makes the weights of the last row of an eigenvector matrix large, which `OneEig` and `Decouple` need. The direction is a complex Gaussian vector applied by rotations; the paper uses a uniform vector on the sphere applied by a reflector. `DistSpec` estimates the distance to the spectrum within $10\%$, because $m$ shifted QR steps compute $\|\mathbf{e}_n^{\mathsf{T}}(\mathbf{H}-s)^{-m}\|^{-1/m}$ approximately. This is inverse iteration.

Every loop is capped, by the words $m,t,m_2\le T$ and by $2N$ rounds of the worklist, and the order-one blocks are a base case. So the run terminates on every tape (`smallEigProg_terminates`).

The twelve parameter words are computed by the library from the order bound $n_{\max}$, the norm bound $\Sigma$, the backward error $\delta$, the failure probability $\varphi$ and the two tail records (`smallEigParams`). They are supplied as exact reals, and their computation is not charged.

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The machine has the standard model with unit roundoff $u$ and no overflow or underflow, index literals, exact natural literals up to $n+1$, exact natural conversion and exact comparisons. The tape has two streams: $s_U$, uniform on $[0,1]$, read by the exact polar disk sampler ($R\sqrt{t_0}\,e^{2\pi i t_1}$ from two entries), and $s_G$, standard real Gaussian, read by draws that store the tape entry. The drawn values are exact; the arithmetic after a draw is rounded. The interpretation is measurable and reads the tape only in the windows of its calls.

The probability bounds need tails for the eigenvalue gap and the eigenvector condition number of $\mathbf{M}+\gamma n^{-1/2}\mathbf{G}$. The library proves them with the records $(2048e,11/3,2/3,2)$ and $(128e,3,2,2)$ (see [pseudospectral shattering](/explore/theory/pseudospectral-shattering/)), so the theorems below are unconditional. Each also has a general form with the records as hypotheses.

**Precision.** $u\le u_{\mathrm{SmallEig}}$, the minimum of five named per-block terms at $n_{\max}$ (`uSmallEig`). For fixed tail records there are constants $e_1,e_2$ with

$$\log_2\frac1{u_{\mathrm{SmallEig}}}\le e_1\log_2^2Y+e_2,\qquad Y=\frac{4n_{\max}\Sigma}{\delta\varphi}.$$

This is `logb_inv_uSmallEig_le`: $O(\log^2)$ bits, as in Theorem 1.1. The constants are not stated in closed form.

## Operations and Storage

{{ statement:nlalib-smalleig-smalleigalgorithm-cf55d814 }}

The bound counts every instruction at unit cost: scalar operations, comparisons, index operations, draws, address computations, loop control and allocation. The constant is larger than the $80390\,(n+1)^4(T+1)^2$ of the instrumented program in `smallEig_work_le`, because the certificate also counts the frame of the program. The cap $T$ is a logarithm of $n_{\max}\Sigma/(\delta\varphi)$ up to constants. So the work is of order $n^4$ up to logarithmic factors. The paper's count is of order $n^4+n^3\log^2$.

The factor $n^4$ comes from re-randomizing the Hessenberg form after each deflation: `RHess` runs at every node of the worklist, with fresh randomness, at a cost of order $d^3$ for a block of order $d$. One random Hessenberg form followed by one-step decoupling would cost of order $n^3$, but no proof is known for it. The library keeps the per-node re-randomization, and it is open whether it is needed.

## Accuracy

{{ statement:nlalib-smalleig-smalleigprog-pwrites-schur }}

{{ statement:nlalib-smalleig-smalleig-measurereal-not-spectrum-le-unconditional }}

The error is absolute and $\Sigma$ is an input. The paper's form is relative; it is `smallEig_relative` and its unconditional form, with $\|\mathbf{M}\|_2\le\Sigma\le c\|\mathbf{M}\|_2$ and error $\varepsilon\|\mathbf{M}\|_2$. The failure probability is split in four parts: the eigenvalue gap, the condition number, the norm of the perturbation and the worklist.

{{ statement:small-eig-forward-error }}

One list of words, chosen at $k_{\max}$, serves every order up to $k_{\max}$; in the paper the order is fixed. The proof runs the backward form at $\delta_b=\Sigma\bigl(\beta/(4(2k_{\max}+1)\Sigma)\bigr)^{k_{\max}}$ and converts the backward error to a forward one by the [Ostrowski–Elsner matching](/explore/theory/perturbation-theory/#ostrowski-elsner), which costs the exponent $k_{\max}$.

{{ statement:nlalib-smalleig-smalleigprog-randomschurleafcontract }}

This contract is the hypothesis that the [shifted QR program](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/?model=bgs-iii-program) and [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) discharge with this program.

{{ statement:small-eig-certificate-accuracy }}

## Not yet presented

- The formulas of the five per-block precision terms of $u_{\mathrm{SmallEig}}$, of $u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, and of the twelve parameter words.
- The guarantees of the blocks on their own: `RHess`, `OneEig`, `DistSpec`, `Decouple` and the core worklist. They are in the Library under `NLAlib.Eigensolvers.SmallEig`.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- A bit-operation count. The work counts instructions of unit cost; it gives no bit costs for arithmetic or sampling.
- A rounded Gaussian or disk sampler: the drawn values are exact.

## Mathematical method

{{ generated:mathematical-method }}
