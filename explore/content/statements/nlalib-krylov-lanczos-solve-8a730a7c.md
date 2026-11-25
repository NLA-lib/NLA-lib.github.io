---
kind: statement
id: nlalib-krylov-lanczos-solve-8a730a7c
uid: 8a730a7c-e552-5641-bd95-fa635dcebc98
---

::: definition decl:NLAlib.Krylov.Lanczos.solve name="Guarded three-term Lanczos" id=algorithm
Supply a starting vector $\mathbf{b}\in\mathbb R^n$, an operator application, and an iteration cap $k$.

1. Zero the basis output, coefficient output, and previous vector.
2. Compute $\sigma=\operatorname{dot}(\mathbf{b},\mathbf{b})$.
3. If $\sigma>0$, compute the input norm $\nu=\sqrt\sigma$.
4. Normalize the initial current vector $\mathbf{q}=\mathbf{b}/\nu$ and store it; otherwise keep zero outputs.
5. Set the previous coefficient $\beta=0$.
6. For each requested round while the current self-dot is positive:
   1. Compute $\mathbf{w}=\operatorname{matvec}(\mathbf{q})$.
   2. Update $\mathbf{w}\leftarrow\mathbf{w}-\beta\mathbf{q}_{\mathrm{prev}}$.
   3. Compute and store $\alpha=\operatorname{dot}(\mathbf{q},\mathbf{w})$.
   4. Update $\mathbf{w}\leftarrow\mathbf{w}-\alpha\mathbf{q}$.
   5. Compute $\sigma=\operatorname{dot}(\mathbf{w},\mathbf{w})$.
   6. Copy the current vector to the previous-vector buffer.
   7. If $\sigma>0$, store $\beta=\sqrt\sigma$ and normalize the next vector $\mathbf{q}=\mathbf{w}/\beta$.
   8. Otherwise store a zero coefficient and a zero next vector.
   9. Store the next basis column.
7. Return the initialized and computed output arrays, releasing scoped scratch.

Square roots and divisions are guarded. A zero starting vector returns zero outputs. A zero cap still initializes the arrays and normalizes a nonzero starting vector. After early breakdown, unused output entries remain zero.
:::
