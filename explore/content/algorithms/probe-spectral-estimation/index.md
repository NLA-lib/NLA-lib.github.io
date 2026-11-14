---
kind: algorithm
id: probe-spectral-estimation
title: Probe spectral estimation
summary: Estimate a Hermitian matrix spectral measure with isotropic random probes.
status: outline
result_ids:
- probe-spectral-measure-unbiased
- spectral-density-kolmogorov-tail
- spectral-density-lipschitz-tail
theory:
- spectral-theory
- probability
- orthogonal-polynomials
---

::: definition name="Probe spectral estimation"
For a Hermitian $n\times n$ matrix and $s$ probes, average their spectral measures with normalization $1/(ns)$. With isotropic probes, the expected measure equals the empirical eigenvalue measure. Lanczos quadrature provides finite-step approximations to the probe measures; its error must be accounted for separately.
:::

## Results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
