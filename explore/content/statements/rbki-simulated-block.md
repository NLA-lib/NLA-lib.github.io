---
kind: statement
id: rbki-simulated-block
uid: 1d855d8f-f49a-5243-9071-144b23a999ad
---

::: theorem result:rbki-simulated-block name="The simulated block" id=simulated-block
Let $\mathbf{A}$ be a real or complex $m\times n$ matrix, $\boldsymbol{\Omega}$ a start block with $n$ rows, and $\mathbf{H}=\mathbf{A}^{\mathsf{H}}\mathbf{A}$. For all integers $s,q\ge0$,

$$\mathsf{rbki}\bigl(\mathbf{A},\ [\boldsymbol{\Omega},\mathbf{H}\boldsymbol{\Omega},\ldots,\mathbf{H}^{s}\boldsymbol{\Omega}],\ q+1\bigr)=\mathsf{rbki}(\mathbf{A},\boldsymbol{\Omega},\ s+q+1).$$

Running $s+q+1$ blocks from $\boldsymbol{\Omega}$ gives the same approximation as running $q+1$ blocks from the wider block built from the first $s+1$ Krylov blocks of $\boldsymbol{\Omega}$. This is an identity of matrices, with no assumption on rank or on the block.
:::
