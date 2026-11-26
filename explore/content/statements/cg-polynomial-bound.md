---
kind: statement
id: cg-polynomial-bound
uid: aa1d5b60-6ec3-58e0-9168-e25e60a9d5a7
references:
  - key: Saad2003
    locator: §6.11.3
---

::: theorem result:cg-polynomial-bound name="Polynomial error bound"
For every polynomial $p$ of degree at most $k$ with $p(0)=1$,

$$\|\mathbf{x}_\star-\mathbf{x}_k\|_\mathbf{A}^2\le\|p(\mathbf{A})(\mathbf{x}_\star-\mathbf{x}_0)\|_\mathbf{A}^2.$$

A polynomial small on the spectrum therefore yields a small CG error.
:::
