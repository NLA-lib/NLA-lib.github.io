---
kind: statement
id: entry-1155ee97-45ea-5225-bf8a-2261f7feebed
uid: 1155ee97-45ea-5225-bf8a-2261f7feebed
---
::: theorem result:random-start-log-overlap name="The mean logarithmic overlap"
For a standard Gaussian vector $\mathbf{g}$ in
$\mathbb{R}^n$ and a unit vector $\mathbf{u}$, with $N = \lvert n \rvert$,
$$\mathbb{E} \log \frac{\|\mathbf{g}\|^2}{\langle \mathbf{u}, \mathbf{g} \rangle^2}
\le \log(2N) + 2,$$
whereas the inverse squared overlap has infinite expectation when $N \ge 2$. When $N = 1$,
the quotient is $1$ almost surely and its logarithm has expectation $0$.
Integrating the tail `NLAlib.measureReal_log_norm_sq_div_sq_ge_le_of_hasLaw_gaussianVector` gives
the bound used in the random-start step of the power and Lanczos methods. The exact mean is
$\psi(N/2) - \psi(1/2) \sim \log(2N) + \gamma$ (digamma $\psi$, Euler's constant $\gamma$), so the
additive constant is not tight.
:::
