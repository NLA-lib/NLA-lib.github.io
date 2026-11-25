---
uid: ae9329d5-32a2-530c-95d4-2229650f11b0
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

{{ statement:relative-error-and-absolute-error-floor-293c93c0 }}

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
