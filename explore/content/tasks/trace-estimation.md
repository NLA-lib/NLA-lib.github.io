---
kind: task
id: trace-estimation
title: Estimate traces and spectral statistics
summary: Estimate $\operatorname{tr}(A)$, $\operatorname{tr}(f(A))$, and related quantities.
status: ready
order: 5
theory:
- probability
- concentration
- orthogonal-polynomials
groups:
- id: probes
  title: Random-probe estimators
  summary: Average random quadratic forms to estimate the trace.
  algorithms:
  - girard-hutchinson
- id: variance-reduction
  title: Low-rank variance reduction
  summary: Capture a low-rank part and estimate the trace of the residual.
  algorithms:
  - hutchpp
- id: spectral-functions
  title: Spectral-function traces
  summary: Combine random probes and quadrature to approximate traces of matrix functions and related
    spectral statistics.
  algorithms:
  - stochastic-lanczos-quadrature
  - probe-spectral-estimation
- id: building-blocks
  title: Shared Krylov construction
  summary: Lanczos supplies a compression to stochastic quadrature; it is not a trace estimator by itself.
  algorithms:
  - lanczos
  summaries:
    lanczos: Build the small tridiagonal matrix used for each probe in stochastic Lanczos quadrature.
---

Estimate $\operatorname{tr}(A)$, $\operatorname{tr}(f(A))$, and related quantities.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
