---
kind: statement
id: nlalib-frobnorm-sub-truncatedsvd-rsvd-sq
uid: 25803ed2-ec86-5406-bad1-718ee3c6f0bf
---

::: theorem decl:NLAlib.frobNorm_sub_truncatedSVD_rsvd_sq name="Orthogonal error decomposition"
For every matrix $\mathbf{A}$, sketch $\boldsymbol{\Omega}$, and target rank $k$,

$$\|\mathbf{A}-[\mathbf{B}]_k\|_{\mathrm F}^2=\|\mathbf{A}-\mathbf{B}\|_{\mathrm F}^2+\|\mathbf{B}-[\mathbf{B}]_k\|_{\mathrm F}^2,\qquad\mathbf{B}=\mathbf{P}_{\mathbf{A}\boldsymbol{\Omega}}\mathbf{A}.$$

The squared error separates into the range-finding error and the error from [truncating within that range](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/).
:::
