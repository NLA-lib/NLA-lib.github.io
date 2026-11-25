---
kind: statement
id: nlalib-generalizednystrom-a93c5a2a
uid: a93c5a2a-f071-5e53-ad6e-926ccafcbdad
---

::: definition decl:NLAlib.generalizedNystrom name="Generalized Nyström approximation"
For a rectangular matrix $\mathbf{A}$ and two test matrices $\mathbf\Omega,\mathbf\Psi$, define

$$\widehat{\mathbf{A}}=\mathsf{gn}(\mathbf{A},\mathbf\Omega,\mathbf\Psi)=\mathbf{A}\mathbf\Omega(\mathbf\Psi^{\mathsf{H}}\mathbf{A}\mathbf\Omega)^{\dagger}\mathbf\Psi^{\mathsf{H}}\mathbf{A}.$$

The two sketches capture column and row information. This is an oblique construction; it is generally different from orthogonally projecting onto the sampled range.
:::
