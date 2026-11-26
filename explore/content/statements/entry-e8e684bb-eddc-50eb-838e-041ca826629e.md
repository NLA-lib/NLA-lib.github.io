---
kind: statement
id: entry-e8e684bb-eddc-50eb-838e-041ca826629e
uid: e8e684bb-eddc-50eb-838e-041ca826629e
---
::: theorem result:cg-physical-energy-decrements name="Physical energy and computed decrements"
For a successful $k$-step CG run with
spectrum in $[a,a']$, $a>0$, $\kappa=a'/a$ and
$k^2\sqrt{k}\varepsilon\kappa^2\le10^{-5}$, a solution
$\mathbf{A}\mathbf{x}_\star=\mathbf{b}$ satisfies for $j\le k$, with
error <!-- value cgEnergyFactor j -->
$R_j=135j^2\varepsilon\kappa\|\mathbf{b}\|^2/a$,
$$\|\mathbf{x}_\star-\mathbf{x}_j\|_{\mathbf{A}}^2\le
\|\mathbf{x}_\star\|_{\mathbf{A}}^2-\sum_{i<j}\gamma_i\|\mathbf{r}_i\|^2+R_j .$$
The coefficient of the computed decrement sum is exactly one.

Note: No printed source.
:::
