---
kind: statement
id: small-eig-forward-error
uid: 5122ab2d-9ad3-5c4d-a1d7-1ae5aed4b848
---

::: theorem result:small-eig-forward-error name="Corollary 1.3: forward error" id=forward
Let the machine and the streams be as above, with exact natural literals up to $k_{\max}$, and let $0<\beta\le\Sigma$ and $0<\varphi\le1$. Let $u\le u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$ at the proved tail records. Take the parameter words and the cap of the forward form at $k_{\max}$. For $\mathbf{M}$ of order $n+1\le k_{\max}$ with $\|\mathbf{M}\|_2\le\Sigma$, except with probability at most $\varphi$, the run writes only the matrix and the accumulator and stores $\widehat{\mathbf{T}}_b$ with $|(\widehat{\mathbf{T}}_b)_{ii}-\lambda_i|\le\beta$ for a listing $\lambda_1,\dots,\lambda_{n+1}$ of the eigenvalues of $\mathbf{M}$ with multiplicity.
:::
