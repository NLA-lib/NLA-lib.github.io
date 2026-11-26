---
kind: statement
id: entry-2ac03293-50e9-5cc8-ade1-64f0afa9bd35
uid: 2ac03293-50e9-5cc8-ade1-64f0afa9bd35
---
::: theorem result:matrix-inverse-newton-schulz name="Residual squaring"
For square matrices $\mathbf{A}$ and initial inverse approximation $\mathbf{X}_0$, define
the inverse-refinement iterates by
$\mathbf{X}_{j+1}=\mathbf{X}_j(2\mathbf{I}-\mathbf{A}\mathbf{X}_j)$. After $k$
iterations, the right residual satisfies

$$\mathbf{I}-\mathbf{A}\mathbf{X}_k=(\mathbf{I}-\mathbf{A}\mathbf{X}_0)^{2^k}.$$
:::
