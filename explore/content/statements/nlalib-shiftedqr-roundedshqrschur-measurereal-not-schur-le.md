---
kind: statement
id: nlalib-shiftedqr-roundedshqrschur-measurereal-not-schur-le
uid: 7455a12b-551e-5cab-81d5-9a9386edaa48
---

::: theorem decl:NLAlib.ShiftedQR.roundedShQRSchur_measureReal_not_schur_le name="Schur pair with the BGS III program" id=accuracy-schur
Let $\mathbf{H}$ be upper Hessenberg of order $n+1$ with

- $\mathbf{H}\mathbf{V}=\mathbf{V}\operatorname{diag}(\mathbf{d})$ for an invertible $\mathbf{V}$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le B$, $B\ge1$;
- $|d_i-d_j|\ge\Gamma>0$ for $i\ne j$;
- $\|\mathbf{H}\|_2\le\Sigma$, $0<\delta\le\Sigma$, $0<\varphi\le1$, and $k$ the shift degree at $4B$.

Let the machine and the sampler be as above, let draws store the tape entry, let the tape have independent entries with $s_U$ uniform on $[0,1]$ and $s_G$ standard real Gaussian, and let $u\le u_0$ at tail records $c_1,c_2$ that bound the two Ginibre tails. Start the program `roundedShQRSchur` from a memory holding $\mathbf{H}$, an accumulator $\mathbf{U}_0$ and the words of `shqrSchurParams`. Then the probability is at most $\varphi$ that the run fails, writes outside the matrix, the accumulator and the failure word, or does not store the failure word $0$ and a Schur pair as in "Shape of the guarantee" above, with $R_{\mathrm{rot}}$ = `shqrSmallEigRotations`.
:::
