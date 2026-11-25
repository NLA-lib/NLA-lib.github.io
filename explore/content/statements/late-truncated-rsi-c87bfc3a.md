---
kind: statement
id: late-truncated-rsi-c87bfc3a
uid: c87bfc3a-e18e-553a-90a0-c82558421a6d
---

::: definition name="Late-truncated RSI"
First form the subspace-iteration approximation $\mathbf{B}=\mathsf{rsi}(\mathbf{A},\mathbf\Omega,p)=\mathsf{rsvd}\bigl(\mathbf{A},(\mathbf{A}^{\mathsf{H}}\mathbf{A})^p\mathbf\Omega\bigr)$. Return $[\mathbf{B}]_r$, a best rank-at-most-$r$ approximation to $\mathbf{B}$; here $[\cdot]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a test matrix of $\ell$ columns the rank of $\mathbf{B}$ is at most $\ell$; the truncated output has rank at most $r$.
:::
