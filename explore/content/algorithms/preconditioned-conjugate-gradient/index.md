---
kind: algorithm
id: preconditioned-conjugate-gradient
title: Preconditioned CG (PCG)
summary: Apply conjugate gradients to a symmetrically preconditioned positive-definite
  system.
status: outline
order: 1
tasks:
- linear-systems
families:
- galerkin-methods
theory:
- krylov-spaces
- spectral-theory
library_algorithm: pcg
search_aliases:
- preconditioned CG
source_guides:
- docs/algorithms/Conjugate-Gradient.md
---

For a symmetric positive-definite matrix $\mathbf A$ and symmetric positive-definite inverse preconditioner $\mathbf C$, PCG corresponds to CG on

$$\mathbf C^{1/2}\mathbf A\mathbf C^{1/2}\mathbf y=\mathbf C^{1/2}\mathbf b,\qquad \mathbf x=\mathbf C^{1/2}\mathbf y.$$

The transformed spectrum governs convergence. The preconditioner changes the search spaces; the unpreconditioned CG statements should not be applied verbatim to PCG iterates.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Mathematical guarantees

These library results describe the mathematical PCG iterates. The implementation page establishes that its stored output is exactly the specified iterate; convergence and approximation results are collected here.

{{ generated:results }}



## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}
