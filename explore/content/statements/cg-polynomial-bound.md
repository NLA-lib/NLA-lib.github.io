---
kind: statement
id: cg-polynomial-bound
uid: aa1d5b60-6ec3-58e0-9168-e25e60a9d5a7
---

::: theorem result:cg-polynomial-bound name="Polynomial error bound"
Let $\mathbf{A}$ be Hermitian positive definite, and let $\mathbf{b}$,
$\mathbf{x}_\star$ satisfy $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$, and let
$\mathbf{x}_0$ be an initial vector. Let $\mathbf{x}_k$ be the $k$-th
[conjugate-gradient (CG)](/explore/algorithms/conjugate-gradient/) iterate in exact
arithmetic. Write $\|\mathbf{v}\|_\mathbf{A}^2=
\mathbf{v}^{\mathsf{H}}\mathbf{A}\mathbf{v}$ for the squared energy norm. For every
real polynomial $p$ of degree at most $k$ with $p(0)=1$,

$$\|\mathbf{x}_\star-\mathbf{x}_k\|_\mathbf{A}^2\le\|p(\mathbf{A})(\mathbf{x}_\star-\mathbf{x}_0)\|_\mathbf{A}^2.$$


Note: A polynomial small on the spectrum therefore yields a small CG error.
:::
