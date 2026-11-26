---
kind: statement
id: nlalib-countsketchmatrix-161d8fd6
uid: 161d8fd6-2f0a-5e7e-8b4c-e7e67c1e6289
---

::: definition decl:NLAlib.countSketchMatrix name="CountSketch"
Choose a hash $h:\{1,\ldots,n\}\to\{1,\ldots,s\}$ and signs $\sigma_i\in\{-1,1\}$. Define $\mathbf{S}_{a,i}=\sigma_i$ when $h(i)=a$, and zero otherwise. Each input coordinate contributes to one output bucket. The standard law uses uniform independent hash values and independent Rademacher signs; [embedding](/explore/statements/dd0c654f-b783-516b-b7c3-04b96f1a90f3/) guarantees specify the required output dimension.
:::
