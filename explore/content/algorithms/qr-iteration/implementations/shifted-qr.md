---
uid: 23322f24-5357-53be-901e-cc9acfe0ac9c
kind: implementation
id: shifted-qr
algorithm: qr-iteration
title: Exact arithmetic (BGS I)
summary: Scalar QR steps, shift search, and deflation, with two explicit local spectral primitives.
status: ready
library_algorithm: shifted-qr
library_results: false
arithmetic_models:
- id: exact
  arithmetic: exact
search_aliases:
- Exact shifted QR solver
source_guides:
- docs/algorithms/Shifted-QR.md
---

The library certifies a fixed shifted-QR program on complex upper Hessenberg matrices. Givens rotations, shifted steps, inverse-row solves, candidate search, and the deflation worklist expand into scalar and index operations. Two local spectral operations remain primitives: obtaining Ritz candidates and solving terminal blocks. The numerical guarantees and resource bounds refer to the same stored execution.

## Algorithm

Complex entries are stored as adjacent real and imaginary words, by columns. For matrix order $N$, shift degree $k=2^m$, and tolerance $\delta$, the solver computes $\tau=\delta\|\mathbf{H}\|_{\mathrm F}$ from its input and processes active diagonal blocks:

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

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

## Operation model and spectral primitives

The exact operation model includes real arithmetic, square root, copies, comparisons, dimension literals, and bounded natural-index conversion. It also includes these two operations:

| Primitive | Required guarantee | Use in the solver |
| --- | --- | --- |
| `ritz` | Return $k$ complex candidates satisfying the stated $\theta$-optimal Ritz condition for admissible Hessenberg inputs | Shift selection; the reference routine uses exact eigenvalues of the trailing $k\times k$ block |
| `smallEig` | Return every eigenvalue of the supplied block, with algebraic multiplicity | Terminal blocks of order at most $k$ |

Every spectral problem used by the full driver has order at most $k$. The `ritz` interface receives the active matrix and requested degree; the reference routine extracts its trailing block. Neither primitive supplies a completed QR step, a successful search, or a deflation result. Primitive work and workspace are explicit operation-model parameters.

{{ statement:nlalib-shiftedqr-kernelroutines-a68765a4 }}

The exact-arithmetic certificate retains this boundary, and it supplies no finite-arithmetic guarantee. The [finite-precision program](/explore/algorithms/qr-iteration/implementations/rounded-shifted-qr/) is a separate program and certificate: there the small-block solver is randomized, it returns a Schur pair, and the guarantee holds with a probability over a random tape. Its page has two models: any solver meeting a small-block Schur contract, or the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/), a program with no oracle. [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) builds on them for any dense matrix.

## Input assumptions

The caller supplies a complex upper Hessenberg matrix, parameter words $[B,\theta,\alpha,\gamma,\delta]$, and output capacity. Initial reduction to Hessenberg form is outside this program.

| Assumption | Meaning |
| --- | --- |
| Diagonalization $\mathbf{H}\mathbf{V}=\mathbf{V}\operatorname{diag}(d)$ with invertible $\mathbf{V}$ and $2\kappa(\mathbf{V})\le B$ | Bounds eigenvector conditioning, with room for perturbations during deflation |
| $g>0$ and $|d_i-d_j|\ge g$ for $i\ne j$ | Provides eigenvalue separation |
| $m\ge1$, $k=2^m$, $\theta,\alpha\ge1$, and $B^{4m}\le\alpha^k$ | Sets the shift degree and search factors |
| $0<\gamma<1$ and $\delta>0$ | Sets contraction and tolerance |
| $(N-1)\tau\le g/(8NB)$ and $(N-1)\tau\le\|\mathbf{H}\|_2$ | Controls accumulated deflation perturbations |
| Sufficient iteration budget $F$ and the prescribed grid size $M$ | Makes the capped search find a split |

The exact budget and grid inequalities, along with storage-shape conditions, are in the source guide and the full solver interface below. These are mathematical input assumptions, rather than assumptions about execution succeeding.

## Output guarantees

{{ statement:nlalib-shiftedqr-forwarddeflationalgorithm-3677cbb0 }}

## Cost and storage

{{ statement:nlalib-shiftedqr-counteddeflationalgorithm-aaf66e60 }}

Instruction counts, scratch, and resident memory retain the detailed program-manifest bounds. Scratch includes declared primitive workspace; resident payload also includes the supplied $2N^2+5+2N$ real-word cells. Scoped buffers are released and the tape position is unchanged.

Some useful component scratch bounds, excluding caller-owned inputs and outputs, are:

| Component | Stored real-word scratch |
| --- | ---: |
| One shifted step | $2N^2+14$ |
| Repeated shifts or a stored shift list | $4N^2+14$ |
| Streaming exceptional-shift search | $4N^2+14$ |

Primitive workspace is accounted for separately by the model and included in the full certificate. These component bounds are not a storage formula for the complete worklist.

## Full solver interface

{{ statement:nlalib-shiftedqr-exactdeflationalgorithm-80c3e8b3 }}

## Step interface

{{ statement:nlalib-shiftedqr-stepalgorithm-0dbb2cc9 }}

## Source guide

{{ generated:source-guides }}

## Mathematical method

{{ generated:mathematical-method }}
