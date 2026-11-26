---
kind: statement
id: entry-e35c703b-0a4f-5a13-bd9d-05dff589ab73
uid: e35c703b-0a4f-5a13-bd9d-05dff589ab73
---
::: theorem result:lagrange-basis-relative-gap-bound name="Lagrange basis polynomials below relatively separated nodes"
Let
$\lambda_0, \dots, \lambda_{t-1}$ be real nodes with
$\lambda_{k+1} \le (1 - \Delta)\lambda_k$ for $k + 1 < t$ and some $\Delta > 0$, and let
$0 \le x \le \lambda_k$ for every $k$ (so the nodes are nonnegative and non-increasing, and
$x$ is at most the smallest). Then every Lagrange basis polynomial
$\ell_i(x) = \prod_{k \ne i}(x - \lambda_k)/(\lambda_i - \lambda_k)$ of the nodes has
$$\lvert\ell_i(x)\rvert \le \Delta^{-(t-1)}\,.$$
Each of the $t - 1$ factors is at most $\Delta^{-1}$: for $k < i$,
$\lvert x - \lambda_k\rvert \le \lambda_k$ and $\lambda_k - \lambda_i \ge \Delta\lambda_k$; for
$k > i$, $\lvert x - \lambda_k\rvert \le \lambda_{k-1}$ and
$\lambda_i - \lambda_k \ge \Delta\lambda_{k-1}$. Positivity of the nodes is not assumed: where
nodes coincide (necessarily at $0$) the division convention $a/0 = 0$ makes the factor vanish.
The exponent is in $\mathbb{N}$; for $t = 0$ there is no basis polynomial.
Meyer, Musco, and Musco treat squared head singular values of a positive semidefinite matrix,
with the gap relative to the smaller of two consecutive singular values; their constants differ.
:::
