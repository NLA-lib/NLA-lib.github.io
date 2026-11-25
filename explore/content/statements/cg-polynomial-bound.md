---
kind: statement
id: cg-polynomial-bound
uid: aa1d5b60-6ec3-58e0-9168-e25e60a9d5a7
---

::: theorem result:cg-polynomial-bound name="Polynomial error bound"
For every polynomial $p$ of degree at most $k$ with $p(0)=1$,

$$\|x_\star-x_k\|_A^2\le\|p(A)(x_\star-x_0)\|_A^2.$$

A polynomial small on the spectrum therefore yields a small CG error.
:::
