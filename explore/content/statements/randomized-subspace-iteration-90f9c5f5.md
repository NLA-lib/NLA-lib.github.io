---
kind: statement
id: randomized-subspace-iteration-90f9c5f5
uid: 90f9c5f5-2db3-5dde-afe2-c2d2f5bdd092
---

::: definition name="Randomized subspace iteration"
Choose a test matrix $\boldsymbol{\Omega}$ with $\ell$ columns and a nonnegative power count $p$. Form

$$\mathbf{Y}=\mathbf{A}(\mathbf{A}^{\mathsf{H}}\mathbf{A})^p\boldsymbol{\Omega},\qquad\mathsf{rsi}(\mathbf{A},\boldsymbol{\Omega},p)=\mathbf{P}_{\mathbf{Y}}\mathbf{A}=\mathsf{rsvd}\bigl(\mathbf{A},(\mathbf{A}^{\mathsf{H}}\mathbf{A})^p\boldsymbol{\Omega}\bigr).$$

Here $\mathbf{P}_{\mathbf{Y}}$ is the [orthogonal projector](/explore/statements/2fa76a05-ce3c-5a1c-9aee-625c01bfd829/) onto the sampled range. With $p=0$ this is the [ordinary range-finder approximation](/explore/statements/15e6c9dc-370c-5cb2-b684-46e5f33e39f2/). Only the last power is kept; [block Krylov iteration](/explore/statements/ce25720b-6102-5bb3-a0e2-a679814dd9d8/) keeps all of them. Intermediate orthogonalization controls the numerical loss of directions and belongs to an implementation. For Hermitian positive-semidefinite matrices, the range also approximates a dominant invariant subspace.
:::
