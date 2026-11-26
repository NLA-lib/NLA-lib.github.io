---
kind: statement
id: lanczos-scalar-rounded-operation-count-ritz-residual
uid: 1b2b66d6-11bb-5c95-be41-014310fedb97
---

::: theorem result:lanczos-scalar-rounded-operation-count-ritz-residual name="Termination, operation count and Ritz residuals" id=stored-scalar-rounded
Let $\mathbf{A}\in\mathbb{R}^{n\times n}$ be symmetric, stored entry by entry, let $\mathbf{b}\in\mathbb{R}^n$, and let $k$ be the iteration cap. The program is the Lanczos recurrence in Paige's ordering started from $\mathbf{b}$, without reorthogonalization. Scalar arithmetic is any machine in the standard model with unit roundoff $u$, and comparisons of stored numbers are exact. Let $E\le1/100$ be an allowance that dominates the rounding of one scalar operation, of one dot product, vector update and scaling of length $n$, and of one row-by-row matrix–vector product (`Lanczos.Rounded.Precision`).

Then, for every such input and every tape, the run succeeds, and:

- it executes at most $33n^2k+153nk+302k+58n+179$ instructions, each of unit cost: scalar operations, comparisons, index arithmetic, operand addressing, loop control and allocation;
- it performs some number $m\le k$ of steps and stores the vectors $\mathbf{v}_1,\dots,\mathbf{v}_{m+1}$, the coefficients $\alpha_1,\dots,\alpha_m$ and $\beta_1,\dots,\beta_m$, and the computed norm of $\mathbf{b}$. They are the values of a rounded Lanczos run with local error allowance $E$ (`Lanczos.Rounded.Output`), which stops before the cap only at a zero computed norm or coupling coefficient;
- if $k>0$, $\mathbf{b}\ne\mathbf{0}$ and $kE\le1/100$, there is a length $q$ with $1\le q\le k$, whose stored $\beta_q$ is zero when $q<k$, such that every $\theta$ and unit vector $\mathbf{y}$ with $\mathbf{T}_q\mathbf{y}=\theta\mathbf{y}$ satisfy

$$\|\mathbf{A}\mathbf{V}_q\mathbf{y}-\theta\mathbf{V}_q\mathbf{y}\|_2\le\sqrt{1+E}\,\beta_q|y_q|+6q\sqrt q\,E\,\|\mathbf{A}\|_2,$$

where $\mathbf{V}_q=[\mathbf{v}_1,\dots,\mathbf{v}_q]$ and $\mathbf{T}_q$ is the leading $q\times q$ stored tridiagonal matrix.

No orthogonality of the stored vectors is claimed. So $\mathbf{V}_q\mathbf{y}$ need not be close to a unit vector, and the residual bound alone does not place $\theta$ near an eigenvalue of $\mathbf{A}$. The instruction count is an upper bound read off the fixed program.
:::
