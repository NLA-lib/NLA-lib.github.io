---
kind: statement
id: verified-schur-certificate
uid: c1ff4d2f-9c6b-5435-9fac-c5ae60632af3
---

::: theorem result:verified-schur-certificate name="Verified solver, on one counted run" id=verified-one-run
Under the hypotheses of the failure bound, the probability is at most $\varphi$ that the counted run of `verifiedSchurAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ with a Schur output of $\mathbf{A}$.
:::
