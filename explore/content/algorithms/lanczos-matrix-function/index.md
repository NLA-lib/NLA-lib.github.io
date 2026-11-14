---
kind: algorithm
id: lanczos-matrix-function
title: Lanczos matrix-function approximation
summary: Run Lanczos, evaluate $f$ on the small tridiagonal matrix, and lift the result to approximate
  $f(A)b$.
status: outline
order: 2
theory:
- matrix-polynomials
- polynomial-approximation
uses:
- lanczos
library_results: false
result_ids:
- lanczos-fa-exactness
- lanczos-fa-formula
- lanczos-fa-interpolation
- lanczos-fa-kernel-near-optimality
- lanczos-fa-near-optimality
- lanczos-fa-near-optimality-lower-bound
- lanczos-fa-uniform-bound
- lanczos-fa-recurrence
- lanczos-fa-cg
---

Run Lanczos, evaluate $f$ on the small tridiagonal matrix, and lift the result to approximate $f(A)b$.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.lanczosFA name="Lanczos matrix-function approximation"
For Hermitian $\mathbf A$, nonzero $\mathbf b$, and a Lanczos basis whose first column is $\mathbf b/\|\mathbf b\|_2$, approximate the matrix-function action by

$$f(\mathbf A)\mathbf b\approx\|\mathbf b\|_2\mathbf Q_k f(\mathbf T_k)\mathbf e_1.$$

Here $\mathbf T_k=\mathbf Q_k^{\mathsf{H}}\mathbf A\mathbf Q_k$. If the Krylov space becomes invariant earlier, use the generated nonzero prefix. Evaluating the function on the compression is an additional step beyond the Lanczos process.
:::



## Components

{{ generated:components }}

## Mathematical guarantees

::: theorem result:lanczos-fa-uniform-bound name="Polynomial approximation controls the error"
Let $\mathbf A$ be Hermitian with spectrum in $[a,b]$, and let $f$ be continuous on that interval. With $q+1$ mathematical Lanczos steps,

$$\|f(\mathbf A)\mathbf b-\operatorname{LanczosFA}(\mathbf A,f,\mathbf b,q+1)\|_2\le2E_q(f;[a,b])\|\mathbf b\|_2,$$

where $E_q$ is the best uniform approximation error among polynomials of degree at most $q$. A good low-degree approximation to $f$ therefore gives an accurate matrix-function action.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
