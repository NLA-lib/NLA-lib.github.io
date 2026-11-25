---
uid: f9f21f8a-b706-5973-b2c8-d108240c997b
kind: algorithm
id: lanczos
title: Lanczos process
summary: Build a Krylov basis and a tridiagonal compression of a symmetric operator.
status: outline
order: 1
theory:
- krylov-spaces
- spectral-theory
- orthogonal-polynomials
- finite-precision-krylov
library_algorithm: lanczos
search_aliases:
- Lanczos recurrence
- Lanczos tridiagonalization
- finite precision Lanczos
- matrix-free Lanczos
source_guides:
- docs/algorithms/Lanczos.md
library_results: false
result_ids:
- lanczos-breakdown
- lanczos-recurrence
- lanczos-tridiagonal
- lanczos-orthogonal-polynomials
- lanczos-jacobi-matrix
- random-start-lanczos
- kaniel-paige-saad
- ritz-value-gap-free
---

Build a Krylov basis and a tridiagonal compression of a symmetric operator. This shared factorization supports linear solves, spectral approximation, matrix functions, and quadrature. Its task placements all link to this one mathematical construction.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:lanczos-process-d9e8ae48 }}



## Mathematical guarantees

{{ statement:lanczos-tridiagonal }}

## Uses and composed algorithms

Lanczos is a shared process. Its compression supports several tasks; evaluating a function or averaging random probes adds further algorithmic steps, represented by their own pages.

{{ generated:applications }}

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
