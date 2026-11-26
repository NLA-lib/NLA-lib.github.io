---
kind: statement
id: nlalib-earlytruncatedrsvd-a10be3ad
uid: a10be3ad-32a7-5746-ab21-26a6bf70c410
---

::: definition decl:NLAlib.earlyTruncatedRSVD name="Early-truncated RSVD"
Form the sketch $\mathbf{Y}=\mathbf{A}\boldsymbol{\Omega}$, retain its best [rank-at-most-$k$ approximation](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/) $[\mathbf{Y}]_k$, then return $\mathbf{P}_{[\mathbf{Y}]_k}\mathbf{A}$. The retained subspace is chosen from the sketch, rather than from the full projected matrix.
:::
