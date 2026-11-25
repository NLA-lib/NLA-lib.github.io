---
kind: statement
id: shifted-qr-rounded-small-eig-certificate-accuracy
uid: bfa69b03-df3e-57c8-a9a5-dbb0ca6bab06
---

::: theorem result:shifted-qr-rounded-small-eig-certificate-accuracy name="On one counted run, with the BGS III program" id=one-run-small-eig
Under the hypotheses of the theorem above, the probability is at most $\varphi$ that the counted run of `shqrSmallEigAlgorithm` fails, exceeds its budget, scratch, memory, work or span, writes outside the matrix, the accumulator and the failure word, or does not store an upper triangular $\widehat{\mathbf{T}}$ whose diagonal lists the spectrum of a matrix $\mathbf{H}+\mathbf{E}$ with $\|\mathbf{E}\|_2\le\delta$. The work and span bound is the certificate's $967736\,(n+1)^3(k+1)^4(n_p+1)(F+1)(T+1)^2$.
:::
