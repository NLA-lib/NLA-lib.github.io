---
kind: family
id: galerkin-methods
title: Galerkin methods
summary: Choose a Krylov approximation by requiring its residual to be orthogonal
  to the trial space.
status: ready
order: 0
tasks:
- linear-systems
source_guides:
- docs/algorithms/Conjugate-Gradient.md
---

Galerkin methods choose an approximate solution from a trial space and require the residual to be orthogonal to that space. CG specializes this principle to a positive-definite system; FOM uses the full Krylov basis for a general square system. Preconditioning and block right-hand sides give further methods, each with its own mathematical definition.

{{ generated:source-guides }}

## Methods

{{ generated:algorithms }}
