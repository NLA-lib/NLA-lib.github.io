---
kind: algorithm
id: lanczos
title: Lanczos process
summary: Build a Krylov basis and a tridiagonal compression of a symmetric operator.
status: outline
order: 1
tasks:
- eigenvalues
- matrix-functions
- quadrature
- trace-estimation
theory:
- krylov-spaces
- spectral-theory
- orthogonal-polynomials
library_algorithm: lanczos
search_aliases:
- Lanczos recurrence
- Lanczos tridiagonalization
- Lanczos-FA
- Lanczos matrix functions
- finite precision Lanczos
- matrix-free Lanczos
source_guides:
- docs/algorithms/Lanczos.md
---

Build a Krylov basis and a tridiagonal compression of a symmetric operator.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

This page is an outline. A readable definition and reviewed pseudocode will be added here. Existing statements are listed below where they are indexed in the library.



## Uses and composed algorithms

Lanczos is a shared process. Its compression supports several tasks; evaluating a function or averaging random probes adds further algorithmic steps, represented by their own pages.

{{ generated:applications }}

## Statements in the library

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
