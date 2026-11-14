---
kind: theory
id: perturbation-theory
title: Perturbation theory
summary: Davis–Kahan subspace bounds and perturbation of eigenvalues, singular values, and solutions.
status: outline
order: 5
parents:
- matrix-analysis
prerequisites:
- matrix-norms
- spectral-theory
module_prefixes:
- NLAlib.Matrix.Perturbation
result_ids:
- weyl-perturbation
- gram-defect-projector-distance
---

Perturbation bounds turn an error in a matrix or a computed equation into an error in an eigenvalue, singular value, or subspace. Values and subspaces behave differently: subspace bounds usually need a gap separating the spectral sets of interest.

::: definition name="Residuals and spectral separation"
For a candidate eigenpair $(\lambda,\mathbf x)$, the residual is $\mathbf r=\mathbf A\mathbf x-\lambda\mathbf x$. For a candidate diagonalization, a matrix residual is $\mathbf A\mathbf U-\mathbf U\mathbf\Lambda$. A small residual measures how well the equation is satisfied. Converting it to a distance from a particular invariant subspace requires the relevant spectral-separation assumptions.
:::

## Background

{{ generated:prerequisites }}

## Mathematical guarantees

::: theorem result:weyl-perturbation name="Perturbation of Hermitian eigenvalues"
For Hermitian matrices $\mathbf A,\mathbf B$ of the same dimension, with eigenvalues in the same ordering,

$$|\lambda_j(\mathbf A)-\lambda_j(\mathbf B)|\le\|\mathbf A-\mathbf B\|_2$$

for every index $j$. Controlling a matrix perturbation in spectral norm controls every ordered eigenvalue.
:::

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
