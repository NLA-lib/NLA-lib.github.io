---
kind: statement
id: entry-ad185187-bc15-5b75-b77e-4eeca6bed53f
uid: ad185187-bc15-5b75-b77e-4eeca6bed53f
---
::: theorem result:paige-stabilized-ritz-values name="Localization of stabilised Ritz values"
(assuming $k\varepsilon \le 1/100$) (Paige): for a unit eigenpair
$\mathbf{T}_k\mathbf{y} = \theta\mathbf{y}$ of the computed tridiagonal matrix, some eigenvalue
$\lambda$ of $\mathbf{H}$ satisfies <!-- value lanczosBackwardFactor k -->
$$\lvert\theta - \lambda\rvert \le \beta_k\lvert y_{k-1}\rvert +
400k^3\varepsilon\|\mathbf{H}\|_2 \,.$$
At a terminal last step ($\beta_k = 0$) this holds for every Ritz value.
No printed source; the maintainer's draft, `thm:stabilized`, states
$\lesssim_k \beta_k\lvert\mathbf{e}_k^{\mathsf{T}}\mathbf{y}\rvert + \varepsilon\|\mathbf{A}\|_2$; Paige’s theorem is the cited comparison.
:::
