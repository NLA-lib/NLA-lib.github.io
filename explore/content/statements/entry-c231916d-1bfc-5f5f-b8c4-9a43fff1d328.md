---
kind: statement
id: entry-c231916d-1bfc-5f5f-b8c4-9a43fff1d328
uid: c231916d-1bfc-5f5f-b8c4-9a43fff1d328
---
::: theorem result:beta-matrix-inverse-mean name="The inverse mean of a Beta matrix, trace form"
For an $n \times k$ Haar frame
$\mathbf{Q}$, $\mathbf{W}$ with $p$ orthonormal rows and $p + 2 \le k \le n$,
$$\mathbb{E}\|(\mathbf{W}\mathbf{Q})^{+}\|_{\mathsf{F}}^2 =
\mathbb{E}\operatorname{tr}\bigl((\mathbf{W}\mathbf{Q}\mathbf{Q}^{\mathsf{H}}
\mathbf{W}^{\mathsf{H}})^{-1}\bigr) = p\Bigl(1 + \frac{n-k}{k-p-1}\Bigr).$$
$\mathbf{W}\mathbf{Q}\mathbf{Q}^{\mathsf{H}}\mathbf{W}^{\mathsf{H}}$ is a Beta matrix; its law is
not used. At $n = k$ the value is $p$ ($\mathbf{W}\mathbf{Q}$ has orthonormal rows).

Note: The proof
writes $\mathbf{W}\mathbf{Q}$ as $\operatorname{polar}(\mathbf{G})\mathbf{V}$
(`NLAlib.hasLaw_const_mul_of_hasLaw_haarFrame_of_hasOrthonormalCols`) and the trace as
$p + \|\mathbf{K}^{+}\mathbf{L}\|_{\mathsf{F}}^2$ for the independent Gaussian blocks
$\mathbf{K} = \mathbf{G}\mathbf{V}$, $\mathbf{L} = \mathbf{G}\mathbf{V}'$.
The cited result treats the matrix $\mathbb{E}\mathbf{X}^{-1}$ over $\mathbb{R}$ and
$\mathbb{C}$; this statement uses its trace over $\mathbb{R}$, the only part their Proposition 5.7
and Lemma 6.2 use.
:::
