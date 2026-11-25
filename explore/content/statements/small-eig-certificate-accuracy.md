---
kind: statement
id: small-eig-certificate-accuracy
uid: 96f14e8b-ee12-585f-a7a5-5142971ee656
---

::: theorem result:small-eig-certificate-accuracy name="On one counted run" id=one-run
Under the hypotheses of Theorem 1.1, the probability is at most $\varphi$ that the counted run of `smallEigAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside the matrix and the accumulator, or does not store an upper triangular $\widehat{\mathbf{T}}_b$ whose diagonal lists the spectrum of a matrix $\mathbf{M}+\mathbf{E}$ with $\|\mathbf{E}\|_2\le\delta$. The work and span bound is the certificate's $517058\,(n+1)^4(T+1)^2$.
:::
