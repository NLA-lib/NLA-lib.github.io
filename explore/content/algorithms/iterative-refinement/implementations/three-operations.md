---
uid: 156393ee-98e4-543f-bb80-b019cc9c899e
kind: implementation
id: three-operations
algorithm: iterative-refinement
title: Residual, solve and update as operations
summary: One fixed loop over three vector operations, each with its own accuracy, certified for an unstored matrix.
status: ready
order: 2
library_algorithm: iterative-refinement
library_results: false
arithmetic_models:
- id: operation-accuracies
  title: Prescribed accuracy of each operation
search_aliases:
- certified iterative refinement
- refinement routine
---

This page describes the library's certified refinement program. The residual, the correction solve and the update are operations of the model, each with its own accuracy contract, so each may be implemented in a different precision. The program performs no scalar arithmetic of its own, so its theorem applies to any implementation of the three operations. The [three-precision program](/explore/algorithms/iterative-refinement/implementations/three-precision/) is one such implementation, in scalar arithmetic.

## Mathematical method

{{ generated:mathematical-method }}

## Algorithm

```text
input: right-hand side b; start x (updated in place); scratch r, d, all of length n
repeat k times:
    r := residual(b, x)
    d := solve(r)
    x := update(d, x)
output: x
```

The number of steps $k$ is fixed: the program has no stopping test. It is the routine `LinearSystems.Refinement.solve`. The matrix is in no buffer, and is reached only through `residual` and `solve`.

| Buffer | Content |
| --- | --- |
| 0 | The $n$ words of $\mathbf{b}$, read only |
| 1 | The $n$ words of $\mathbf{x}_0$, overwritten by the output |
| 2 | Room for $n$ words: the residual, not reported |
| 3 | Room for $n$ words: the correction, not reported |

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The model has three operations and no query. For the matrix $\mathbf{A}$ of the input and fixed $\theta,\eta,\zeta,\varepsilon\ge0$, on decoded blocks in the Euclidean norm:

| Operation | Contract |
| --- | --- |
| `residual` | $\|\mathbf{b}-\mathbf{A}\mathbf{x}-\mathbf{r}\|\le\zeta\|\mathbf{b}-\mathbf{A}\mathbf{x}\|+\eta(\|\mathbf{b}\|+\|\mathbf{A}\|_2\|\mathbf{x}\|)$ |
| `solve` | $\|\mathbf{A}^{-1}\mathbf{r}-\mathbf{d}\|\le\theta\|\mathbf{A}^{-1}\mathbf{r}\|$ |
| `update` | $\|\mathbf{x}+\mathbf{d}-\mathbf{x}'\|\le\varepsilon\|\mathbf{x}+\mathbf{d}\|$ |

`residual` and `solve` are declared oracles for $\mathbf{A}$: their contracts depend on the input only through the matrix. `update` has one contract at every size and input. The model is confined, and exact arithmetic satisfies the three contracts jointly, so they are not vacuous. These contracts are assumptions of the model. In particular, a `solve` meeting its contract is assumed here, not built from a factorization.

## Operations and Storage

With unit weights, each call of `residual`, `solve` or `update` and each structural instruction counts one. The work and span are at most

$$25k+15$$

instructions, independent of $n$ because the three vector operations are primitives. There are $3k$ operation calls. This is not a count of scalar operations: the cost of a factorization, of a residual and of an update is not included. The supplied buffers hold $4n$ words and the routine allocates nothing.

## Accuracy

{{ statement:nlalib-linearsystems-refinement-certification-algorithm-checked }}

The condition $\varphi<1$ is part of the admitted inputs. The stored iterates form a [refinement run](/explore/algorithms/iterative-refinement/#run), so every theorem about a run applies to them.

## Not yet presented

- A stopping test, and the backward-error results of Carson and Higham.
