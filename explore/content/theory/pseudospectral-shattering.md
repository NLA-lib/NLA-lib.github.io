---
uid: 44142ca3-3907-580b-a6f1-2ef8f99e51c1
kind: theory
id: pseudospectral-shattering
title: Pseudospectral shattering and Gaussian regularization
summary: A small complex Gaussian perturbation makes a matrix diagonalizable with a bounded eigenvector condition number and separated eigenvalues, with polynomial tails.
status: outline
order: 16
parents:
- random-matrices
- perturbation-theory
prerequisites:
- singular-values
- spectral-theory
module_prefixes:
- NLAlib.RandomMatrix.Shattering
search_aliases:
- Pseudospectral shattering
- Ginibre perturbation
- Gaussian regularization
- Eigenvector condition number tail
- Eigenvalue gap tail
---

A matrix can have eigenvalues that are arbitrarily ill conditioned, or no basis of eigenvectors at all. A small random perturbation removes both problems with high probability. For a deterministic $\mathbf{M}$ of order $n$, a scale $\gamma>0$ and a standard complex Gaussian matrix $\mathbf{G}$ (independent entries of mean square modulus one), the perturbation

$$\mathbf{M}+\gamma n^{-1/2}\mathbf{G}$$

has, outside an event of small probability, simple eigenvalues with all gaps above $t$ and an eigenvector matrix $\mathbf{V}$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le1/t$. This is *pseudospectral shattering* (Banks, Garza-Vargas, Kulkarni and Srivastava): the $\varepsilon$-pseudospectrum splits into small components, one around each eigenvalue. Randomized eigensolvers such as the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/) perturb their input in this way, so that every later step can assume a diagonalizable matrix with a known condition number and eigenvalue separation.

The library proves the two tails in an elementary polynomial form. Its exponents are weaker than the printed ones, and the tails are stated so that sharper ones can replace them. This page collects the tails and the deterministic and probabilistic facts they are built from. It is meant to grow as further results are added.

## The two tails

{{ statement:nlalib-measurereal-not-exists-iseigenvaluelisting-le-le-log-sq-of-haslaw-complexgaussianmatrix }}

This is a weaker polynomial form of Lemma B.1 of BGS III. The exponent of $t/\gamma$ is $2/3$ here and $2$ in the source. The proof covers a disk containing the spectrum by a net of $36(R/t)^2$ points. Two eigenvalues close to a net point force a small second-smallest singular value (see [eigenvalue clustering](#clustering) below), whose tail is of fourth order. The proof then combines the condition tail below at the cutoff $(\gamma/(nt))^{1/3}$, which balances the net term against the condition tail, with a norm cutoff.

{{ statement:nlalib-measurereal-not-exists-pseudoconditionnumber-le-le-log-sq-of-haslaw-complexgaussianmatrix }}

This is Theorem 1.5 of Banks, Kulkarni, Mukherjee and Srivastava in a polynomial-tail form. The proof integrates the area of the $\varepsilon$-pseudospectrum inside a disk over the Gaussian law, using Fubini and the shifted smallest-singular-value tail. Fatou's lemma bounds the expected lower limit of the normalized areas. A matrix without a good diagonalizer has a large lower limit, by the [pseudospectral area inequality](#area-inequality), so Markov's inequality applies without choosing eigenvectors measurably.

{{ statement:nlalib-measurereal-not-exists-class-le-of-haslaw-complexgaussianmatrix }}

The tails are recorded as four numbers $(C,a,b,c)$, the bound $C\,n^a\,s^b\,(K+\log(1/s))^c$ (`PolyLogTail`). The predicates `BoundsGinibreGap` and `BoundsGinibreCondition` say that a record bounds the gap or the condition tail. The library proves them for the records `ginibreGapTail` $=(2048e,11/3,2/3,2)$ and `ginibreConditionTail` $=(128e,3,2,2)$ (`boundsGinibreGap_ginibreGapTail`, `boundsGinibreCondition_ginibreConditionTail`). The theorems that use the tails take a record as a hypothesis, and each has an unconditional corollary at the proved records. So a sharper tail, such as the printed gap exponent $2$, plugs in without changing them.

## Ingredients

### Small balls and singular values

{{ statement:nlalib-measurereal-norm-mulvec-add-le-le-of-haslaw-complexgaussianvector }}

{{ statement:nlalib-measurereal-singularvalues-add-smul-le-le-exp-one-mul-of-haslaw-complexgaussianmatrix }}

The source of this bound is Lemma 3.3 of Banks, Kulkarni, Mukherjee and Srivastava, which has constant $1$ in place of $e$. The proof here is the probe argument of Sankar, Spielman and Teng, in its complex version.

{{ statement:nlalib-measurereal-singularvalues-add-smul-le-le-pow-four-of-haslaw-complexgaussianmatrix }}

### Pseudospectral area

{{ statement:nlalib-ofreal-sum-sq-le-liminf-measure-inter-ball-of-mul-eq-mul-diagonal }}

{{ statement:nlalib-ofreal-sq-div-card-le-liminf-measure-inter-ball-of-not-exists }}

Both are Lemmas 3.1 and 3.2 of Banks, Kulkarni, Mukherjee and Srivastava, with the sufficient factor $4$ of the local area estimate.

### Eigenvalue clustering

{{ statement:nlalib-singularvalues-le-mul-pseudoconditionnumber-of-mul-eq-mul-diagonal }}

{{ statement:nlalib-exists-mem-singularvalues-le-of-not-exists-iseigenvaluelisting }}

### Simple spectrum

{{ statement:nlalib-ae-charpoly-separable-of-haslaw-complexgaussianmatrix }}

## Formal definitions

{{ generated:definitions }}

## Background

{{ generated:prerequisites }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
