---
kind: algorithm
id: nystrom-bki
title: Nyström block Krylov iteration
summary: Use a block Krylov construction in a Nyström approximation.
status: outline
order: 16
theory:
- krylov-spaces
- random-matrices
library_algorithm: nystrom-bki
uses:
- nystrom
library_results: false
result_ids:
- nysbki-gapless-error
- nysbki-gapped-error
- nystrom-bki-simulated-block
---

Use a block Krylov construction in a Nyström approximation.

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.nystromBKI name="Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf A$, build the test matrix $[\mathbf\Omega,\mathbf A\mathbf\Omega,\ldots,\mathbf A^{q-1}\mathbf\Omega]$ with $q$ blocks, then apply the Nyström construction using this entire block Krylov range. The powers are retained together rather than keeping only the last one.
:::



## Components

{{ generated:components }}

## Mathematical guarantees

::: theorem result:nystrom-bki-simulated-block name="The simulated block"
Let $\mathbf H$ be a real or complex Hermitian positive-semidefinite matrix and $\mathbf\Omega$ a start block. Write $\operatorname{NysBKI}(\mathbf H,\mathbf\Omega,q)$ for the approximation defined above. For all integers $s,q\ge0$,

$$\operatorname{NysBKI}\bigl(\mathbf H,\ [\mathbf\Omega,\mathbf H\mathbf\Omega,\ldots,\mathbf H^{s}\mathbf\Omega],\ q+1\bigr)=\operatorname{NysBKI}(\mathbf H,\mathbf\Omega,\ s+q+1).$$

Running $s+q+1$ blocks from $\mathbf\Omega$ gives the same approximation as running $q+1$ blocks from the wider block formed by the first $s+1$ Krylov blocks of $\mathbf\Omega$. Positive semidefiniteness is a hypothesis of the statement.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
