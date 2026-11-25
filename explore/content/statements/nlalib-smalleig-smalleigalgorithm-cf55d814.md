---
kind: statement
id: nlalib-smalleig-smalleigalgorithm-cf55d814
uid: cf55d814-21be-5b57-b8ce-33a3917607de
---

::: definition decl:NLAlib.SmallEig.smallEigAlgorithm name="Certificate of the small-eigenvalue solver" id=certificate
The fixed program `smallEigProgram`, with unit costs and no oracle, succeeds on every admitted input, every interpretation of the model and every tape. It stays within the static budget, scratch and memory, writes only the matrix buffer and the accumulator, and leaves both stored. At the sizes $(n,n_q,T)$, for a matrix of order $n+1$, $n_q$ parameter words and the loop cap $T$, its work and span are at most

$$517058\,(n+1)^4(T+1)^2.$$
:::
