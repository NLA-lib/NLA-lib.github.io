---
kind: statement
id: landweber-iteration-be6e71b0
uid: be6e71b0-40da-513f-9790-9c44f41a3a31
---

::: definition name="Landweber iteration"
For $\min_{\mathbf{x}}\|\mathbf{A}\mathbf{x}-\mathbf{b}\|_2^2$, choose a real step $\eta$ and set $\mathbf{x}_{j+1}=\mathbf{x}_j+\eta\mathbf{A}^{\mathsf{H}}(\mathbf{b}-\mathbf{A}\mathbf{x}_j)$. The finite-step spectral-filter identity holds without asserting stability of the chosen step; convergence needs an appropriate step-size condition.
:::
