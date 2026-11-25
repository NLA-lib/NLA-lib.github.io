---
uid: 9b00024d-5ef6-59fe-9f78-62175ef21b3f
kind: task
id: sketching
title: Sketching and embeddings
summary: Compress vectors, matrices, or subspaces while preserving selected geometry.
status: ready
sections_collapsed: true
order: 7
theory:
- subspaces
- probability
- concentration
groups:
- id: sparse
  title: Sparse embeddings
  summary: Apply a sketch with very few nonzero entries per input coordinate.
  algorithms:
  - countsketch
- id: structured
  title: Structured orthogonal embeddings
  summary: Combine random signs, an orthogonal transform, and subsampling.
  algorithms:
  - srht
---

Compress vectors, matrices, or subspaces while preserving selected geometry.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
