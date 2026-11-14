---
kind: theory
id: matrix-functions
title: Matrix functions and operator inequalities
summary: Matrix exponentials, logarithms, sign, and operator monotonicity, including Golden–Thompson and
  Lieb.
status: outline
parents:
- matrix-analysis
prerequisites:
- spectral-theory
- matrix-norms
module_prefixes:
- NLAlib.Matrix.Functions
---

Functions of matrices extend scalar functions to operators. Matrix exponentials, logarithms, powers, and sign functions have different domains; operator inequalities compare their behavior under matrix order.

::: definition name="Hermitian functional calculus"
For Hermitian $\mathbf A=\mathbf U\mathbf\Lambda\mathbf U^{\mathsf{H}}$ and a function $f$ defined on its spectrum, set

$$f(\mathbf A)=\mathbf U\operatorname{diag}(f(\lambda_1),\ldots,f(\lambda_n))\mathbf U^{\mathsf{H}}.$$

The expression is independent of the chosen eigenbasis. Domain restrictions, such as positive definiteness for a real logarithm, are part of each statement.
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
