---
kind: statement
id: nlalib-sketchandsolve-9af30d5f
uid: 9af30d5f-52d8-5a0a-af57-e2b4820cfa0a
---

::: definition decl:NLAlib.sketchAndSolve name="Sketch-and-solve least squares"
Replace the original problem by $\min_{\mathbf{x}}\|\mathbf{S}\mathbf{A}\mathbf{x}-\mathbf{S}\mathbf{b}\|_2$ and return the minimum-norm solution

$$\widehat{\mathbf{x}}=(\mathbf{S}\mathbf{A})^{\dagger}\mathbf{S}\mathbf{b}.$$

The solution minimizes the sketched residual. Relating it to the original residual requires assumptions on the sketch.
:::
