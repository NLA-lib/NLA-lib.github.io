---
kind: statement
id: entry-b3c6efe3-cf1e-571d-86b8-2112fc6f6cf7
uid: b3c6efe3-cf1e-571d-86b8-2112fc6f6cf7
---
::: theorem result:lanczos-spectral-measure-wasserstein name="The spectral measures are Wasserstein-close"
(assuming $k\varepsilon \le 1/100$): for every $1$-Lipschitz
$f$, <!-- value lanczosBackwardFactor k -->
$$\lvert\bar{\mathbf{v}}_1^{\mathsf{T}}f(\mathbf{H})\bar{\mathbf{v}}_1 -
\tilde{\mathbf{v}}^{\mathsf{T}}f(\tilde{\mathbf{H}})\tilde{\mathbf{v}}\rvert
\le 400k^3\varepsilon\|\mathbf{H}\|_2 \,,$$
so the spectral measure of $(\mathbf{H}, \bar{\mathbf{v}}_1)$ and that of the backward model
$(\tilde{\mathbf{H}}, \tilde{\mathbf{v}})$, on which exact Lanczos computes $\mathbf{T}_k$, are
within that distance in $W_1$.

Note: No printed source; the maintainer's draft, `rem:wasserstein`, bounds the difference by
$\sqrt{2k}\|\mathbf{\Delta}\|$ (through the rank of $\mathbf{\Delta}$); here directly by
$\|\mathbf{\Delta}\|_{\mathsf{F}}$.
:::
