---
kind: theory
id: chebyshev-polynomials
title: Chebyshev polynomials
summary: Chebyshev polynomials, equioscillation, extremal growth, and residual convergence bounds.
status: outline
order: 8
parents:
- polynomial-approximation
module_prefixes:
- NLAlib.Polynomial.Chebyshev
result_ids:
- chebyshev-extremal
- chebyshev-growth
---

Chebyshev polynomials provide an oscillating basis on an interval and explicit extremal polynomials. They appear both in polynomial approximations to matrix functions and in convergence bounds for Krylov solvers.

::: definition name="Chebyshev polynomials"
The first-kind Chebyshev polynomials satisfy $T_k(\cos\theta)=\cos(k\theta)$, with $T_0(t)=1$, $T_1(t)=t$, and

$$T_{k+1}(t)=2tT_k(t)-T_{k-1}(t).$$

An affine change of variable transfers constructions on $[-1,1]$ to another interval. Residual bounds also impose the normalization appropriate to the linear system.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
