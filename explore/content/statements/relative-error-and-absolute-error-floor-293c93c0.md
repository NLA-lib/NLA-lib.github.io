---
kind: statement
id: relative-error-and-absolute-error-floor-293c93c0
uid: 293c93c0-109c-5fc6-b2df-49f56a960c23
---

::: definition name="Relative error and absolute error floor"
A typical scalar error contract has the form

$$|\widehat z-z|\le u|z|+\eta,$$

where $u$ is a relative-error parameter and $\eta$ is an absolute-error floor. Setting $\eta=0$ is an additional choice, not a consequence of relative accuracy. Dot products with cancellation and matrix-vector products need their own accumulation bounds.
:::
