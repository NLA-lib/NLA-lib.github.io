---
kind: statement
id: entry-a3c1fc4e-a1f4-5bb4-a453-7bafd4394411
uid: a3c1fc4e-a1f4-5bb4-a453-7bafd4394411
---
::: theorem result:gaussian-integration-by-parts name="Gaussian integration by parts"
(Stein's identity, covariance form): for a Gaussian vector
$\mathbf{g}$ in $\mathbb{R}^\iota$ and $f$ of class $C^1$ with $\|Df(\mathbf{x})\| \le C$,
$$\mathbb{E}[(\mathbf{g}_i - \mathbb{E}\mathbf{g}_i) f(\mathbf{g})]
= \sum_j \operatorname{Cov}(\mathbf{g}_i, \mathbf{g}_j)\, \mathbb{E}[\partial_j f(\mathbf{g})]\,.$$
For a standard Gaussian, the cited lemma states $\mathbb{E}[g f(g)] = \mathbb{E} f'(g)$.
This formulation allows any mean and covariance, possibly singular, with no centring hypothesis
(a centred consumer rewrites with `sub_zero`). The case $k = 0$ of
`integral_sub_integral_mul_eq_sum_covariance_mul_integral_fderiv_of_hasGaussianLaw_of_le_pow`.
:::
