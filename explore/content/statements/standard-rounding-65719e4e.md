---
kind: statement
id: standard-rounding-65719e4e
uid: 65719e4e-6ea0-536c-91c1-7624e92b30d1
---

::: definition name="Standard rounding" id=standard
Standard rounding is the standard model of rounded arithmetic with unit roundoff $u$
(`Ops.StdModel`). A scalar machine is in it when
each operation returns its exact result with relative error at most $u$:

$$|\widehat{a\circ b}-a\circ b|\le u\,|a\circ b|,\qquad\circ\in\{+,-,\times,/\},$$

with division only by a nonzero number, and likewise for literals and for the square
root of a nonnegative number. Negation is exact. There is no overflow and no underflow.
Exact arithmetic is the case $u=0$.

The model constrains the scalar operations only. A program whose only primitives are
scalar operations and comparisons, such as the stored scalar programs of CG and Lanczos,
needs nothing else. A program that calls vector or matrix operations also needs their
contracts, as in the next two definitions.
:::
