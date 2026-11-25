---
uid: 2906d1be-3396-5842-9363-4c7753c847eb
kind: algorithm
id: golub-kahan
title: Golub–Kahan process
summary: Build a pair of Krylov bases and a block bidiagonal factorization of a rectangular operator.
status: outline
order: 8
theory:
- krylov-spaces
- subspaces
- singular-values
- perturbation-theory
- finite-precision-krylov
library_algorithm: block-golub-kahan
uses:
- gram-schmidt
search_aliases:
- Golub–Kahan bidiagonalization
- Golub-Kahan bidiagonalization
- block Golub–Kahan
- block Golub-Kahan
- band Golub–Kahan
- block Lanczos bidiagonalization
- Golub–Kahan–Lanczos
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
library_results: false
result_ids:
- block-golub-kahan-existence
- block-golub-kahan-krylov-range
- block-golub-kahan-band-structure
- block-golub-kahan-factored-output
---

Build a right basis $\mathbf{V}$ and a left basis $\mathbf{U}$ for a rectangular matrix $\mathbf{A}\in\Bbbk^{m\times n}$ from a start block $\mathbf\Omega\in\Bbbk^{n\times\ell}$, together with banded coefficient matrices $\mathbf{R}$ and $\mathbf{S}$ such that

$$\mathbf{A}\mathbf{V}_{<q}=\mathbf{U}\mathbf{R},\qquad\mathbf{A}^{\mathsf{H}}\mathbf{U}=\mathbf{V}\mathbf{S}.$$

The process alternates products with $\mathbf{A}$ and $\mathbf{A}^{\mathsf{H}}$. It is a shared Krylov factorization for a rectangular operator, as the Lanczos process is for a Hermitian one; randomized block Krylov iteration specifies how to use it for low-rank approximation. The library states the block form, with block width $\ell$ (named `b` in the Lean statements); $\ell=1$ gives bidiagonalization from a single start vector.

This page holds the exact mathematical process and its theory. The program, its certificate, and the bounds for a rounded run are on the implementation page.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

The process is defined over an orthogonalization step given by a contract, not by a formula.

{{ statement:nlalib-isbasisextension-12a7ec72 }}

{{ statement:nlalib-isblockgolubkahan-4dfc5d02 }}

## Mathematical guarantees

These statements hold in exact arithmetic, for every $\mathbf{A}$, every start block, and every exact extension scheme. Dependent start columns, rank-deficient $\mathbf{A}$, and breakdown inside the run are included: a dropped direction is a zero column of the stored basis.

{{ statement:nlalib-isblockgolubkahan-mul-blockprefix-right-eq }}

{{ statement:nlalib-isblockgolubkahan-conjtranspose-mul-left-eq }}

{{ statement:nlalib-isblockgolubkahan-gramdefect-right-eq-zero }}

{{ statement:nlalib-isblockgolubkahan-range-blockprefix-right }}

{{ statement:block-golub-kahan-band-structure }}

{{ statement:block-golub-kahan-existence }}

{{ statement:block-golub-kahan-factored-output }}

## Components

The orthogonalization step is a parameter of the process. The scheme the library supplies for it is a column-wise two-pass classical Gram–Schmidt extension with threshold deflation, described as an implementation of Gram–Schmidt orthogonalization.

{{ generated:components }}

## Uses and composed algorithms

The process returns bases and coefficients. Using the factors for an approximation task is a further algorithmic step with its own page.

{{ generated:applications }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
