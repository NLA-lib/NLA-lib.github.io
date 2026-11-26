---
uid: f430e970-924b-50f8-8c08-f3c99a3ca720
kind: algorithm
id: lu
title: LU factorization
summary: Factor a matrix into lower- and upper-triangular factors without row permutations.
status: ready
theory:
- subspaces
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- lu-existence
- lu-row-inclusion
---

{{ statement:lu-factorization-a7033c37 }}

Unpivoted LU writes $A=LU$ with a unit lower-triangular factor and an upper-triangular factor. The scalar and blocked stored implementations below require nonzero canonical Gaussian pivots of the original matrix. Their pages give the actual instruction listings and certified work/storage bounds; the blocked routine uses scalar matrix-product updates.

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

The results below give mathematical existence, inclusion, and pivoting guarantees. Stored execution, arithmetic assumptions, and resource certificates are presented on the implementation pages.

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
