---
kind: theory
id: spectral-theory
title: Spectral theory
summary: The spectral theorem, eigenvalue variational principles, interlacing, and positive definiteness.
status: outline
order: 2
parents:
- matrix-analysis
module_prefixes:
- NLAlib.Matrix.Spectral.Eigenvalues
- NLAlib.Matrix.Spectral.EigenvalueListing
- NLAlib.Matrix.Spectral.CourantFischer
- NLAlib.Matrix.Spectral.Interlacing
- NLAlib.Matrix.Spectral.Diagonalizable
- NLAlib.Matrix.Spectral.Normal
- NLAlib.Matrix.Spectral.Schur
- NLAlib.Matrix.Spectral.RealSchur
- NLAlib.Matrix.Spectral.SylvesterCriterion
- NLAlib.Matrix.Spectral.SpectralRadius
---

Spectral theory connects a matrix to its eigenvalues, eigenvectors, and invariant subspaces. Hermitian structure makes this connection especially strong: the eigenvalues are real and an orthonormal eigenbasis is available.

::: definition name="Hermitian spectral decomposition"
A Hermitian matrix satisfies $\mathbf A^{\mathsf{H}}=\mathbf A$. Its spectral decomposition has the form $\mathbf A=\mathbf U\mathbf\Lambda\mathbf U^{\mathsf{H}}$, with unitary $\mathbf U$ and real diagonal $\mathbf\Lambda$. Variational principles characterize the ordered eigenvalues through subspaces; interlacing compares them with eigenvalues of compressions.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
