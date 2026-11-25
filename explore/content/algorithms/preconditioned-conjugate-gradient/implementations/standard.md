---
uid: 8022b33f-300a-5c7b-8ed8-af94fa11a561
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

These rounded results are for a program that starts from $\mathbf{x}_0=\mathbf 0$, not for the listing above. `Krylov.CG.HSPCG.Rounded.solve` assumes that the supplied iterate is zero, and `Krylov.CG.HSPCG.Rounded.zeroStart` first writes that zero iterate; the stored scalar certificates are for the program lowered from `zeroStart`. A rounded certificate for a general starting guess is not presented.
