---
kind: statement
id: nlalib-krylov-lanczos-runs-solve
uid: 161639a0-5d37-530b-9f3f-52b80780a847
---

::: theorem decl:NLAlib.Krylov.Lanczos.runs_solve name="Exact execution correspondence" id=execution
Under the exact primitive contracts, admissible dimension, live separated input/output buffers, and sufficient output capacity, the program executes successfully and stores the mathematical three-term recurrence for the supplied matrix, starting vector, and cap. It preserves the random-tape position and satisfies the [call](/explore/statements/3318f77c-2fb6-5ae5-a52e-c7239d83ab69/) and [scratch bounds](/explore/statements/ca6ffb21-49a0-54fc-81a5-dae0dd103639/) above.

This correspondence holds for any real square matrix. Symmetry is additionally required to interpret the returned recurrence as [Hermitian Lanczos](/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/) and apply the tridiagonal spectral results on the mathematical method page. Zero input, zero cap, and early breakdown have the [output conventions described above](/explore/statements/8a730a7c-e552-5641-bd95-fa635dcebc98/).
:::
