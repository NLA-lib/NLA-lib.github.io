---
kind: statement
id: entry-c0dbd55a-6013-5ccf-9bf4-6bceef0ec8a6
uid: c0dbd55a-6013-5ccf-9bf4-6bceef0ec8a6
---
::: theorem result:intrinsic-matrix-chernoff name="Intrinsic-dimension matrix Chernoff for the mean"
For finitely many independent, almost
everywhere measurable random $n \times n$ matrices $\mathbf{X}_k$ over $\Bbbk$ with
$\mathbf{0} \preceq \mathbf{X}_k \preceq L\mathbf{I}$ almost surely, $L > 0$, any matrix
$\mathbf{M}$ with $\sum_k \mathbb{E}\mathbf{X}_k \preceq \mathbf{M}$ (possibly $\mathbf{0}$) and
every $\theta > 0$,
$$\mathbb{E}\, \lambda_0\Bigl(\sum_k \mathbf{X}_k\Bigr)
\le \frac{e^\theta - 1}{\theta} \lambda_0(\mathbf{M}) +
\frac{L}{\theta} \log\bigl(2 \operatorname{intdim}(\mathbf{M})\bigr)\,.$$
The bound permits any upper bound $\mathbf{M}$ in Loewner order and any free
$\theta$. No assumption $\mathbf{M} \ne \mathbf{0}$ is needed: at $\mathbf{M} = \mathbf{0}$ both sides are $0$
(`Real.log 0 = 0`).
:::
