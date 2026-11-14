---
kind: implementation
id: ordinary
algorithm: lanczos
title: Ordinary Lanczos
summary: The guarded three-term recurrence with a matrix-free operator and exact vector operations.
status: ready
order: 3
library_algorithm: lanczos
library_results: false
source_guides:
- docs/algorithms/Lanczos.md
---

This page describes the real, matrix-free three-term program. It stores a basis and tridiagonal coefficients; extracting eigenvalues or evaluating a matrix function is a subsequent algorithm.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.Krylov.Lanczos.solve name="Guarded three-term Lanczos" id=algorithm
Supply a starting vector $\mathbf b\in\mathbb R^n$, an operator application, and an iteration cap $k$.

1. Zero the basis output, coefficient output, and previous vector.
2. Compute $\sigma=\operatorname{dot}(\mathbf b,\mathbf b)$.
3. If $\sigma>0$, compute the input norm $\nu=\sqrt\sigma$.
4. Normalize the initial current vector $\mathbf q=\mathbf b/\nu$ and store it; otherwise keep zero outputs.
5. Set the previous coefficient $\beta=0$.
6. For each requested round while the current self-dot is positive:
   1. Compute $\mathbf w=\operatorname{matvec}(\mathbf q)$.
   2. Update $\mathbf w\leftarrow\mathbf w-\beta\mathbf q_{\mathrm{prev}}$.
   3. Compute and store $\alpha=\operatorname{dot}(\mathbf q,\mathbf w)$.
   4. Update $\mathbf w\leftarrow\mathbf w-\alpha\mathbf q$.
   5. Compute $\sigma=\operatorname{dot}(\mathbf w,\mathbf w)$.
   6. Copy the current vector to the previous-vector buffer.
   7. If $\sigma>0$, store $\beta=\sqrt\sigma$ and normalize the next vector $\mathbf q=\mathbf w/\beta$.
   8. Otherwise store a zero coefficient and a zero next vector.
   9. Store the next basis column.
7. Return the initialized and computed output arrays, releasing scoped scratch.

Square roots and divisions are guarded. A zero starting vector returns zero outputs. A zero cap still initializes the arrays and normalizes a nonzero starting vector. After early breakdown, unused output entries remain zero.
:::

## Model of arithmetic

The result below uses exact real scalar arithmetic, exact dot products, vector updates, copies and normalization, and an exact application of $\mathbf A$. Matvec is an abstract operator call with its own work and workspace costs. The matrix itself is not supplied as a resident dense buffer in this program.

The library also has rounded and stored scalar implementations. Their error contracts and lowered resource counts require separate presentation; choosing a stored matrix changes more than the arithmetic accuracy alone.

## Operations and Storage

::: theorem decl:NLAlib.Krylov.Lanczos.stmtCost_solve name="Operation budget" id=operations
For dimension $n$ and cap $k$, the static budget permits at most $k$ matvecs, $1+2k$ length-$n$ dot products, $2k$ vector updates, $1+2k$ vector copies, and $1+k$ vector normalizations.

It also permits $1+k$ square roots, $2k$ scalar negations, $(k+2)n+2k+2$ zero literals, and $1+2k$ positivity queries. Initialization is included; early stopping can reduce the actual calls. Work is obtained by charging these calls according to the chosen primitive costs. The displayed Lean statement identifies the complete primitive-call budget.
:::

::: theorem decl:NLAlib.Krylov.Lanczos.stmtPeak_solve_le name="Scratch and output capacity" id=storage
The scoped scratch bound is

$$2n+2+W(n),$$

where $W(n)$ is the maximum declared workspace over the primitive calls used by this program. It does not grow with the cap.

The supplied basis output has $(k+1)n$ cells, the coefficient output has $2k+2$ cells, and the input has $n$ cells. These supplied capacities are additional to scratch. Storage captured by an external operator is accounted for by that operator's model.
:::

## Accuracy

::: theorem decl:NLAlib.Krylov.Lanczos.runs_solve name="Exact execution correspondence" id=execution
Under the exact primitive contracts, admissible dimension, live separated input/output buffers, and sufficient output capacity, the program executes successfully and stores the mathematical three-term recurrence for the supplied matrix, starting vector, and cap. It preserves the random-tape position and satisfies the call and scratch bounds above.

This correspondence holds for any real square matrix. Symmetry is additionally required to interpret the returned recurrence as Hermitian Lanczos and apply the tridiagonal spectral results on the mathematical method page. Zero input, zero cap, and early breakdown have the output conventions described above.
:::

## Mathematical method

{{ generated:mathematical-method }}
