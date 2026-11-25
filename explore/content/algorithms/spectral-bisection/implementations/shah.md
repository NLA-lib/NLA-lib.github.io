---
uid: c4c95246-b768-591e-9acc-0d7479c59c31
kind: implementation
id: shah
algorithm: spectral-bisection
title: Randomized, finite precision
summary: Shah's Hermitian eigensolver with an explicit precision bound, stored-word arithmetic, and certified resources.
status: ready
library_algorithm: spectral-bisection
library_results: false
arithmetic_models:
- id: float-machine
  title: Floating-point machine, Shah's contract
search_aliases:
- Randomized spectral bisection
result_ids:
- spectral-bisection-diagonalization
- spectral-bisection-diagonalization-bits
- spectral-bisection-diagonalization-simple
order: 0
source_guides:
- docs/algorithms/Spectral-Bisection.md
---

Diagonalize a stored Hermitian matrix $\mathbf{A}\in\mathbb C^{n\times n}$ by splitting its spectrum, solving the smaller problems, and assembling a basis $\mathbf{U}$ and real values $\mathbf{d}$. This implementation follows Shah's randomized spectral-bisection method.

The [precision bound](#precision) grows logarithmically in dimension, inverse error tolerance, and inverse failure probability.

{{ generated:source-guides }}

## Algorithm

{{ statement:nlalib-spectralbisection-bisectionprogram-c1b568f6 }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The dense word model supplies scalar arithmetic and decoding, matrix multiplication, full QR, comparisons, bounded integer conversions, and explicit random draws. Scalar transformations, copies, control flow, and allocation are counted separately. This is a parameterized arithmetic model; a concrete floating-point format must establish the primitive accuracy and range assumptions.

Matrix multiplication and QR have supplied work and workspace costs. The bounds below count abstract scalar cells, rather than bytes. Complex matrix entries occupy two cells.

## Operations and Storage

Write $T(k)$ for a monotone, superadditive bound on a matrix primitive whose largest dimension is $k$. Require this bound for every primitive shape, including zero dimensions. Let $\mathcal{H}(n,L,c)$ denote the static program budget with matrix-kernel work set to zero: it includes scalar arithmetic, sampling, literals, queries, addressing, control flow, frames, and allocation.

{{ statement:nlalib-spectralbisection-certifies-work }}

This work bound uses the supplied primitive costs. Counting bit operations additionally requires bit costs for scalar arithmetic, matrix multiplication, QR, and sampling; the precision requirement below specifies how accurately those primitives must operate.

Let $E(n)$ be the maximum workspace cost of multiplication and QR over all call dimensions at most $n$; no monotonicity of workspace is required.

{{ statement:nlalib-spectralbisection-staticpeak-workspaceenvelope-le }}

{{ statement:nlalib-spectralbisection-initialbytes-add-staticpeak-workspaceenvelope-le }}

## Accuracy

{{ statement:nlalib-spectralbisection-bisectionroutine-meets }}

{{ statement:nlalib-floatmachine-isaccurate-measurereal-not-isapproxdiagonalization-eigh-bisectiondepth-le-of-logb-le-of-haslaw-eighsamplelaw }}

The precision theorem concerns the numerical reference. The next theorem transfers a reference guarantee to the stored-word execution when its arithmetic and random tape realize those assumptions.

{{ statement:nlalib-spectralbisection-measurereal-not-accepts-le-of-wordspecification }}

The last theorem states the work as an explicit polynomial and combines it with the accuracy guarantee, with the precision hypotheses stated for the machine itself.

{{ statement:spectral-bisection-operation-count-accuracy }}

## Further numerical results

{{ generated:results }}

## Mathematical method

{{ generated:mathematical-method }}
