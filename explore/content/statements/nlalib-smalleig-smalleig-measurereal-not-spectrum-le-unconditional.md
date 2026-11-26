---
kind: statement
id: nlalib-smalleig-smalleig-measurereal-not-spectrum-le-unconditional
uid: 4db025d7-bfbb-5ade-a7bc-94a4f0d7e94f
---

::: theorem decl:NLAlib.SmallEig.smallEig_measureReal_not_spectrum_le_unconditional name="Theorem 1.1: eigenvalues, backward error" id=accuracy
Let the machine and the streams be as above, with $u\le u_{\mathrm{SmallEig}}$ at the proved tail records. Let $n+1\le n_{\max}$, let $\mathbf{M}$ be a complex matrix of order $n+1$ with $\|\mathbf{M}\|_2\le\Sigma$, and let $0<\delta\le\Sigma$ and $0<\varphi\le1$. Start `smallEigProg` from a memory holding $\mathbf{M}$ and the parameter words. Then, for a random tape with the stream laws,

$$\mathbb{P}\bigl[\text{the run fails, writes outside the matrix and the accumulator, or does not store an upper triangular }\widehat{\mathbf{T}}_b\text{ whose diagonal lists }\operatorname{spec}(\mathbf{M}+\mathbf{E})\text{ with }\|\mathbf{E}\|_2\le\delta\bigr]\le\varphi.$$
:::
