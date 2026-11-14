---
kind: algorithm
id: gmres
title: GMRES
summary: Minimize the residual over a Krylov space for a general square system.
status: outline
order: 6
theory:
- krylov-spaces
- subspaces
uses:
- arnoldi
families:
- residual-minimization-methods
library_results: false
result_ids:
- gmres-optimality
- gmres-petrov-galerkin
- gmres-polynomial-bound
- gmres-diagonalizable-bound
- gmres-field-of-values-bound
- gmres-finite-termination
- gmres-arnoldi
- gmres-givens
- gmres-residual-estimate
---

Minimize the residual over a Krylov space for a general square system.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="GMRES"
For $\mathbf A\mathbf x=\mathbf b$, set $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$. Choose

$$\mathbf x_k\in\operatorname*{arg\,min}_{\mathbf y\in\mathbf x_0+\mathcal K_k(\mathbf A,\mathbf r_0)}\|\mathbf b-\mathbf A\mathbf y\|_2.$$

Arnoldi reduces this minimization to a small least-squares problem. Restarting changes the sequence of search spaces and is a distinct concrete variant.
:::



## Components

{{ generated:components }}

## Mathematical guarantees

::: theorem result:gmres-optimality name="Minimum residual"
For any square $\mathbf A$, right-hand side $\mathbf b$, starting point $\mathbf x_0$, and $k\ge0$, the mathematical GMRES iterate satisfies

$$\|\mathbf b-\mathbf A\mathbf x_k\|_2\le\|\mathbf b-\mathbf A\mathbf y\|_2\quad\text{for every }\mathbf y\in\mathbf x_0+\mathcal K_k(\mathbf A,\mathbf r_0),$$

where $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$. No positive-definiteness assumption is required for this optimality statement.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}

## Family

{{ generated:families }}
