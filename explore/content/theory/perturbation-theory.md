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

For a non-Hermitian matrix no such linear bound holds: a Jordan block of order $n$ perturbed by $\varepsilon$ in one corner has eigenvalues of modulus $\varepsilon^{1/n}$. The Ostrowski–Elsner theorem shows that this root is the worst case, for every matrix, with a matching of the two spectra.

::: theorem decl:NLAlib.exists_isEigenvalueListing_norm_sub_le_rpow name="Ostrowski–Elsner matching" id=ostrowski-elsner
For complex matrices $\mathbf A,\mathbf A'$ of order $n+1$ and every listing $\lambda_0,\dots,\lambda_n$ of the eigenvalues of $\mathbf A$ with multiplicity, there is a listing $\lambda'_0,\dots,\lambda'_n$ of those of $\mathbf A'$ with

$$|\lambda'_i-\lambda_i|\le(2n+1)\bigl(\|\mathbf A\|_2+\|\mathbf A'\|_2\bigr)^{1-1/(n+1)}\|\mathbf A'-\mathbf A\|_2^{1/(n+1)}$$

for every $i$.
:::

This is Lemma 1.2 of Banks, Garza-Vargas and Srivastava, *Global convergence of Hessenberg shifted QR III*. The constant $2n+1$ comes from an argument over the connected components of the union of disks around the eigenvalues; Bhatia, Elsner and Krause have the constant $4$. The [randomized shifted inverse iteration (BGS III)](/explore/algorithms/inverse-iteration/implementations/small-eig/) uses it to turn a backward error into a forward error for the eigenvalues: a backward error $\delta_b$ gives a forward error of order $\delta_b^{1/(n+1)}$.

::: theorem decl:NLAlib.exists_isEigenvalueListing_norm_sub_le_of_class name="Forward error through a diagonalizable matrix"
Let $\mathbf A+\mathbf E_1=\mathbf V\operatorname{diag}(\mathbf d)\mathbf V^{-1}$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le B$ and eigenvalues separated by $g>0$, and let $\|\mathbf E_2\|_2\le g/(16(n+1)B)$. Then every listing $\mathbf r$ of the eigenvalues of $\mathbf A+\mathbf E_1+\mathbf E_2$ is matched to a listing $\boldsymbol\lambda$ of those of $\mathbf A$ with

$$|r_i-\lambda_i|\le B\|\mathbf E_2\|_2+(2n+1)\bigl(2\|\mathbf A\|_2+\|\mathbf E_1\|_2\bigr)^{1-1/(n+1)}\|\mathbf E_1\|_2^{1/(n+1)}$$

for every $i$. The first term is the Bauer–Fike perturbation of the diagonalizable matrix; the second is the Ostrowski–Elsner matching for the rest.
:::

Random perturbations make these hypotheses likely: see [pseudospectral shattering and Gaussian regularization](/explore/theory/pseudospectral-shattering/).

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
