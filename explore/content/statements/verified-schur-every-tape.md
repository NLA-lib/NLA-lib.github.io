---
kind: statement
id: verified-schur-every-tape
uid: ba50b7b7-4199-5605-8b73-6702f764b5c4
---

::: theorem result:verified-schur-every-tape name="Verified solver: flag 0 implies accuracy, on every tape" id=verified-every-tape
Let the machine be as above, $0<\delta\le1$, any $\varphi$ and $u\le u_{\mathrm{ver}}$. For every complex $\mathbf{A}$ of order $n+1$, from a memory holding $\mathbf{A}$ and the words of `verifiedSchurParams`, on **every** tape the run of `verifiedSchur` terminates, writes only $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, stores the flag $0$ or $1$ and has $\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le58Ru$, with $R$ = `denseSchurRotations` at $\delta_{\mathrm{int}}$. If the flag is $0$, then $\widehat{\mathbf{T}}$ is upper triangular and $\|\mathbf{A}-\widehat{\mathbf{U}}\widehat{\mathbf{T}}\widehat{\mathbf{U}}^{\mathsf{H}}\|_2\le\delta\|\mathbf{A}\|_2$.
:::
