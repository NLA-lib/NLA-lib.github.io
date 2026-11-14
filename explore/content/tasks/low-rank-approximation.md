---
kind: task
id: low-rank-approximation
title: Build low-rank approximations
summary: Approximate a matrix by a small-rank factorization or structured surrogate.
status: ready
order: 3
theory:
- singular-values
- matrix-norms
- random-matrices
groups:
- id: range-finders
  title: RSVD-type methods
  summary: Choose a sketched range, with separate choices for truncating the sketch and the final approximation.
  algorithms:
  - randomized-svd
  - late-truncated-rsvd
  - early-truncated-rsvd
  - early-and-late-truncated-rsvd
  family: rsvd-type-methods
- id: filtered-ranges
  title: Iterated and filtered range finders
  summary: Improve the sampled range with repeated applications, a Krylov space, or a polynomial filter.
  algorithms:
  - rsi
  - rbki
  - filtered-randomized-svd
- id: nystrom
  title: Nyström methods for PSD matrices
  summary: Approximate a positive-semidefinite matrix from sampled or sketched columns.
  algorithms:
  - nystrom
  - nyssi
  - nystrom-bki
- id: generalized-nystrom
  title: Generalized Nyström (GN)
  summary: Use two-sided sketches for a general rectangular matrix, with distinct early and late truncation
    choices.
  algorithms:
  - generalized-nystrom
  - late-truncated-generalized-nystrom
  - early-truncated-generalized-nystrom
  family: generalized-nystrom-methods
- id: deterministic
  title: Singular-value truncation
  summary: Use singular values to define a best low-rank approximation and a deterministic reference for
    randomized methods.
  algorithms:
  - svd
  - pivoted-cholesky
  summaries:
    svd: Retain the leading singular components to form a best rank-at-most-k approximation.
---

Approximate a matrix by a small-rank factorization or structured surrogate.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
