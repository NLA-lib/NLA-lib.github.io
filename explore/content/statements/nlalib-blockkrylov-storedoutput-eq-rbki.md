---
kind: statement
id: nlalib-blockkrylov-storedoutput-eq-rbki
uid: 9e96e2c6-478a-5eef-8072-3b65a72a0b33
---

::: theorem decl:NLAlib.BlockKrylov.storedOutput_eq_rbki name="The stored output on the tape of a given start block" id=stored-output
Let a program be certified for the block Golub–Kahan problem with a postcondition that implies the exact-run postcondition, and let $\mathbf{A}$ be the real $m\times n$ input matrix. For every real $n\times\ell$ matrix $\mathbf{X}$, the stored product of the run on the tape carrying $\mathbf{X}$ is

$$\mathbf{U}\mathbf{S}^{\mathsf{H}}\mathbf{V}^{\mathsf{H}}=\mathsf{rbki}(\mathbf{A},\mathbf{X},q).$$

The equality holds for every $\mathbf{X}$, not almost surely, under the exact certificate.

Note: This identity lets the library transfer tail and expectation bounds for $\mathsf{rbki}(\mathbf{A},\mathbf{X},q)$ to the stored output of the counted run. For standard Gaussian $\mathbf{X}$, the library restates the gapped tail bound for every block size and the gapped expected-error bound when $t+2\le\ell$.
:::
