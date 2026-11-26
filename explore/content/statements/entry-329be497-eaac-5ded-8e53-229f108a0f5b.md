---
kind: statement
id: entry-329be497-eaac-5ded-8e53-229f108a0f5b
uid: 329be497-eaac-5ded-8e53-229f108a0f5b
---
::: theorem result:albert-theorem name="Albert's criterion"
The block matrix $\begin{bmatrix} \mathbf{A} & \mathbf{B} \\
\mathbf{B}^{\mathsf{H}} & \mathbf{C} \end{bmatrix}$ is positive semidefinite exactly when
$\mathbf{A}$ is, the equation $\mathbf{A}\mathbf{X} = \mathbf{B}$ has a solution, and
$\mathbf{C} - \mathbf{X}^{\mathsf{H}}\mathbf{A}\mathbf{X}$ is positive semidefinite for one such
solution (equivalently for all, `Matrix.IsHermitian.conjTranspose_mul_mul_eq_of_mul_eq`).
The cited form uses the pseudoinverse solution
$\mathbf{X} = \mathbf{A}^{+}\mathbf{B}$ and the range condition
$\mathbf{A}\mathbf{A}^{+}\mathbf{B} = \mathbf{B}$, here with any solution, so that no
pseudoinverse is needed.
:::
