---
kind: statement
id: dense-schur-backward-error
uid: 9fd58d97-e831-5cb7-9bf8-24b035ded4c6
---

::: theorem result:dense-schur-backward-error name="The dense Schur theorem" id=accuracy
Let the machine and the streams be as above, $0<\delta\le1$, $0<\varphi\le1$ and $u\le u_0$. For every complex $\mathbf{A}$ of order $n+1$, start `denseSchur` from a memory holding $\mathbf{A}$ and the words of `denseSchurParams`. Then the probability is at most $\varphi$ that the run fails, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ and $\widehat{\mathbf{U}},\widehat{\mathbf{T}}$ with $\widehat{\mathbf{T}}$ upper triangular,

$$\|\mathbf{A}-\widehat{\mathbf{U}}\widehat{\mathbf{T}}\widehat{\mathbf{U}}^{\mathsf{H}}\|_2\le\delta\|\mathbf{A}\|_2\quad\text{and}\quad\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le58Ru.$$

Here $R$ is `denseSchurRotations`, and $58Ru\le\delta$.
:::
