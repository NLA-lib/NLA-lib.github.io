---
uid: bf5523d0-125e-5ad7-a567-aeacc945d7de
kind: algorithm
id: pluq
title: PLUQ factorization
summary: Factor a matrix after independent row and column pivoting.
status: ready
theory: [subspaces, matrix-factorization-theory]
families: [matrix-factorizations]
library_results: false
search_aliases:
- complete pivoting
- rook pivoting
- Gaussian elimination with complete pivoting
---

PLUQ factorization permits both row and column exchanges during elimination. The stored routines return unit lower and upper factors together with two independent current-position swap histories. If their composed permutations are $P$ and $C$, the exact convention is $A_{P(i),C(j)}=(LU)_{ij}$.

## Implementations

{{ generated:implementations }}

Complete pivoting scans the active square for its first maximum. Rook pivoting alternates active column and row scans with a proved finite bound. Both implementation pages expose exact and standard-rounding models of the actual same scalar listing, with singular and empty inputs included. Selection rules, arithmetic hypotheses, componentwise error, and actual work and storage bounds belong to those pages.

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
