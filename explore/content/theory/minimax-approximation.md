---
kind: theory
id: minimax-approximation
title: Minimax approximation
summary: Best uniform approximation, equioscillation, and the minimax properties of Chebyshev polynomials.
status: outline
order: 9
parents:
- polynomial-approximation
module_prefixes:
- NLAlib.Polynomial.Approximation.Equioscillation
- NLAlib.Polynomial.Approximation.MinimaxError
---

A minimax problem asks how accurately a function can be approximated by a polynomial of a given degree on a specified set. The domain and normalization matter: a residual polynomial constrained at zero is a different problem from unconstrained approximation of a function.

::: definition name="Best uniform polynomial error"
For a continuous function $f$ on a compact set $S$, define

$$E_k(f;S)=\inf_{\deg p\le k}\sup_{t\in S}|f(t)-p(t)|.$$

For linear-system bounds, a common alternative is to minimize $\sup_{t\in S}|p(t)|$ over degree-at-most-$k$ polynomials satisfying $p(0)=1$. Equioscillation characterizes optimal approximants under the corresponding hypotheses.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
