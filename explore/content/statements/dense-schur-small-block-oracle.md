---
kind: statement
id: dense-schur-small-block-oracle
uid: 0fd77512-96c3-582c-b497-d366e5477268
---

::: theorem result:dense-schur-small-block-oracle name="The dense Schur theorem with any small-block solver" id=accuracy-any-leaf
Let the machine and the streams be as above, $0<\delta\le1$, $0<\varphi\le1$, let `L` meet the small-block contract with $\beta_L,\varphi_L,\varepsilon_L$ in the ranges above, and let $u\le$ `uDenseSchurWith`. For every complex $\mathbf{A}$ of order $n+1$, from a memory holding $\mathbf{A}$ and the words of `denseSchurParamsWith` with the solver's twelve words, the probability is at most $\varphi$ that `denseSchurWith sG L` fails, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ and $\widehat{\mathbf{U}},\widehat{\mathbf{T}}$ with $\widehat{\mathbf{T}}$ upper triangular,

$$\|\mathbf{A}-\widehat{\mathbf{U}}\widehat{\mathbf{T}}\widehat{\mathbf{U}}^{\mathsf{H}}\|_2\le\delta\|\mathbf{A}\|_2\quad\text{and}\quad\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le58Ru,$$

with $R$ = `denseSchurRotationsWith` at the solver's $R_L$.
:::
