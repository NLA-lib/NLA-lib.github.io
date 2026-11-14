---
kind: theory
id: krylov-spaces
title: Krylov spaces
summary: Krylov spaces, grade, and polynomial projections underlying CG, Lanczos, and Arnoldi.
status: outline
order: 12
parents:
- matrix-analysis
- polynomial-approximation
prerequisites:
- subspaces
- matrix-polynomials
module_prefixes:
- NLAlib.Krylov.Basic
---

For a starting vector $b$, a Krylov space collects the vectors obtainable by applying low-degree polynomials in $A$. It is a mathematical object shared by many algorithms, not an arithmetic implementation.

::: definition name="Krylov space and grade"
For $\mathbf A\in\mathbb R^{n\times n}$ and $\mathbf b\in\mathbb R^n$, define $\mathcal K_k(\mathbf A,\mathbf b)=\operatorname{span}\{\mathbf b,\mathbf A\mathbf b,\ldots,\mathbf A^{k-1}\mathbf b\}$. The grade is the first index at which this sequence of subspaces stops growing. Orthogonal compression onto such a space underlies several different algorithms; their output and optimality conditions belong on the method pages.
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
