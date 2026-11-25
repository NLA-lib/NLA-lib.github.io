---
kind: statement
id: shifted-qr-rounded-schur-any-leaf
uid: 806dec5b-0402-5070-b77e-7e1cb8ddef57
---

::: theorem result:shifted-qr-rounded-schur-any-leaf name="Schur pair with any small-block solver" id=accuracy
Let $B\ge1$, $\Gamma>0$, $0<\delta\le\Sigma$, $0<\varphi\le1$, and let $k$ be the shift degree at $4B$. Let the machine and the sampler be as above, let the uniform stream have its law, and let `L` meet the small-block contract with $\beta_L$, $\varphi_L$ and $\varepsilon_L$ in the ranges above and twelve words. Let $u\le u_{\mathrm{ShQR}}$ and $u\le u_{\mathrm{replay}}$.

Then `roundedShQRSchurWith L` meets the Schur core contract. For every upper Hessenberg $\mathbf{H}$ of order at most $n+1$ with $\|\mathbf{H}\|_2\le\Sigma$ that has a diagonalization $\mathbf{H}\mathbf{V}=\mathbf{V}\operatorname{diag}(\mathbf{d})$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le B$ and $|d_i-d_j|\ge\Gamma$ for $i\ne j$, and every stored accumulator $\mathbf{U}_0$, the probability is at most $\varphi$ that the run fails, writes outside the matrix, the accumulator and the failure word, or does not store the failure word $0$ and a Schur pair as in "Shape of the guarantee" above.
:::
