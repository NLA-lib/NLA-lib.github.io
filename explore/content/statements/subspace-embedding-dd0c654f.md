---
kind: statement
id: subspace-embedding-dd0c654f
uid: dd0c654f-b783-516b-b7c3-04b96f1a90f3
---

::: definition name="Subspace embedding"
A matrix $\mathbf{S}$ is an embedding of a subspace $V$ with squared-norm distortion $\varepsilon$ if

$$(1-\varepsilon)\|\mathbf{x}\|_2^2\le\|\mathbf{S}\mathbf{x}\|_2^2\le(1+\varepsilon)\|\mathbf{x}\|_2^2\qquad\text{for every }\mathbf{x}\in V.$$

An oblivious distribution chooses $\mathbf{S}$ independently of the fixed target subspace, with a stated success probability. The dimension and probability requirements differ among sketch laws.
:::
