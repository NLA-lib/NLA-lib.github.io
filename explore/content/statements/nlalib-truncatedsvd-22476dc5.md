---
kind: statement
id: nlalib-truncatedsvd-22476dc5
uid: 22476dc5-4a8c-59f3-95a5-929740cd4e5b
---

::: definition decl:NLAlib.truncatedSVD name="Truncated SVD"
Write $[\mathbf{A}]_k$ for the matrix obtained by retaining the $k$ largest singular values and their singular vectors. It has rank at most $k$. Ties can make the best approximation nonunique; the library fixes a choice.
:::
