---
kind: statement
id: entry-ea8e5b65-3cf4-568b-aa9d-e6b25b8a4cf1
uid: ea8e5b65-3cf4-568b-aa9d-e6b25b8a4cf1
---
::: theorem result:one-pass-low-rank-lower-bound name="One-pass low-rank approximation needs $\\Omega(k/\\varepsilon)$ matrix–vector products"
Let $k$, $m$ and $q$ be natural numbers and $n = k + 3m$, with
$0 < \varepsilon \le \varepsilon_0$, $\varepsilon \le k/C_1$ and
$m = \lfloor k/(8\varepsilon) \rfloor$. Let $(\mathcal{A}_s)$ be a randomized algorithm, that is,
a measurable family of algorithms with seed $s$ drawn from a probability measure $\rho$, where
every $\mathcal{A}_s$ makes $q$ matrix–vector products with its input $\mathbf{A}$ in one pass
(all products are chosen before any response is seen) and returns
$\mathbf{W} \in \mathbb{R}^{n \times k}$ and $\mathbf{M} \in \mathbb{R}^{k \times n}$. If for
every symmetric $\mathbf{A} \in \mathbb{R}^{n \times n}$
$$\mathbb{P}_{s \sim \rho}\bigl[\|\mathbf{A} - \mathbf{W}\mathbf{M}\|_{\mathsf{F}}^2 \le
(1 + \varepsilon)\|\mathbf{A} - \llbracket \mathbf{A} \rrbracket_k\|_{\mathsf{F}}^2\bigr]
\ge \frac{1}{2} \,,$$
then
$$q > \frac{k}{C\varepsilon} \,.$$
Here $C = 6400$, $\varepsilon_0 = 1/6500$ and $C_1 = 14000$.

Note: No printed source.
:::
