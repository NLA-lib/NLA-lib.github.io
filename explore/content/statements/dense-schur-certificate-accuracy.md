---
kind: statement
id: dense-schur-certificate-accuracy
uid: db934d13-3642-524f-9980-66c833e0f17a
---

::: theorem result:dense-schur-certificate-accuracy name="On one counted run" id=one-run
Under the hypotheses of the dense Schur theorem, the probability is at most $\varphi$ that the counted run of `denseSchurAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ and a Schur pair with the two bounds of that theorem. The work and span bound is `denseSchurWork`.
:::
