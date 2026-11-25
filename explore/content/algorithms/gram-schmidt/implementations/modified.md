---
uid: b1de29e7-6914-5ba0-8297-0b309905a35a
kind: implementation
id: modified
algorithm: gram-schmidt
title: Modified Gram–Schmidt
summary: Orthogonalize the stored columns in place, updating each residual after every projection.
status: ready
order: 1
arithmetic_models:
- id: exact
  arithmetic: exact
source_guides:
- docs/algorithms/Gram-Schmidt.md
---

The checked program overwrites an $n\times m$ input matrix with the mathematical Gram–Schmidt columns. Dependent columns are allowed: a zero residual stays zero. This endpoint returns the basis matrix, rather than storing a triangular coefficient matrix.

{{ generated:source-guides }}

## Algorithm

{{ statement:nlalib-mgs-factorprogram-8f827d72 }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

This page presents exact real or complex field arithmetic with Hermitian dot products, vector updates, division by a scalar, square roots, and real-part comparisons. The primitive contracts permit the in-place column views used by the program. The normalization guard handles dependent columns and zero dimensions.

A cell is one abstract field value. Translating a complex value to physical real/imaginary storage is a separate representation choice.

## Operations and Storage

The column sweeps make $m(m-1)/2$ projection dot products, the same number of vector updates and scalar negations, and $m$ additional self-dot products. There are $m$ zero literals and equality tests, and at most $m$ square roots and vector normalizations. For $n,m\ge1$, with linear-cost length-$n$ vector primitives, numerical work is $O(nm^2)$. The canonical certificate also covers zero dimensions and counts structural instructions.

{{ statement:nlalib-mgs-factor-peak-le }}

## Accuracy

{{ statement:nlalib-mgs-factorroutine-meets }}

## Mathematical method

{{ generated:mathematical-method }}
