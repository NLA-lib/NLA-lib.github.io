---
kind: statement
id: sequential-summation-in-standard-rounding-01b91c62
uid: 01b91c62-c0a4-5fb4-b5a3-c4049d568957
---

::: definition name="Sequential summation in standard rounding" id=sequential
The standard-rounding model of the solver pages sums sequentially. Scalar operations obey
standard rounding with unit roundoff $u$. A sum of $n$ terms accumulated in order has the
error coefficient $(1+u)^{n-1}-1$ (`Ops.Blas.seqSumErr`), and a dot product, which forms
rounded products and sums them, has

$$d_n=(1+u)^n-1$$

(`Ops.Blas.seq.err`). The same profile supplies the vector-update bounds. All vector lengths
are admitted. Matvec error is supplied separately; this model does not assume exact matvecs.

The library also has pairwise summation (`Ops.Blas.pairwise.err`). It improves the sum
coefficient to $(1+u)^{\lceil\log_2 n\rceil}-1$ (`Ops.Blas.pairSumErr`), so that
$d_n=(1+u)^{\lceil\log_2 n\rceil+1}-1$. It needs the depth condition
$\lceil\log_2 n\rceil<\mathrm{depth}$ (`Nat.clog 2 n < depth`) and declares a different
workspace for the vector operations. The solver theorems are stated for either scheme; the
pages present the sequential one. Pairwise summation specifies the reduction order; it does
not by itself certify parallel execution.
:::
