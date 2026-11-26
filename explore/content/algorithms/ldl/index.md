---
uid: 0ee54415-bb18-5e83-bc86-014eeb3c774d
kind: algorithm
id: ldl
title: Hermitian LDL factorization
summary: Factor a symmetric matrix into a unit lower factor, a diagonal, and the transpose factor.
status: ready
search_aliases: [LDLT, LDL transpose, symmetric indefinite factorization]
theory: [spectral-theory, matrix-factorization-theory]
families: [matrix-factorizations]
---

For a real symmetric matrix, LDL factorization seeks
$$\mathbf A=\mathbf L\operatorname{diag}(\mathbf d)\mathbf L^{\mathsf T},$$
where $\mathbf L$ is unit lower triangular. The diagonal entries may have either sign, so the method can handle indefinite matrices without taking square roots. The presented unpivoted program requires every original Gaussian pivot to be nonzero; symmetry alone does not ensure that domain condition.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.IsLDL name="LDL factor identity"
The lower factor is unit lower triangular, the diagonal vector is fixed by conjugation, and its diagonal matrix reconstructs the input through the conjugate-transpose identity. For the real stored program, conjugate transpose is ordinary transpose.
:::

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
