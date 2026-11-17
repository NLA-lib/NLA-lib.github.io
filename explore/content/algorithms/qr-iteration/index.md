---
kind: algorithm
id: qr-iteration
title: Hessenberg shifted QR (BGS)
summary: The shifted QR algorithm of Banks, Garza-Vargas and Srivastava on Hessenberg matrices, with an exact-arithmetic program and a finite-precision program.
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

This page is the Hessenberg shifted QR algorithm of Banks, Garza-Vargas and Srivastava (BGS): a shifting strategy with exceptional shifts for upper Hessenberg matrices that are diagonalizable with a bounded eigenvector condition number. The library has two certified programs for it, one in exact arithmetic (BGS I) and one in finite precision (BGS II). They are different programs, not one program under two models.

::: definition name="Shifted QR step"
Choose a shift $\mu_j$ and factor $\mathbf A_j-\mu_j\mathbf I=\mathbf Q_j\mathbf R_j$. Set $\mathbf A_{j+1}=\mathbf R_j\mathbf Q_j+\mu_j\mathbf I=\mathbf Q_j^{\mathsf{H}}\mathbf A_j\mathbf Q_j$. Thus each exact step preserves eigenvalues. Shift selection, deflation tests, and explicit or implicit execution belong to concrete variants. The target for a general matrix is Schur form, rather than necessarily a diagonal matrix.
:::

## Outline shared by the two programs

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

The finite-precision program has its own certificate. Its arithmetic is a machine in the standard model with unit roundoff $u$, its terminal blocks and Ritz values are computed by a randomized small-eigenvalue solver, and it stores the eigenvalues of a nearby matrix with probability at least $1-\varphi$ over a random tape. The page of that program has two models. In one the small-eigenvalue solver is an oracle, specified by its accuracy and failure probability. In the other it is the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/), and the theorem has no oracle hypothesis. That theorem is unconditional: the random-matrix tails it needs are proved.

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
