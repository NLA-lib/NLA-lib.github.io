---
kind: algorithm
id: stochastic-lanczos-quadrature
title: Stochastic Lanczos quadrature
summary: Average Lanczos-based quadrature over random probes to estimate spectral quantities.
status: outline
order: 4
theory:
- orthogonal-polynomials
- random-matrices
library_algorithm: stochastic-lanczos-quadrature
uses:
- lanczos-quadrature
---

Average Lanczos-based quadrature over random probes to estimate spectral quantities.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Stochastic Lanczos quadrature"
For $s\ge1$ random probes, approximate each quadratic form $\mathbf g_i^{\mathsf{H}}f(\mathbf A)\mathbf g_i$ by Lanczos quadrature and average the results. Isotropic probes connect their average to a spectral-function trace. Sampling error and quadrature error are distinct contributions; both must be controlled to obtain a trace-estimation guarantee.
:::



## Components

{{ generated:components }}

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
