---
kind: statement
id: randomized-subspace-iteration-90f9c5f5
uid: 90f9c5f5-2db3-5dde-afe2-c2d2f5bdd092
---

::: definition name="Randomized subspace iteration"
Choose a test matrix $\mathbf\Omega$ with $\ell$ columns and a nonnegative power count $p$. Form

$$\mathbf{Y}=\mathbf{A}(\mathbf{A}^{\mathsf{H}}\mathbf{A})^p\mathbf\Omega,\qquad\mathsf{rsi}(\mathbf{A},\mathbf\Omega,p)=\mathbf{P}_{\mathbf{Y}}\mathbf{A}=\mathsf{rsvd}\bigl(\mathbf{A},(\mathbf{A}^{\mathsf{H}}\mathbf{A})^p\mathbf\Omega\bigr).$$

Here $\mathbf{P}_{\mathbf{Y}}$ is the orthogonal projector onto the sampled range. With $p=0$ this is the ordinary range-finder approximation. Only the last power is kept; block Krylov iteration keeps all of them. Intermediate orthogonalization controls the numerical loss of directions and belongs to an implementation. For Hermitian positive-semidefinite matrices, the range also approximates a dominant invariant subspace.
:::
