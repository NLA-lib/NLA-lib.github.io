---
uid: 4a911f62-1c69-5569-b402-2ad58b5b9fc9
kind: algorithm
id: deflation
title: Randomized subspace extraction (deflation)
summary: Project a random sample through a matrix and extract a basis using QR.
status: outline
order: 28
theory:
- subspaces
- spectral-theory
library_algorithm: deflate
search_aliases:
- DEFLATE
- Gaussian range finder
- randomized range finder without oversampling
source_guides:
- docs/algorithms/Sign-Deflation.md
uses:
- qr
---

The deflation component used by spectral bisection extracts a basis from a sampled matrix image. It is distinct from locking already converged eigenvectors in an iterative eigensolver.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

{{ statement:randomized-subspace-extraction-a0a6bea3 }}



## Results

{{ generated:results }}

## Components

{{ generated:components }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
