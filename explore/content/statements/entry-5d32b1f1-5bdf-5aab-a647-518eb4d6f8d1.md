---
kind: statement
id: entry-5d32b1f1-5bdf-5aab-a647-518eb4d6f8d1
uid: 5d32b1f1-5bdf-5aab-a647-518eb4d6f8d1
---
::: theorem result:minres-chebyshev-sharp name="MINRES attains the Chebyshev value"
For $0 < a < a'$, on the Chebyshev extrema matrix with right-hand side
$\mathbf{w}$ = `chebyshevWeightVector` and the zero start,
$$\|\mathbf{w} - \mathbf{A}\,\mathsf{gmresIterate}(\mathbf{A}, \mathbf{w}, \mathbf{0}, q)\| =
T_q\Bigl(\frac{a' + a}{a' - a}\Bigr)^{-1}\|\mathbf{w}\| = \frac{2\rho^q}{1 +
\rho^{2q}}\|\mathbf{w}\| \,.$$
As for CG, with residual weights $\lvert\mathbf{w}_k\rvert^2 = \omega_k$.
:::
