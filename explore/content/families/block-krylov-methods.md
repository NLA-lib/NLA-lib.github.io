---
uid: 6760009f-4ad5-5e18-b867-ac458c1da459
kind: family
id: block-krylov-methods
title: Block Krylov methods
summary: Low-rank approximations from a block Krylov space that keeps every power applied to the start block.
status: ready
---

Block Krylov methods apply the operator repeatedly to a start block and keep every block, so the sampled range grows with the depth and the start block can be narrower than the target rank. Randomized block Krylov iteration (RBKI) projects a general matrix onto the block Krylov space; Nyström block Krylov iteration (NysBKI) uses the block Krylov test matrix for a positive-semidefinite matrix; late truncation of the completed approximation is a further step with its own output.

Each method below defines a mathematical output and has its own analysis. Follow a method for its guarantees and implementations. The Golub–Kahan process, a Krylov factorization, computes factors of the block Krylov projection. Methods that keep only the last power are subspace iteration methods.

## Methods

{{ generated:algorithms }}

## Appears under these tasks

{{ generated:task-membership }}
