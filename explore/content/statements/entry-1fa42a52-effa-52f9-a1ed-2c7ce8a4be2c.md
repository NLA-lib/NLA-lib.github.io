---
kind: statement
id: entry-1fa42a52-effa-52f9-a1ed-2c7ce8a4be2c
uid: 1fa42a52-effa-52f9-a1ed-2c7ce8a4be2c
---
::: theorem result:cg-delayed-energy-stopping name="Certified delayed-energy stopping"
For a successful $k$-step CG run with spectrum
in $[a,a']$, $a>0$, $k^2\sqrt{k}\varepsilon(a'/a)^2\le10^{-5}$, solution
$\mathbf{A}\mathbf{x}_\star=\mathbf{b}$ and $j+d\le k$, suppose the terminal energy
is at most $T$. If the delayed decrement sum plus $T$ and the input-only rounding allowance
of <!-- value cgEnergyEstimatorFactor j d -->
$150d(j+d)\varepsilon(a'/a)\|\mathbf{b}\|^2/a$
is at most the requested tolerance, the physical energy at $j$ is at most that tolerance.
A small delayed sum alone is insufficient when the terminal tail or rounding allowance is large.

Note: No printed source.
:::
