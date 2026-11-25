---
uid: 6f920667-a2bc-5dee-a40c-0defe7ec59c2
kind: algorithm
id: qr-iteration
title: Hessenberg shifted QR (BGS)
summary: The shifted QR algorithm of Banks, Garza-Vargas and Srivastava on Hessenberg matrices, with exact-arithmetic and finite-precision programs and BGS + Dense Schur (end-to-end).
search_aliases:
- QR eigenvalue iteration
- QR algorithm
- Banks Garza-Vargas Srivastava
status: ready
theory:
- spectral-theory
- perturbation-theory
- pseudospectral-shattering
result_ids:
- shifted-qr-ritz-dichotomy
- shifted-qr-normal-decoupling
- shifted-qr-rapid-decoupling
uses:
- qr
- hessenberg-reduction
library_results: false
source_guides:
- docs/algorithms/Shifted-QR.md
---

A QR eigenvalue method preserves the spectrum through unitary similarities and exposes small subdiagonal couplings that can be discarded to split the eigenvalue problem. A shifting strategy chooses which similarities to apply; a deflation rule decides when to split. Different strategies give different algorithms.

This page is the Hessenberg shifted QR algorithm of Banks, Garza-Vargas and Srivastava (BGS): a shifting strategy with exceptional shifts for upper Hessenberg matrices that are diagonalizable with a bounded eigenvector condition number. The library has certified programs for it in exact arithmetic (BGS I) and in finite precision (BGS II); they are different programs, not one program under two models. [BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) runs the finite-precision program inside a pipeline that accepts any dense matrix.

{{ statement:shifted-qr-step-cf917bf1 }}

## Outline shared by the programs

```text
start from an upper Hessenberg matrix
while an active block remains:
    choose shifts and apply shifted QR steps
    when a subdiagonal coupling is sufficiently small:
        split into smaller diagonal blocks
    solve terminal blocks and collect their eigenvalues
```

For multiple shifts $s_1,\ldots,s_k$, the shift polynomial is $p(z)=\prod_{j=1}^k(z-s_j)$. The exact-arithmetic program applies a sequence of single-shift steps. The candidate order, the shift search, the storage, and the operation model of each program are specified on its own page.

## What is certified

The library proves normal-matrix and conditioned nonnormal-matrix decoupling results, together with the Ritz-quality or early-decoupling dichotomy. The exact-arithmetic program connects scalar execution to backward error, a directed forward-error bound, and resource accounting.

The exact-arithmetic program uses local spectral primitives for Ritz candidates and terminal blocks of order at most the shift degree $k$. These are explicit operation-model assumptions with declared costs. See that implementation for its precise boundary and input hypotheses.

The finite-precision program has its own certificate. Its arithmetic is a machine in the standard model with unit roundoff $u$, its terminal blocks are solved by a randomized small-block Schur solver, and with probability at least $1-\varphi$ over a random tape it stores a Schur pair of a nearby matrix; the eigenvalues are the diagonal. The page of that program has two models. In one the small-block solver is any routine meeting a Schur contract. In the other it is the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/), and no hypothesis on a solver or on random matrices remains.

[BGS + Dense Schur (end-to-end)](/explore/algorithms/qr-iteration/implementations/dense-schur/) removes the Hessenberg and conditioning hypotheses: for any dense $\mathbf{A}$ it computes $\widehat{\mathbf{U}}$ and an exactly upper triangular $\widehat{\mathbf{T}}$.

## Programs

{{ generated:implementations }}

## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Source guide

{{ generated:source-guides }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
