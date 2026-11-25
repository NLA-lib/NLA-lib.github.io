---
kind: statement
id: nlalib-schur-verifiedschurwith-writes
uid: eacde6b9-1053-568f-8c81-625ce5f50695
---

::: theorem decl:NLAlib.Schur.verifiedSchurWith_writes name="The check works with any Schur solver" id=verified-any-solver
Let `Solve` be any routine that, from every input memory and on every tape, terminates, writes only $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, and stores a matrix and an accumulator with $\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le e_U$. On a machine in the standard model with index literals and exact comparisons, let $64(n+2)^3u\le1$, $\kappa\ge32(n+2)^2u$, $\theta\ge0$ and $2\theta\sqrt{n+1}\le\delta$. Then for every $\mathbf{A}$, on **every** tape, `verifiedSchurWith Solve` terminates, writes only $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, keeps the orthogonality bound and stores the flag $0$ or $1$. If the flag is $0$, then $\widehat{\mathbf{T}}$ is upper triangular and

$$\|\mathbf{A}-\widehat{\mathbf{U}}\widehat{\mathbf{T}}\widehat{\mathbf{U}}^{\mathsf{H}}\|_2\le\delta\|\mathbf{A}\|_2.$$
:::
