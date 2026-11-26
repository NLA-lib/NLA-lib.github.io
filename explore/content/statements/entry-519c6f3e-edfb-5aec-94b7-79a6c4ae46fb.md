---
kind: statement
id: entry-519c6f3e-edfb-5aec-94b7-79a6c4ae46fb
uid: 519c6f3e-edfb-5aec-94b7-79a6c4ae46fb
---
::: theorem result:procrustes-scaled name="The nearest scaled isometry in Frobenius norm"
For
$\mathbf{A} \in \Bbbk^{m \times n}$ with $\lvert n \rvert \le \lvert m \rvert$, the least
value of $\|\mathbf{A} - c\mathbf{U}\|_{\mathsf{F}}^2$ over all $c \in \mathbb{R}$ and all
$\mathbf{U} \in \Bbbk^{m \times n}$ with orthonormal columns is
$$\|\mathbf{A}\|_{\mathsf{F}}^2 - \frac{\|\mathbf{A}\|_*^2}{\lvert n \rvert}\,.$$
It is attained by an isometric polar extension scaled by the average singular value. This
includes negative competing scales and rank-deficient matrices. For empty columns the minimum
is zero, with division by zero interpreted as zero. No uniqueness is asserted.
The cited result is for the square case; this statement generalizes it to rectangular matrices over
any `RCLike` field and arbitrary finite index types, including empty columns.
Generalizes `NLAlib.isLeast_frobSq_sub_scaled_orthogonal` and
`NLAlib.isLeast_frobSq_sub_scaled_orthogonal_of_isEmpty` from the original NLAlib formal library,
`NLAlib.Matrix.Factorizations.ScaledOrthogonal`, commit
`77514ce42a0e437d837797a063ac161f41022730`, from square real to rectangular `RCLike` matrices,
combining the nonempty and empty cases.
:::
