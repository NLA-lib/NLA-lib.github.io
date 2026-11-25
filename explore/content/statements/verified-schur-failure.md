---
kind: statement
id: verified-schur-failure
uid: 045e0daf-23ac-5e28-a6ba-063cb765120c
---

::: theorem result:verified-schur-failure name="Verified solver: the flag is nonzero with probability at most φ" id=verified-failure
Let the machine and the streams be as in the dense Schur theorem, $0<\delta\le1$, $0<\varphi\le1$ and $u\le u_{\mathrm{ver}}$. For every complex $\mathbf{A}$ of order $n+1$, the probability is at most $\varphi$ that the run fails, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ and a Schur pair with backward error $\delta_{\mathrm{int}}\|\mathbf{A}\|_2$ and $\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le58Ru$. In particular $\mathbb P[\text{flag}\ne0]\le\varphi$.
:::
