---
kind: algorithm
id: qr-iteration
title: QR eigenvalue iteration
summary: Use repeated QR factorizations and orthogonal similarities to approximate a Schur form.
status: ready
theory:
- spectral-theory
- perturbation-theory
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

QR iteration preserves the spectrum through unitary similarities and exposes small subdiagonal couplings that can be discarded to split the eigenvalue problem. A shifting strategy chooses which similarities to apply; a deflation rule decides when to split.

::: definition name="QR eigenvalue iteration"
Choose a shift $\mu_j$ and factor $\mathbf A_j-\mu_j\mathbf I=\mathbf Q_j\mathbf R_j$. Set $\mathbf A_{j+1}=\mathbf R_j\mathbf Q_j+\mu_j\mathbf I=\mathbf Q_j^{\mathsf{H}}\mathbf A_j\mathbf Q_j$. Thus each exact step preserves eigenvalues. Shift selection, deflation tests, and explicit or implicit execution belong to concrete variants. The target for a general matrix is Schur form, rather than necessarily a diagonal matrix.
:::

## Abstract algorithm

```text
start from an upper Hessenberg matrix
while an active block remains:
    choose shifts and apply shifted QR steps
    when a subdiagonal coupling is sufficiently small:
        split into smaller diagonal blocks
    solve terminal blocks and collect their eigenvalues
```

For multiple shifts $s_1,\ldots,s_k$, the shift polynomial is $p(z)=\prod_{j=1}^k(z-s_j)$. The exact implementation applies a sequence of single-shift steps. Its candidate order, exceptional-shift search, storage, and operation model are specified on the implementation page.

## What is certified

The library proves normal-matrix and conditioned nonnormal-matrix decoupling results, together with the Ritz-quality or early-decoupling dichotomy. The concrete exact solver connects scalar execution to backward error, a directed forward-error bound, and resource accounting.

The exact solver uses local spectral primitives for Ritz candidates and terminal blocks of order at most the shift degree $k$. These are explicit operation-model assumptions with declared costs. Approximate small eigensolvers and rounded QR analysis belong to the finite-arithmetic extension. See the implementation for the precise current boundary and input hypotheses.

## Implementations

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
