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

A stored matrix changes more than the arithmetic accuracy alone. The [stored scalar program](#section-stored-scalar-program-in-rounded-arithmetic) below is a different program, with its own operation count and its own arithmetic model.

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

## Stored scalar program in rounded arithmetic

The library also certifies the recurrence as a different program. The matrix is stored entry by entry, and every matrix–vector product and vector operation is written out as scalar loops. Its only primitives are scalar operations and comparisons, so its work is a count of instructions and its arithmetic is the standard model alone.

::: theorem result:lanczos-scalar-rounded-operation-count-ritz-residual name="Termination, operation count and Ritz residuals" id=stored-scalar-rounded
Let $\mathbf A\in\mathbb R^{n\times n}$ be symmetric, stored entry by entry, let $\mathbf b\in\mathbb R^n$, and let $k$ be the iteration cap. The program is the Lanczos recurrence in Paige's ordering started from $\mathbf b$, without reorthogonalization. Scalar arithmetic is any machine in the standard model with unit roundoff $u$, and comparisons of stored numbers are exact. Let $E\le1/100$ be an allowance that dominates the rounding of one scalar operation, of one dot product, vector update and scaling of length $n$, and of one row-by-row matrix–vector product (`Lanczos.Rounded.Precision`).

Then, for every such input and every tape, the run succeeds, and:

- it executes at most $33n^2k+153nk+302k+58n+179$ instructions, each of unit cost: scalar operations, comparisons, index arithmetic, operand addressing, loop control and allocation;
- it performs some number $m\le k$ of steps and stores the vectors $\mathbf v_1,\dots,\mathbf v_{m+1}$, the coefficients $\alpha_1,\dots,\alpha_m$ and $\beta_1,\dots,\beta_m$, and the computed norm of $\mathbf b$. They are the values of a rounded Lanczos run with local error allowance $E$ (`Lanczos.Rounded.Output`), which stops before the cap only at a zero computed norm or coupling coefficient;
- if $k>0$, $\mathbf b\ne\mathbf 0$ and $kE\le1/100$, there is a length $q$ with $1\le q\le k$, whose stored $\beta_q$ is zero when $q<k$, such that every $\theta$ and unit vector $\mathbf y$ with $\mathbf T_q\mathbf y=\theta\mathbf y$ satisfy

$$\|\mathbf A\mathbf V_q\mathbf y-\theta\mathbf V_q\mathbf y\|_2\le\sqrt{1+E}\,\beta_q|y_q|+6q\sqrt q\,E\,\|\mathbf A\|_2,$$

where $\mathbf V_q=[\mathbf v_1,\dots,\mathbf v_q]$ and $\mathbf T_q$ is the leading $q\times q$ stored tridiagonal matrix.

No orthogonality of the stored vectors is claimed. So $\mathbf V_q\mathbf y$ need not be close to a unit vector, and the residual bound alone does not place $\theta$ near an eigenvalue of $\mathbf A$. The instruction count is an upper bound read off the fixed program.
:::

## Mathematical method

{{ generated:mathematical-method }}
