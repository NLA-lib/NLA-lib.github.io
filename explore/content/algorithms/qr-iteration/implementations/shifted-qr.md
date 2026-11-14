---
kind: implementation
id: shifted-qr
algorithm: qr-iteration
title: Exact shifted QR solver
summary: Scalar QR steps, shift search, and deflation, with two explicit local spectral primitives.
status: ready
library_algorithm: shifted-qr
library_results: false
source_guides:
- docs/algorithms/Shifted-QR.md
---

The library certifies a fixed shifted-QR program on complex upper Hessenberg matrices. Givens rotations, shifted steps, inverse-row solves, candidate search, and the deflation worklist expand into scalar and index operations. Two local spectral operations remain primitives: obtaining Ritz candidates and solving terminal blocks. The numerical guarantees and resource bounds refer to the same stored execution.

## Algorithm

Complex entries are stored as adjacent real and imaginary words, by columns. For matrix order $N$, shift degree $k=2^m$, and tolerance $\delta$, the solver computes $\tau=\delta\|\mathbf H\|_{\mathrm F}$ from its input and processes active diagonal blocks:

```text
put the full matrix block on the worklist
while a block remains:
    if its order is at most k:
        call smallEig and store every eigenvalue, with multiplicity
    otherwise:
        scan for a subdiagonal coupling of magnitude at most tau
        while no split is found and the iteration budget remains:
            obtain k Ritz candidates for the trailing block
            try repeated shifted QR steps with each candidate
            if none passes the decoupling or contraction test:
                select a promising candidate using inverse-row norms
                try it, then stream the exceptional-shift grid
            retain the selected QR result and scan again
        split at the detected coupling and enqueue the children
```

The input assumptions ensure that a required split is found within the budget. Splitting logically discards a small coupling; the backward-error witness accounts for it. The program retains that entry's physical words in the matrix arena.

Zero input pairs produce identity Givens rotations. Inverse-row solves test pivots and return either the inverse-row result or a singularity flag. The enclosing strategy handles these cases; the theorem does not assume a successful run or that all candidate shifts are nonsingular.

## Operation model and spectral primitives

The exact operation model includes real arithmetic, square root, copies, comparisons, dimension literals, and bounded natural-index conversion. It also includes these two operations:

| Primitive | Required guarantee | Use in the solver |
| --- | --- | --- |
| `ritz` | Return $k$ complex candidates satisfying the stated $\theta$-optimal Ritz condition for admissible Hessenberg inputs | Shift selection; the reference routine uses exact eigenvalues of the trailing $k\times k$ block |
| `smallEig` | Return every eigenvalue of the supplied block, with algebraic multiplicity | Terminal blocks of order at most $k$ |

Every spectral problem used by the full driver has order at most $k$. The `ritz` interface receives the active matrix and requested degree; the reference routine extracts its trailing block. Neither primitive supplies a completed QR step, a successful search, or a deflation result. Primitive work and workspace are explicit operation-model parameters.

::: definition decl:NLAlib.ShiftedQR.KernelRoutines name="Local spectral contracts"
The routine collection specifies the output lengths, Ritz optimality, and complete eigenvalue listing. The exact reference realization uses noncomputable root selection. It establishes consistency of the operation model; it is not an executable small eigensolver.
:::

The exact-arithmetic certificate retains this boundary. Implementing approximate small eigensolvers belongs to the finite-arithmetic extension, where accuracy, failure probability, and cost must be specified and composed. The current certificate supplies no finite-arithmetic guarantee.

## Input assumptions

The caller supplies a complex upper Hessenberg matrix, parameter words $[B,\theta,\alpha,\gamma,\delta]$, and output capacity. Initial reduction to Hessenberg form is outside this program.

