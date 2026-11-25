---
uid: 2facc04c-dcf6-5873-80cb-49863e025a58
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

{{ statement:residuals-and-spectral-separation-5979b536 }}

## Background

{{ generated:prerequisites }}

## Mathematical guarantees

{{ statement:weyl-perturbation }}

For a non-Hermitian matrix no such linear bound holds: a Jordan block of order $n$ perturbed by $\varepsilon$ in one corner has eigenvalues of modulus $\varepsilon^{1/n}$. The Ostrowski–Elsner theorem shows that this root is the worst case, for every matrix, with a matching of the two spectra.

{{ statement:nlalib-exists-iseigenvaluelisting-norm-sub-le-rpow }}

This is Lemma 1.2 of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR III*. The constant $2n+1$ comes from an argument over the connected components of the union of disks around the eigenvalues; Bhatia, Elsner and Krause have the constant $4$. The [randomized shifted inverse iteration (BGS III)](/explore/algorithms/inverse-iteration/implementations/small-eig/) uses it to turn a backward error into a forward error for the eigenvalues: a backward error $\delta_b$ gives a forward error of order $\delta_b^{1/(n+1)}$.

{{ statement:nlalib-exists-iseigenvaluelisting-norm-sub-le-of-class }}

Random perturbations make these hypotheses likely: see [pseudospectral shattering and Gaussian regularization](/explore/theory/pseudospectral-shattering/).

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
