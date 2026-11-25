---
kind: statement
id: nlalib-smalleig-smalleigprog-randomschurleafcontract
uid: 69d70e2e-9dfa-5224-b7b9-d22da53af29f
---

::: theorem decl:NLAlib.SmallEig.smallEigProg_randomSchurLeafContract name="The program is a small-block Schur solver" id=schur-leaf
On the machine and streams above, with exact natural literals up to $d_{\max}\le k_{\max}$, tail records bounding the two Ginibre tails, $0<\beta\le\Sigma$, $0<\varphi\le1$ and $u\le u^{\mathrm{fwd}}_{\mathrm{SmallEig}}$, the program with the forward words meets the small-block Schur contract on orders at most $d_{\max}$ and norms at most $\Sigma$: except with probability $\varphi$ it stores an upper triangular $\mathbf{T}_b$ and an accumulator $\mathbf{U}_b$ with $\mathbf{T}_b=\mathbf{V}_b^{\mathsf{H}}(\mathbf{B}+\mathbf{F})\mathbf{V}_b$, $\|\mathbf{F}\|_2\le\delta_b$ and $\|\mathbf{U}_b-\mathbf{V}_b\|_2\le(1+24u)^{R_L}-1$, for an exact unitary $\mathbf{V}_b$ and $R_L=k_{\max}^2+2(k_{\max}+1)\bigl((T+k_{\max})k_{\max}+6\bigr)$.
:::
