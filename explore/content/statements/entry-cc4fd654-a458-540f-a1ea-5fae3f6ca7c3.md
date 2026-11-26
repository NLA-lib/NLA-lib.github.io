---
kind: statement
id: entry-cc4fd654-a458-540f-a1ea-5fae3f6ca7c3
uid: cc4fd654-a458-540f-a1ea-5fae3f6ca7c3
---
::: theorem result:lanczos-backward-model name="Geometric Lanczos backward error"
The backward error with coefficient growth retained as a
finite geometric sum.
Writing $G_k=(1+\varepsilon)\sum_{i<k}(1+8\varepsilon)^{i+1}$, the bound
is <!-- value lanczosSmallRoundoffBackwardFactor k -->
$1000k^2\varepsilon(1+G_k)\|\mathbf H\|_2$.
Only local accuracy is assumed, and terminal breakdown is allowed. The geometric sum may
be large; this theorem does not assert convergence as the number of steps increases.

Note: No printed source. It uses `NLAlib.LanczosRun.β_le_geom_sum` as a coefficient certificate.
:::
