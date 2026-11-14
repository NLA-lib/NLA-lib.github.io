---
kind: theory
id: matrix-inequalities
title: Matrix inequalities and majorization
summary: Loewner order, determinant inequalities, majorization, and Ky Fan and Lidskii bounds.
status: outline
parents:
- matrix-analysis
prerequisites:
- matrix-norms
- spectral-theory
module_prefixes:
- NLAlib.Matrix.Inequalities
- NLAlib.Matrix.Majorization
---

Matrix inequalities compare operators, their spectra, or scalar quantities such as trace and determinant. Keeping these comparisons distinct makes their hypotheses easier to read.

::: definition name="Loewner order and majorization"
For Hermitian matrices, $\mathbf A\preceq\mathbf B$ means $\mathbf x^{\mathsf{H}}(\mathbf B-\mathbf A)\mathbf x\ge0$ for every vector $\mathbf x$. Majorization instead compares partial sums of ordered scalar lists, such as eigenvalues or singular values. A statement about one of these orders does not automatically imply a statement about every other matrix quantity.
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
