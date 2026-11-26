---
kind: statement
id: truncated-gn-lower-bound
uid: fddf9c5b-4258-5153-a554-e27c7168cb23
---

::: theorem result:truncated-gn-lower-bound name="An unavoidable error on hard inputs" id=lower-bound
Let $\mathbf{A}_a=\operatorname{diag}(a\mathbf{I}_k,\mathbf{I}_{n-k})$, and use independent standard Gaussian sketches with $k+2\le\ell<n$ and $p\ge\ell+2$. For every $\eta>0$, all sufficiently large $a$ satisfy

$$\mathbb E\|\mathbf{A}_a-[\mathsf{gn}(\mathbf{A}_a,\boldsymbol{\Omega},\boldsymbol{\Psi})]_k\|_{\mathrm F}^2\ge(n-k)+\frac{k(n-\ell)}{p-\ell-1}-\eta.$$

The optimal rank-$k$ squared Frobenius error is $n-k$ when $a\ge1$. The extra term shows noise that late truncation can retain even when the leading singular values become arbitrarily large. This is a lower bound for a particular family of inputs, rather than an upper guarantee for every input.
:::
