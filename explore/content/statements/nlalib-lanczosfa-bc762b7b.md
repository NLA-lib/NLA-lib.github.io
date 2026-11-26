---
kind: statement
id: nlalib-lanczosfa-bc762b7b
uid: bc762b7b-4199-51cc-b90c-187c41dc3af9
---

::: definition decl:NLAlib.lanczosFA name="Lanczos matrix-function approximation"
For [Hermitian](/explore/statements/49f5c3f6-f926-5bc6-b401-16993ec1e357/) $\mathbf{A}$, nonzero $\mathbf{b}$, and a Lanczos basis whose first column is $\mathbf{b}/\|\mathbf{b}\|_2$, approximate the matrix-function action by

$$f(\mathbf{A})\mathbf{b}\approx\|\mathbf{b}\|_2\mathbf{Q}_k f(\mathbf{T}_k)\mathbf{e}_1.$$

Here $\mathbf{T}_k=\mathbf{Q}_k^{\mathsf{H}}\mathbf{A}\mathbf{Q}_k$. If the Krylov space becomes invariant earlier, use the generated nonzero prefix. Evaluating the function on the compression is an additional step beyond the [Lanczos process](/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/).
:::
