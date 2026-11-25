---
kind: statement
id: nlalib-polarschulziterate-469e6e39
uid: 469e6e39-a086-5aba-9b14-ee0d2e5df1f0
---

::: definition decl:NLAlib.polarSchulzIterate name="Newton–Schulz polar iteration"
Apply $\mathbf{X}_{j+1}=\tfrac12\mathbf{X}_j(3\mathbf{I}-\mathbf{X}_j^{\mathsf{H}}\mathbf{X}_j)$. This is the rectangular polar update and does not require a pseudoinverse. Initial scaling and the admissible singular-value interval are part of its convergence hypotheses.
:::
