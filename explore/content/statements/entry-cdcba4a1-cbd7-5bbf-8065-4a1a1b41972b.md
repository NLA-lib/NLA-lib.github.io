---
kind: statement
id: entry-cdcba4a1-cbd7-5bbf-8065-4a1a1b41972b
uid: cdcba4a1-cbd7-5bbf-8065-4a1a1b41972b
---
::: theorem result:lanczos-backward-model-small-roundoff name="Quadratic backward error under small roundoff"
For a $k$-step finite-precision
Lanczos run with $k^2\varepsilon \le 10^{-3}$, the same exact backward model satisfies the bound
with factor <!-- value lanczosSmallRoundoffBackwardFactor k -->
$$\|\tilde{\mathbf{H}}-\mathbf{I}_{k+1}\otimes\mathbf{H}\|_{\mathsf{F}}
\le 1000k^2\varepsilon\|\mathbf{H}\|_2 \,.$$
 The exact model bounds its own coefficients; the additional smallness
condition absorbs its perturbation into the right-hand side. Terminal breakdown is allowed.

Note: No printed source.
:::
