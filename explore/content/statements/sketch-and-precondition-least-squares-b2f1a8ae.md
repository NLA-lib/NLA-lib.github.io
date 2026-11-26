---
kind: statement
id: sketch-and-precondition-least-squares-b2f1a8ae
uid: b2f1a8ae-a178-59b9-93a3-cb761460b941
---

::: definition name="Sketch-and-precondition least squares"
Use a sketch to construct a preconditioner, then solve the original least-squares objective in transformed coordinates. For example, if a [thin QR factorization](/explore/statements/adb72f11-3503-58f9-89c4-98a60c4f7a40/) $\mathbf{S}\mathbf{A}=\mathbf{Q}\mathbf{R}$ has invertible $\mathbf{R}$, solve $\min_{\mathbf{y}}\|\mathbf{A}\mathbf{R}^{-1}\mathbf{y}-\mathbf{b}\|_2$ and recover $\mathbf{x}=\mathbf{R}^{-1}\mathbf{y}$. The sketch improves the coordinates; it does not replace the original objective.
:::
