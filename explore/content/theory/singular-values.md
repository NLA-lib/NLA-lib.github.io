---
kind: theory
id: singular-values
title: Singular values
summary: Singular-value decompositions, Weyl inequalities, interlacing, and best-rank approximation.
status: outline
order: 3
parents:
- matrix-analysis
prerequisites:
- matrix-norms
module_prefixes:
- NLAlib.Matrix.Spectral.SVD
- NLAlib.Matrix.Spectral.SingularValues
- NLAlib.Matrix.Spectral.SingularValueInequalities
- NLAlib.Matrix.Spectral.LeastSingularValue
result_ids:
- weyl-singular-values
---

Singular values describe how a matrix stretches vectors. They organize rank, conditioning, and low-rank approximation without requiring the matrix to be square or Hermitian.

::: definition name="Singular values"
The singular values of $\mathbf A$ are the nonnegative square roots of the eigenvalues of $\mathbf A^{\mathsf{H}}\mathbf A$, listed in decreasing order and with the appropriate zero padding. Equivalently, they are the diagonal values in a singular-value decomposition. A positive singular value represents an active direction; small singular values identify directions sensitive to perturbation or truncation.
:::

## Background

{{ generated:prerequisites }}

## Mathematical guarantees

::: theorem result:weyl-singular-values name="Perturbation of singular values"
For matrices $\mathbf A,\mathbf B$ of the same shape and every singular-value index $j$,

$$|\sigma_j(\mathbf A)-\sigma_j(\mathbf B)|\le\|\mathbf A-\mathbf B\|_2.$$

A spectral-norm perturbation therefore bounds the change of each ordered singular value by the same amount.
:::

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
