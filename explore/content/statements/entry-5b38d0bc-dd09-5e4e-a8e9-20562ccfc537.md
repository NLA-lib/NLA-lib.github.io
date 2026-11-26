---
kind: statement
id: entry-5b38d0bc-dd09-5e4e-a8e9-20562ccfc537
uid: 5b38d0bc-dd09-5e4e-a8e9-20562ccfc537
---
::: theorem result:linear-system-matvec-lower-bound name="The matrix–vector complexity of linear systems"
Shamir's theorem: Let $\kappa \ge 2$,
$\varepsilon > 0$ and $\lvert n \rvert \ge 20(q + 3)^2$. If a randomized algorithm (a measurable
seeded family, seed law $\rho$) making $q$ adaptive matrix–vector products, with a fixed known
right-hand side $\mathbf{b} \ne \mathbf{0}$ on which the algorithm may depend, returns for every
symmetric $\mathbf{A} \in \mathbb{R}^{n \times n}$ with spectrum in
$[-\kappa, -1] \cup [1, \kappa]$ (condition number at most $\kappa$), an
$\hat{\mathbf{x}}$ with $\|\mathbf{b} - \mathbf{A}\hat{\mathbf{x}}\| \le \varepsilon\|\mathbf{b}\|$
with probability at least $\tfrac23$, then
$$\kappa\log\frac{1}{4\varepsilon} \le 2(q + 1) \,.$$
For symmetric $\mathbf{A}$ the products $\mathbf{A}^{\mathsf{H}}\mathbf{x}$ are the same, so this
covers the oracle $\mathbf{x} \mapsto (\mathbf{A}\mathbf{x}, \mathbf{A}^{\mathsf{H}}\mathbf{x})$ of
the source. MINRES needs $O(\kappa\log(1/\varepsilon))$ products on these spectra
(`Matrix.IsHermitian.norm_sub_mulVec_gmresIterate_le_two_mul_pow_div_two`), so the bound is
sharp up to the constant.
The cited source assumes $T \ge c\kappa\log(1/\varepsilon)$, for $\kappa \ge C$, $\varepsilon \le c$
and $n = \Omega(T^2)$ with unspecified constants; this statement makes them explicit. In the
source the output is the last query (one query fewer).
:::
