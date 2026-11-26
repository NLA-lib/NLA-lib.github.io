---
kind: statement
id: nystrom-bki-simulated-block
uid: 2f994852-fd90-57d9-8eb6-b3c0d529793f
---

::: theorem result:nystrom-bki-simulated-block name="The simulated block" id=simulated-block
Let $\mathbf{A}$ be a real or complex Hermitian positive-semidefinite matrix and $\boldsymbol{\Omega}$ a start block. For all integers $s,q\ge0$,

$$\mathsf{nysbki}\bigl(\mathbf{A},\ [\boldsymbol{\Omega},\mathbf{A}\boldsymbol{\Omega},\ldots,\mathbf{A}^{s}\boldsymbol{\Omega}],\ q+1\bigr)=\mathsf{nysbki}(\mathbf{A},\boldsymbol{\Omega},\ s+q+1).$$

Running $s+q+1$ blocks from $\boldsymbol{\Omega}$ gives the same approximation as running $q+1$ blocks from the wider block formed by the first $s+1$ Krylov blocks of $\boldsymbol{\Omega}$. Positive semidefiniteness is a hypothesis of the statement.
:::
