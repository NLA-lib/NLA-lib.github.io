---
kind: theory
id: best-rank-approximation
title: Best-rank approximation and truncation
summary: Truncated SVD, Eckart–Young optimality, and error bounds for projection and
  truncation.
status: outline
parents:
- matrix-analysis
prerequisites:
- singular-values
- subspaces
---

This topic contains reusable approximation theory. The choices of when to truncate a sketch or an approximation belong to the individual RSVD method pages.

::: definition decl:NLAlib.truncatedSVD name="Truncated SVD"
Write $[\mathbf A]_k$ for the matrix obtained by retaining the $k$ largest singular values and their singular vectors. It has rank at most $k$. Ties can make the best approximation nonunique; the library fixes a choice.
:::

## Background

{{ generated:prerequisites }}

## Used by algorithms

{{ generated:used-by }}
