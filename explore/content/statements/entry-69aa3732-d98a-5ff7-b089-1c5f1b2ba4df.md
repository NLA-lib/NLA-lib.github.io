---
kind: statement
id: entry-69aa3732-d98a-5ff7-b089-1c5f1b2ba4df
uid: 69aa3732-d98a-5ff7-b089-1c5f1b2ba4df
---
::: theorem result:cg-tiny-interval-computed-residual name="Computed residual convergence on tiny intervals"
For a successful $k$-step run,
input spectrum in $[a,a']$, $a>0$, $\kappa=a'/a$ and
$k^2\sqrt{k}\varepsilon\kappa^2\le10^{-5}$, let $S$ contain all closed radius-$\delta$
intervals about the input eigenvalues, with Frobenius backward distance at most $\delta$.
For $j\le k$, a real polynomial $p$ of degree at most $j$, $p(0)=1$ and
$\lvert p\rvert\le\eta$ on $S$ gives
$$\|\mathbf{r}_j\|^2\le(a'+a/2)\eta^2
(\|\mathbf{x}_\star\|_{\mathbf{A}}^2+\Delta)\,.$$
Here $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$; the coefficient
<!-- value cgBackwardFactor k -->$c=6000k^2\sqrt{k}\varepsilon\kappa a'$ gives
$\Delta=2\|\mathbf{b}\|^2c/a^2$.
Exact $\mathsf{cgIterate}$ on the full model reproduces the computed residual norms.
The polynomial set is retained and no residual gap is assumed.
:::
