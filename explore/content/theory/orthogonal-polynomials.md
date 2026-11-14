---
kind: theory
id: orthogonal-polynomials
title: Orthogonal polynomials and quadrature
summary: Three-term recurrences and Gauss, Gauss–Radau, and Gauss–Lobatto quadrature.
status: outline
order: 10
parents:
- polynomial-approximation
module_prefixes:
- NLAlib.Polynomial.Orthogonal
- NLAlib.Krylov.Functions.Quadrature
---

A measure defines an inner product on polynomials. Orthogonalizing this sequence produces recurrences whose small Jacobi matrices connect polynomial zeros, quadrature nodes, and Lanczos coefficients.

::: definition name="Orthogonal polynomials and quadrature rules"
For a positive measure $\mu$ with the required finite moments, polynomials $p_i,p_j$ are orthogonal when $\int p_i(t)p_j(t)\,d\mu(t)=0$ for $i\ne j$. A quadrature rule replaces an integral by $\sum_i w_i f(t_i)$. Gauss, Radau, and Lobatto rules differ in whether endpoint nodes are prescribed; exactness and error statements require the hypotheses given in each result.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
