---
kind: statement
id: nlalib-generalizednystrom-a93c5a2a
uid: a93c5a2a-f071-5e53-ad6e-926ccafcbdad
---

::: definition decl:NLAlib.generalizedNystrom name="Generalized Nyström approximation"
For a rectangular matrix $\mathbf{A}$ and two test matrices $\boldsymbol{\Omega},\boldsymbol{\Psi}$, define

$$\widehat{\mathbf{A}}=\mathsf{gn}(\mathbf{A},\boldsymbol{\Omega},\boldsymbol{\Psi})=\mathbf{A}\boldsymbol{\Omega}(\boldsymbol{\Psi}^{\mathsf{H}}\mathbf{A}\boldsymbol{\Omega})^{\dagger}\boldsymbol{\Psi}^{\mathsf{H}}\mathbf{A}.$$

The two sketches capture column and row information. This is an oblique construction; it is generally different from [orthogonally projecting](/explore/statements/2fa76a05-ce3c-5a1c-9aee-625c01bfd829/) onto the sampled range.
:::
