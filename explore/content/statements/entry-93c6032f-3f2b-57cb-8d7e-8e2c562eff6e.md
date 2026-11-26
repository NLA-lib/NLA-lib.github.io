---
kind: statement
id: entry-93c6032f-3f2b-57cb-8d7e-8e2c562eff6e
uid: 93c6032f-3f2b-57cb-8d7e-8e2c562eff6e
---
::: theorem result:jl-distributional name="Distributional Johnson–Lindenstrauss for a Gaussian sketch"
For every unit $\mathbf{x}$
and every $\varepsilon \ge 0$,
$$\mathbb{P}\bigl[\varepsilon \le \lvert \|\mathbf{S}\mathbf{x}\|^2 - 1 \rvert\bigr]
\le 2 e^{-\lvert k \rvert (\varepsilon^2/4 - \varepsilon^3/6)} \,;$$
$\|\mathbf{S}\mathbf{x}\|^2 = \|\mathbf{G}\mathbf{x}\|^2/\lvert k \rvert$ is
$\chi^2_{\lvert k \rvert} / \lvert k \rvert$
(`NLAlib.measureReal_abs_norm_sq_div_card_sub_one_ge_le_of_hasLaw_gaussianVector`).
Woodruff's bound uses $\varepsilon^2\lvert k \rvert/16$ in the exponent. The exponent displayed here is
that of Dasgupta and Gupta, discussed by Martinsson and Tropp. No $\varepsilon < 1$: the bound
is at least $2$ for $\varepsilon \ge 3/2$.
:::
