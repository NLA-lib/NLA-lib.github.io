---
kind: statement
id: entry-aa94b434-afe8-51dd-a7bb-bd57f4fdb619
uid: aa94b434-afe8-51dd-a7bb-bd57f4fdb619
---
::: theorem result:stochastic-lanczos-quadrature-error name="The error of stochastic Lanczos quadrature and the minimax error"
for Hermitian
$\mathbf{A}$ with spectrum in $[a, a']$, $f$ continuous on $[a, a']$, every test matrix
$\mathbf{\Omega}$ with $m$ columns and $q + 1$ Lanczos steps per probe,
$$\bigl\lvert\operatorname{tr} f(\mathbf{A}) -
\mathsf{slq}(\mathbf{A}, f, \mathbf{\Omega}, q + 1)\bigr\rvert \le
\bigl\lvert\operatorname{tr} f(\mathbf{A}) - \mathsf{girardHutchinson}(f(\mathbf{A}),
\mathbf{\Omega})\bigr\rvert + \frac{2E_{2q + 1}(f; [a, a'])\|\mathbf{\Omega}\|_{\mathsf{F}}^2}{m}
\,,$$
$E_{2q + 1}$ the error of the best uniform approximation of $f$ on $[a, a']$ by polynomials of
degree at most $2q + 1$ (`minimaxError`). Ubaru, Chen, and Saad bound the quadrature error through analytic $f$ and Chebyshev
approximation; the inherited locator still needs checking.
:::