| Assumption | Meaning |
| --- | --- |
| Diagonalization $\mathbf H\mathbf V=\mathbf V\operatorname{diag}(d)$ with invertible $\mathbf V$ and $2\kappa(\mathbf V)\le B$ | Bounds eigenvector conditioning, with room for perturbations during deflation |
| $g>0$ and $|d_i-d_j|\ge g$ for $i\ne j$ | Provides eigenvalue separation |
| $m\ge1$, $k=2^m$, $\theta,\alpha\ge1$, and $B^{4m}\le\alpha^k$ | Sets the shift degree and search factors |
| $0<\gamma<1$ and $\delta>0$ | Sets contraction and tolerance |
| $(N-1)\tau\le g/(8NB)$ and $(N-1)\tau\le\|\mathbf H\|_2$ | Controls accumulated deflation perturbations |
| Sufficient iteration budget $F$ and the prescribed grid size $M$ | Makes the capped search find a split |

The exact budget and grid inequalities, along with storage-shape conditions, are in the source guide and the full solver interface below. These are mathematical input assumptions, rather than assumptions about execution succeeding.

## Output guarantees

::: definition decl:NLAlib.ShiftedQR.exactForwardAlgorithm name="Backward and forward error certificate"
Under the stated input assumptions, execution terminates and initializes all $N$ stored complex outputs. Their multiset is exactly the characteristic-polynomial roots of $\mathbf H+\mathbf E$, including algebraic multiplicities, for a perturbation satisfying
$$\|\mathbf E\|_2\le (N-1)\delta\|\mathbf H\|_{\mathrm F}.$$
Every stored output is also within
$$\frac B2(N-1)\delta\|\mathbf H\|_{\mathrm F}$$
of some eigenvalue of $\mathbf H$. This forward bound is directed from outputs to the input spectrum; it does not assert a bijective matching or reverse coverage. The certificate retains the original resource guarantees.
:::

## Cost and storage

::: definition decl:NLAlib.ShiftedQR.exactAlgorithmWithPolynomialWork name="Full program work and span certificate"
The same program has both numerical guarantees above. Write $W$ for work and $S$ for sequential span. Their conservative bound is
$$W,\ S\le17109\,b^{14}\bigl(1+K(b^5)\bigr),$$
where $b=N+m+k+F+M+1$.
Here $K(L)$ is the finite maximum of the supplied costs of both spectral primitives over dimension lists of length at most two and entries at most $L$. The bound includes scalar, index, comparison, address, control, and allocation charges. It makes no polynomial-growth assumption about the primitive costs. This is a full-program upper bound, rather than the paper's tight complexity estimate or a bit-complexity bound.
:::

Instruction counts, scratch, and resident memory retain the detailed program-manifest bounds. Scratch includes declared primitive workspace; resident payload also includes the supplied $2N^2+5+2N$ real-word cells. Scoped buffers are released and the tape position is unchanged.

Some useful component scratch bounds, excluding caller-owned inputs and outputs, are:

| Component | Stored real-word scratch |
| --- | ---: |
| One shifted step | $2N^2+14$ |
| Repeated shifts or a stored shift list | $4N^2+14$ |
| Streaming exceptional-shift search | $4N^2+14$ |

Primitive workspace is accounted for separately by the model and included in the full certificate. These component bounds are not a storage formula for the complete worklist.

## Full solver interface

::: definition decl:NLAlib.ShiftedQR.exactAlgorithm name="Exact shifted-QR solver interface"
This is the original backward-error certificate for the fixed program. The stronger interfaces above preserve its program, operation model, and resource guarantees. Expand the Lean details for the exact specification and input domain.
:::

## Step interface

::: definition decl:NLAlib.ShiftedQR.stepAlgorithm name="Shifted-QR step interface"
This component certifies one raw scalar shifted-QR step under its exact operation model, including singular shifts. It is a constituent of the full solver and does not require the full solver's separation and conditioning assumptions.
:::

## Source guide

{{ generated:source-guides }}

## Mathematical method

{{ generated:mathematical-method }}
