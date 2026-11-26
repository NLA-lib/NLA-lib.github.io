---
kind: statement
id: entry-d87a4d6a-1227-58b3-a62d-c7efe303ce7d
uid: d87a4d6a-1227-58b3-a62d-c7efe303ce7d
---
::: theorem result:shifted-qr-ritz-dichotomy name="The dichotomy for forward-approximate Ritz values"
Let $\mathbf{H}$ be upper Hessenberg
with $\mathbf{H}\mathbf{V} = \mathbf{V}\operatorname{diag}(\mathbf{d})$, $\mathbf{V}$ invertible,
$\kappa = \|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2$, eigenvalues separated by $\Gamma$; let
$1 \le k \le n$, $x = (2\kappa^4)^{1/(2k)} < \theta$, $c = \tfrac12(\theta/x - 1)$,
$0 < \beta < c\Gamma$, and let `rs` be within $\beta$ of the Ritz values of order $k$, entry by
entry. Then `rs` is a set of $\theta$-optimal Ritz values, or some $r$ in `rs` is an eigenvalue,
or
$$\tfrac25\,\psi_k(\mathbf{H})\Bigl(1 - \frac x\theta\Bigr) \le \kappa^{2/k}(\|\mathbf{H}\|_2 +
\beta)\,\beta\,\|\mathbf{e}_n^{\mathsf{H}}(\mathbf{H} - r\mathbf{I})^{-k}\|^{1/k}$$
for some $r$ in `rs`. Adapted from the cited result: the constant
$\tfrac25$ bounds the factor $k^{-1/(2k)}/2$, and the strict $\beta < c\Gamma$ keeps two
eigenvalues from sharing a Ritz value.
:::
