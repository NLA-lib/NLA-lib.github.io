---
kind: statement
id: entry-5da0ca0a-493a-5fba-9898-00a2bbb35d60
uid: 5da0ca0a-493a-5fba-9898-00a2bbb35d60
---
::: theorem result:cg-tiny-interval-polynomial-convergence name="Tiny-interval polynomial convergence of computed CG"
For a successful $k$-step run,
input spectrum in $[a,a']$, $a>0$, $\kappa=a'/a$ and
$k^2\sqrt{k}\varepsilon\kappa^2\le10^{-5}$, let $S$ contain all closed radius-$\delta$
intervals about the input eigenvalues, where the Frobenius backward distance is at most
$\delta$. For $j\le k$, every real polynomial $p$ of degree at most $j$ with $p(0)=1$ and
$\lvert p\rvert\le\eta$ on $S$ gives
$$\|\mathbf{x}_\star-\mathbf{x}_j\|_{\mathbf{A}}^2
\le\eta^2(\|\mathbf{x}_\star\|_{\mathbf{A}}^2+\Delta)+\Delta+R_j\,.$$
Here $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$. With
the value <!-- value cgBackwardFactor k -->$c=6000k^2\sqrt{k}\varepsilon\kappa a'$, the initial
comparison error is $\Delta=2\|\mathbf{b}\|^2c/a^2$.
The term is <!-- value cgEnergyFactor j -->$R_j=135j^2\varepsilon\kappa\|\mathbf{b}\|^2/a$.
The model error is that of exact $\mathsf{cgIterate}$ on the full backward model.
This is a squared physical-energy statement with explicit additive errors, rather
than the qualitative tiny-interval minimax discussion in the cited source.
:::
