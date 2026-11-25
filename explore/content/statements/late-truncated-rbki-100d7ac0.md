---
kind: statement
id: late-truncated-rbki-100d7ac0
uid: 100d7ac0-44b3-5c2a-8737-9d2b4faad068
---

::: definition name="Late-truncated RBKI"
First form the block Krylov approximation $\mathbf{B}=\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q)$. Return $[\mathbf{B}]_r$, a best rank-at-most-$r$ approximation to $\mathbf{B}$; here $[\cdot]_r$ denotes the rank-$r$ truncated singular-value decomposition. For a start block of $\ell$ columns the rank of $\mathbf{B}$ is at most $q\ell$; the truncated output has rank at most $r$.
:::
