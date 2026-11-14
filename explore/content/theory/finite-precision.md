---
kind: theory
id: finite-precision
title: Rounding and finite-precision arithmetic
summary: Word arithmetic, relative and absolute error, representability, and accumulated rounding error.
status: outline
parents:
- computational-models
- matrix-analysis
prerequisites:
- matrix-norms
module_prefixes:
- NLAlib.Matrix.FinitePrecision.Machine
- NLAlib.Matrix.FinitePrecision.Rounding
- NLAlib.Matrix.FinitePrecision.EntrywiseRounding
- NLAlib.Matrix.FinitePrecision.VectorErrors
- NLAlib.Matrix.FinitePrecision.WordRepresentation
- NLAlib.Matrix.FinitePrecision.Traces
---

Arithmetic contracts specify how decoded word operations differ from ideal operations. Scalar roundoff, vector reductions, matrix applications, and range restrictions contribute different error terms; a numerical theorem states which combination it needs.

::: definition name="Relative error and absolute error floor"
A typical scalar error contract has the form

$$|\widehat z-z|\le u|z|+\eta,$$

where $u$ is a relative-error parameter and $\eta$ is an absolute-error floor. Setting $\eta=0$ is an additional choice, not a consequence of relative accuracy. Dot products with cancellation and matrix-vector products need their own accumulation bounds.
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
