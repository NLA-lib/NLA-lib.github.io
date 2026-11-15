---
kind: task
id: low-rank-approximation
title: Low-rank approximation
summary: Approximate a matrix by a small-rank factorization or structured surrogate.
status: ready
sections_collapsed: true
result_ids:
- range-recovery-k-queries
- fixed-batch-low-rank-lower-bound
- fixed-batch-nuclear-lower-bound
- one-pass-low-rank-lower-bound
- two-pass-low-rank-lower-bound
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
  title: Subspace iteration methods
  summary: Multiply the test matrix by a power, or another polynomial filter, of the operator before
    taking its range; only the last block is kept.
  algorithms:
  - rsi
  - late-truncated-rsi
  - filtered-randomized-svd
  summaries:
    filtered-randomized-svd: Replace the power by a general polynomial filter; its bound is the comparison
      behind the gapped subspace iteration and block Krylov bounds.
  family: subspace-iteration-methods
- id: block-krylov
  title: Block Krylov methods
  summary: Project onto a block Krylov space that keeps every power applied to the start block, with
    a separate choice for truncating the final approximation.
  algorithms:
  - rbki
  - late-truncated-rbki
  family: block-krylov-methods
- id: nystrom
  title: Nyström methods for PSD matrices
  summary: Approximate a positive-semidefinite matrix from sampled or sketched columns; the test matrix
    can be a plain sketch, a powered sketch, or a block Krylov matrix.
  algorithms:
  - nystrom
  - nyssi
  - late-truncated-nyssi
  - nystrom-bki
  - late-truncated-nystrom-bki
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

## Lower bounds

These bounds constrain every admissible algorithm within a stated access model: exact range recovery, fixed-batch approximation, and one- or two-pass approximation. Each statement specifies its query model and accuracy assumptions. Lower bounds for a particular algorithm appear on that algorithm's page.

{{ generated:results }}

## Mathematical background

{{ generated:theory }}
