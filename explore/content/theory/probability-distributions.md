---
kind: theory
id: probability-distributions
title: Distributions, moments, and random probes
summary: Gaussian, Rademacher, chi-square, isotropy, and moment estimates.
status: outline
parents:
- probability
prerequisites: []
module_prefixes:
- NLAlib.Probability.Distributions
- NLAlib.Probability.Isotropic
- NLAlib.Probability.Orlicz
- NLAlib.ForMathlib.Probability.Distributions.Beta
- NLAlib.ForMathlib.Probability.Distributions.ChiSquared
---

Moments and distributional assumptions are the inputs to randomized error analysis. In particular, isotropy explains why random quadratic forms can estimate a trace, while higher moments and independence determine variance and tail behavior.

::: definition name="Isotropic probes"
A square-integrable probe $\mathbf g$ is isotropic when $\mathbb E[\mathbf g\mathbf g^{\mathsf{H}}]=\mathbf I$. Standard real Gaussian and independent Rademacher probes are common examples. Isotropy specifies a second moment; it does not itself assert independent coordinates or independent probes.
:::

## Background

{{ generated:prerequisites }}

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
