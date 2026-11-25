---
kind: statement
id: nlalib-smalleig-smalleigprog-pwrites-schur
uid: 20efeb03-db73-58b6-b181-c8ccc263a5a2
---

::: theorem decl:NLAlib.SmallEig.smallEigProg_pwrites_schur name="The output is a Schur pair" id=accuracy-schur
Let the machine and the streams be as above, with tail records that bound the two Ginibre tails, $u\le u_{\mathrm{SmallEig}}$ at those records, $n+1\le n_{\max}$, $\|\mathbf{M}\|_2\le\Sigma$, $0<\delta\le\Sigma$ and $0<\varphi\le1$. From a memory holding $\mathbf{M}$ and the parameter words, except with probability at most $\varphi$, the run writes only the matrix and the accumulator and stores an upper triangular $\widehat{\mathbf{T}}_b$ and an accumulator $\widehat{\mathbf{U}}_b$ with

$$\widehat{\mathbf{T}}_b=\mathbf{V}^{\mathsf{H}}(\mathbf{M}+\mathbf{E})\mathbf{V},\qquad\|\mathbf{E}\|_2\le\delta,\qquad\|\widehat{\mathbf{U}}_b-\mathbf{V}\|_2\le(1+24u)^{R}-1$$

for an exact unitary $\mathbf{V}$, with $R=n_{\max}^2+2(n_{\max}+1)\bigl((T+n_{\max})n_{\max}+6\bigr)$ (`smallEigLeafRotations`). The proved tail records satisfy the hypothesis. The eigenvalue theorems below are corollaries: the diagonal of $\widehat{\mathbf{T}}_b$ lists them.
:::
