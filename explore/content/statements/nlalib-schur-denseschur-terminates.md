---
kind: statement
id: nlalib-schur-denseschur-terminates
uid: 35b1d0b4-eb55-5a94-a77d-b2ae5486ab56
---

::: theorem decl:NLAlib.Schur.denseSchur_terminates name="Termination and orthogonality on every tape" id=every-tape
On the same machine, for $0<\delta\le1$, any $\varphi$, every $\mathbf{A}$ and $u\le u_0$, the run succeeds on **every** tape, writes only $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, and stores $\widehat{\mathbf{U}}$ with $\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le58Ru$.
:::
