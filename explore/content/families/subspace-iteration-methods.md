---
uid: 10698c1d-b514-5dc3-a091-6f0a9edf980f
kind: family
id: subspace-iteration-methods
title: Subspace iteration methods
summary: Range approximations from a test matrix multiplied by a power, or another polynomial filter, of the operator.
status: ready
---

Randomized subspace iteration (RSI) applies a power of $\mathbf{A}^{\mathsf{H}}\mathbf{A}$, or of a positive-semidefinite $\mathbf{A}$, to a test matrix and keeps only that last block. The sampled range has the width of the test matrix. A general polynomial filter replaces the power; Nyström subspace iteration (NysSI) uses the powered test matrix in a Nyström approximation; late truncation of the completed approximation is a further step with its own output.

Each method below defines a mathematical output and has its own analysis. Follow a method for its guarantees and implementations. Methods that keep every power in the sampled range are block Krylov methods.

## Methods

{{ generated:algorithms }}

## Appears under these tasks

{{ generated:task-membership }}
