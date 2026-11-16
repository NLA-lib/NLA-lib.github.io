---
kind: implementation
id: standard
algorithm: preconditioned-conjugate-gradient
title: Standard PCG recurrence
summary: Apply a supplied inverse preconditioner in the CG recurrence.
status: ready
order: 1
renderer: cg
source_variant: pcg
arithmetic_models:
- id: exact
  arithmetic: exact
  program: blas-matvec
library_algorithm: pcg
search_aliases:
- preconditioned CG
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm


Apply a supplied inverse preconditioner in the CG recurrence.

{{ generated:cg-definition }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

## Operations and Storage

{{ generated:cg-resources }}

## Accuracy

{{ generated:cg-accuracy-exact }}

## Not yet presented

{{ generated:cg-coverage }}
