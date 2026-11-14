---
kind: theory
id: finite-precision-krylov
title: Finite-precision Krylov analysis
summary: Local recurrence defects, backward models, residual gaps, Paige bounds, and rounded matrix-function
  estimates.
status: outline
parents:
- finite-precision
- krylov-spaces
module_prefixes:
- NLAlib.Krylov.FinitePrecision
---

Rounded Krylov methods can lose orthogonality and differ from their exact-arithmetic counterparts. These mathematical run models quantify local defects, backward interpretations, and their spectral or matrix-function consequences. They are not execution certificates: an implementation must separately establish that its returned data satisfy the selected model.

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
