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
library_algorithm: pcg
search_aliases:
- preconditioned CG
---

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm


Apply a supplied inverse preconditioner in the CG recurrence.

{{ generated:cg-definition }}

## Operations and Storage

{{ generated:cg-resources }}

## Accuracy

{{ generated:cg-accuracy }}
