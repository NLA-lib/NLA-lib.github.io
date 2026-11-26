---
kind: statement
id: entry-f67bedbe-c1e0-5d73-9c75-58aefd15bf99
uid: f67bedbe-c1e0-5d73-9c75-58aefd15bf99
---
::: theorem result:greenbaum-backward-model name="Greenbaum-type backward model for finite-precision Lanczos"
(assuming $k\varepsilon \le 1/100$): the symmetric backward model
$\tilde{\mathbf{H}}$ is close to $\mathbf{I}_{k+1} \otimes
\mathbf{H}$, <!-- value lanczosBackwardFactor k -->
$$\|\tilde{\mathbf{H}} - \mathbf{I}_{k+1} \otimes \mathbf{H}\|_{\mathsf{F}}
\le 400k^3\varepsilon\|\mathbf{H}\|_2 \,,$$
and it satisfies the computed recurrence exactly with orthonormal vectors
(`NLAlib.LanczosRun.backwardH_mul_dilatedBasis`), so exact Lanczos on it from the dilated
starting vector computes $\mathbf{T}_k$ and $\beta_k$
(`NLAlib.LanczosRun.lanczosTridiagonal_backwardH_dilatedStart`).
No printed source; the maintainer's draft, `thm:greenbaum`, states
$\|\mathbf{\Delta}\|_2 \lesssim_k \varepsilon\|\mathbf{A}\|_2$ (its formalization:
$480000k^6$ in the spectral norm); the Frobenius norm here is at least the spectral norm.
The cited result has a perturbation of order $\varepsilon^{1/4}$.
:::
