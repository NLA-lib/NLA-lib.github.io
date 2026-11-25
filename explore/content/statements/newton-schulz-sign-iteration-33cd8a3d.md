---
kind: statement
id: newton-schulz-sign-iteration-33cd8a3d
uid: 33cd8a3d-4740-5cbd-82aa-7e67e7c152da
---

::: definition name="Newton–Schulz sign iteration"
Scale a Hermitian matrix to obtain an initial iterate $\mathbf{X}_0$, then apply

$$\mathbf{X}_{j+1}=\tfrac12\mathbf{X}_j(3\mathbf{I}-\mathbf{X}_j^2).$$

The scalar polynomial has fixed points at $-1$, $0$, and $1$. Approximating the matrix sign requires a suitable initial scale and a spectral gap away from zero. A capped implementation returns a defined iterate even when its numerical convergence conditions have not been established.
:::
