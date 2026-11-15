---
kind: task
id: quadrature
title: Quadrature and quadratic forms
summary: Approximate integrals and quantities such as $b^{\mathsf T}f(A)b$.
status: ready
order: 6
theory:
- orthogonal-polynomials
- spectral-theory
groups:
- id: deterministic
  title: Lanczos quadrature
  summary: Approximate a quadratic form through the spectral measure associated with a starting vector.
  algorithms:
  - lanczos-quadrature
- id: stochastic
  title: Stochastic quadrature
  summary: Repeat quadrature over random probes to estimate spectral statistics.
  algorithms:
  - stochastic-lanczos-quadrature
- id: recurrences
  title: Shared recurrence
  summary: The common tridiagonal compression connects Krylov bases with orthogonal polynomials and quadrature
    nodes.
  algorithms:
  - lanczos
  summaries:
    lanczos: Generate the tridiagonal recurrence underlying the quadrature rule.
---

Approximate integrals and quantities such as $b^{\mathsf T}f(A)b$.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
