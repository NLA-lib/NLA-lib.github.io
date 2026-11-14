---
kind: algorithm
id: svd
title: Singular-value decomposition
summary: Construct singular values and left and right singular vectors.
status: outline
order: 25
theory:
- singular-values
- matrix-factorization-theory
families:
- matrix-factorizations
library_results: false
result_ids:
- svd-existence
- svd-uniqueness
- eckart-young-frobenius
- eckart-young-spectral
---

Construct singular values and left and right singular vectors.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Singular-value decomposition"
A singular-value decomposition is $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^{\mathsf{H}}$, with unitary factors $\mathbf U,\mathbf V$ and a rectangular diagonal matrix $\mathbf\Sigma$ containing nonnegative singular values in decreasing order. Retaining the leading $k$ singular components defines a rank-at-most-$k$ truncation. The decomposition and its truncation are mathematical objects; concrete SVD algorithms have separate execution and accuracy questions.
:::



## Mathematical guarantees

::: theorem result:eckart-young-frobenius name="Optimal rank truncation"
For every comparison matrix $\mathbf B$ with rank at most $k$,

$$\|\mathbf A-[\mathbf A]_k\|_{\mathrm F}\le\|\mathbf A-\mathbf B\|_{\mathrm F}.$$

Thus retaining the leading singular components gives a best rank-at-most-$k$ approximation in Frobenius norm. A separate checked result gives the spectral-norm optimum.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
