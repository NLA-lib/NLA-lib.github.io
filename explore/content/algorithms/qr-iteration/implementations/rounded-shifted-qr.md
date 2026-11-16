---
kind: implementation
id: rounded-shifted-qr
algorithm: qr-iteration
title: Rounded shifted QR solver
summary: The shifted QR program in rounded arithmetic, with a randomized small-eigenvalue kernel and a random tape.
status: outline
library_algorithm: shifted-qr-rounded
library_results: false
---

The library certifies a second shifted QR program, for rounded arithmetic. It is a different program from the [exact solver](/explore/algorithms/qr-iteration/implementations/shifted-qr/), over a different operation model: scalar arithmetic is the arithmetic of a machine, terminal blocks are solved by a randomized kernel that may fail on a bad window of the tape, and the program draws shifts from the tape. Its accuracy holds with a probability over the tape, not on every run.

This page states the certificate and its accuracy theorem. It does not yet present pseudocode, the parameter words, or the explicit precision threshold; see [what is not presented](#section-not-yet-presented).

## Algorithm

The program is the rounded deflation worklist with the decoupling loop and a `SmallEig` leaf. Its sizes are the order $n+1$ of the matrix, the shift degree $k$, the number $n_p$ of parameter words, and the iteration cap $F$. It is supplied five buffers:

| Buffer | Content |
| --- | --- |
| Matrix | The $2(n+1)^2$ words of a complex matrix of order $n+1$, overwritten by the run |
| Threshold | One deflation threshold word |
| Parameters | $n_p$ parameter words |
| Output | Room for $2(n+1)$ words: the computed eigenvalues |
| Failure | One failure word |

The shift degree, the parameter words, the threshold word and the cap are determined by five reals of the input: a condition bound $B$, a separation $\Gamma$, a norm bound $\Sigma$, a backward error $\delta$ and a failure probability $\varphi$.

## Operation model

::: definition decl:NLAlib.ShiftedQR.shqrModel name="Operation model of the rounded solver" id=model
The operations are scalar arithmetic, dimension literals, two eigenvalue kernels and a disk sampler.

- Scalar arithmetic is the function of a machine. The model does not constrain the machine: the standard model at unit roundoff $u$ is a hypothesis of the accuracy theorem only.
- Dimension literals, comparisons and index conversion are exact.
- `SmallEig` is specified by a contract, not by a function. At order $d$ it reads the $2d^2$ words of a matrix and a window of $W(d)$ entries of one stream of the tape, and writes $2d$ words. If the matrix is upper Hessenberg and the window is not in its bad set, the output is within $\beta$ of a listing of the eigenvalues with multiplicity. On a window in the bad set it may return any words.
- The disk sampler is exact. It reads a radius $R$ and two entries $(t_0,t_1)$ of the same stream, and writes $R\sqrt{t_0}\,e^{2\pi i t_1}$.
- The `Ritz` kernel is in the operation signature, which is shared with the exact program, but this program never calls it.

Each kernel call costs the work, span and workspace that the caller supplies for its dimensions; these weights can be zero. Every other primitive, query and structural instruction costs one unit of work and span.
:::

The model is realized by exact eigenvalues and the exact sampler. That a measurable interpretation meets the `SmallEig` contract is assumed by the accuracy theorem, not exhibited: no small eigensolver is implemented here.

## Operations and Storage

::: definition decl:NLAlib.ShiftedQR.roundedShQRAlgorithm name="Certificate of the rounded solver" id=certificate
Let the sizes $(n,k,n_p,F)$ be admitted: natural literals up to $n+1$ are exact on the machine, $k\le n$, and $k$, $n_p$ and $F$ are those of some parameter reals. Let the bad sets be measurable, $\beta\ge0$, and let the supplied kernel span be at most the supplied kernel work.

Then, on every admitted input, every interpretation that meets the model, and every tape, the run of the fixed program succeeds within the static budget, scratch and memory of the program. Its work is at most

$$196017\,(n+1)^3(k+1)^3(n_p+1)(F+1)+8\,c^4\,\overline{w},\qquad c=n+k+n_p+F+2,$$

where $\overline{w}$ is the largest supplied kernel work over dimension lists of at most one entry, of size at most $c^2$. Its span satisfies the same bound with the supplied kernel span. The first term bounds the instructions, each of unit weight; the second is at most $8c^4$ kernel calls at their largest weight. The run writes only the matrix, the output and the failure word.

No accuracy holds on every tape, not even given a failure word equal to $0$: on a bad window `SmallEig` may return any words, and a terminal block stores them as its eigenvalues.
:::

The supplied buffers hold $2(n+1)^2+1+n_p+2(n+1)+1$ words. The budget, scratch and resident memory are bounds by the static count of the program; this page gives no closed formula for them.

## Accuracy

::: theorem decl:NLAlib.ShiftedQR.roundedShQR_algorithm_measureReal_not_accepts_le name="Accuracy on one run" id=accuracy
Let the machine be in the standard model with unit roundoff $u$. Let the input hold an upper Hessenberg matrix $\mathbf H$ of order $n+1$ at admitted sizes, with

- $\mathbf H\mathbf V=\mathbf V\operatorname{diag}(\lambda)$ for an invertible $\mathbf V$ with $\kappa(\mathbf V)\le B$;
- $|\lambda_i-\lambda_j|\ge\Gamma>0$ for $i\ne j$;
- $\|\mathbf H\|_2\le\Sigma$, $0<\delta\le\Sigma$ and $0<\varphi\le1$.

Let the bad sets of `SmallEig` be measurable, each of probability at most $\varphi_{\mathrm{se}}$ under the product law of its stream at every upper Hessenberg matrix, and assume

$$0\le\beta\le\texttt{shqrSmallEigAccuracy},\qquad0\le\varphi_{\mathrm{se}}\le\texttt{shqrSmallEigFailure},\qquad u\le\texttt{uShQR}.$$

Let the interpretation meet the model, be measurable, and read the tape only in the windows of its calls. Let the tape have independent entries with the given stream laws, the stream of `SmallEig` and of the sampler being uniform on $[0,1]$.

Then the probability over the tape of the following event is at most $\varphi$: the counted run of the certificate's program fails, or exceeds its budget, scratch or memory, or has work or span above the bound of the certificate, or writes outside the matrix, the output and the failure word, or does not both set the failure word to $0$ and store all eigenvalues, with multiplicity, of some $\mathbf H+\mathbf E$ with $\|\mathbf E\|_2\le\delta$.
:::

By the certificate, the run succeeds and meets its resource bounds on every tape. The probability therefore concerns the stored output: a backward error of at most $\delta$ with probability at least $1-\varphi$. The theorem is the library's corrected form of Theorem 6.3 of Banks, Garza-Vargas and Srivastava, with the quantifiers of their Theorem 1.4.

The three bounds named in code are definitions of the library, functions of $n$, $k$, $B$, $\Gamma$, $\Sigma$, $\delta$ and $\varphi$. The failure allowed to `SmallEig` is $\varphi/(12F(n+1))$. The precision threshold `uShQR` is the minimum of four named per-block terms.

## Not yet presented

- Pseudocode of the worklist, the decoupling loop, the shift search and the regularization.
- The parameter words, the deflation threshold, the shift degree $k$ and the cap $F$ as functions of $B$, $\Gamma$, $\Sigma$, $\delta$ and $\varphi$.
- The formulas of `shqrSmallEigAccuracy` and `uShQR`. In particular, this page does not state how many bits of precision suffice.
- Closed bounds for the instruction budget, the scratch and the resident memory.
- The separate statements of the output probability and of the static count in the library, which this certificate combines on one run.
- A bit-operation count. The work counts instructions of unit cost and the supplied kernel weights; it gives no bit costs for arithmetic, the kernel or sampling.

## Mathematical method

{{ generated:mathematical-method }}
