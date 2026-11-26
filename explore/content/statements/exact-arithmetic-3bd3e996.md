---
kind: statement
id: exact-arithmetic-3bd3e996
uid: 3bd3e996-91bc-59ca-a0ac-fb32de488886
---

::: definition name="Exact arithmetic" id=exact
Every scalar operation of the machine returns the exact value: literals, addition,
subtraction, multiplication, division by a nonzero number, negation, and the square
root of a nonnegative number (`Ops.ExactModel`). In an exact operation model, dot
products, vector updates, and matrix–vector products are exact as well.

Note: A correspondence theorem identifies a stored program's output with the mathematical method. For CG, the recurrence agrees with mathematical CG, so classical convergence and finite-termination results apply under their matrix assumptions.
:::
