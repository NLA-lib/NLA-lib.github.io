---
kind: statement
id: nlalib-earlytruncatedgeneralizednystrom-cdd691bb
uid: cdd691bb-6aef-5d59-b7e9-615785a98d27
---

::: definition decl:NLAlib.earlyTruncatedGeneralizedNystrom name="Early-truncated GN"
Form $\mathbf{Y}_k=[\mathbf{A}\boldsymbol{\Omega}]_k$, then return

$$\widehat{\mathbf{A}}=\mathbf{Y}_k(\boldsymbol{\Psi}^{\mathsf{H}}\mathbf{Y}_k)^{\dagger}\boldsymbol{\Psi}^{\mathsf{H}}\mathbf{A}.$$

The rank-$k$ subspace is selected from the range sketch before the second sketch completes the approximation. The output has rank at most $k$; the library fixes a choice when [singular values](/explore/statements/581c9098-24f3-55b6-bd36-a47af48b21ff/) are tied.
:::
