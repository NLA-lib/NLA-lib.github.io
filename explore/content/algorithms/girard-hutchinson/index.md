---
kind: algorithm
id: girard-hutchinson
title: Girard–Hutchinson trace estimator
summary: Estimate a trace using quadratic forms of random probes.
status: outline
order: 18
theory:
- probability
- random-matrices
library_algorithm: girard-hutchinson
library_results: false
result_ids:
- girard-hutchinson-tail
- girard-hutchinson-unbiased
- girard-hutchinson-variance
- hutchinson-variance-gaussian
- hutchinson-variance-rademacher
- rademacher-probe-optimality
---

Estimate a trace using quadratic forms of random probes.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.girardHutchinson name="Girard–Hutchinson estimator"
For $s\ge1$ probes $\mathbf g_1,\ldots,\mathbf g_s$, estimate the trace by

$$\widehat t=\frac1s\sum_{i=1}^s\mathbf g_i^{\mathsf{H}}\mathbf A\mathbf g_i.$$

The standard random estimator uses isotropic probes, such as independent Rademacher or standard Gaussian vectors. Variance and probability guarantees depend on the probe distribution and matrix assumptions.
:::



## Mathematical guarantees

::: theorem result:girard-hutchinson-unbiased name="Unbiased trace estimate"
For a nonempty collection of isotropic probes, the estimator has expectation

$$\mathbb E[\widehat t]=\operatorname{tr}(\mathbf A).$$

The probes need not be independent for this expectation identity. Independence and distribution-specific assumptions enter the variance and tail guarantees separately.
:::

## Further results

{{ generated:results }}

## Used by other algorithms

{{ generated:applications }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
