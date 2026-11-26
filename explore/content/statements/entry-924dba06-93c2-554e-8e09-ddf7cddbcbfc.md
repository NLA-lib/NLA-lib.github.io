---
kind: statement
id: entry-924dba06-93c2-554e-8e09-ddf7cddbcbfc
uid: 924dba06-93c2-554e-8e09-ddf7cddbcbfc
---
::: theorem result:chi-square-small-ball name="Small-ball bound for $\chi^2$, exact density"
for a standard Gaussian vector $\mathbf{g}$
of dimension $d = \lvert n \rvert$ and $u \ge 0$,
$$\mathbb{P}[\|\mathbf{g}\|^2 \le u] \le \frac{(u/2)^{d/2}}{\Gamma(d/2 + 1)}\,,$$
from the $\chi^2_d$ density (`NLAlib.integral_comp_norm_of_hasLaw_gaussianVector`) after dropping
$e^{-u/2} \le 1$; for $d = 0$ both sides are $1$. It dominates the Chernoff small ball
`NLAlib.measureReal_norm_sq_le_le_rpow_of_hasLaw_gaussianVector` by
$\Gamma(x + 1) \ge (x/e)^x$ (`Real.rpow_mul_exp_neg_le_Gamma_add_one`), which is proved from it
(docs/contributing/statements.md §2, rule 6); asymptotically it is smaller by the Stirling factor
$\sqrt{\pi d}$.
:::
