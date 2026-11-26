---
kind: statement
id: entry-ae325865-5edf-5230-babb-d1cb28595cce
uid: ae325865-5edf-5230-babb-d1cb28595cce
---
::: theorem result:cg-spectrum-minimax-bound name="The spectrum-optimal bound for CG"
for positive definite $\mathbf{A}$ and
$\mathbf{A}\mathbf{x}_\star = \mathbf{b}$,
$$\|\mathbf{x}_\star - \mathsf{cgIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, q)\|_{\mathbf{A}}^2
\le \mathsf{residualMinimax}(\sigma(\mathbf{A}), q)^2
\|\mathbf{x}_\star - \mathbf{x}_0\|_{\mathbf{A}}^2 \,,$$
where $\mathsf{residualMinimax}(\sigma(\mathbf{A}), q) =
\min_{p}\max_{\lambda \in \sigma(\mathbf{A})}\lvert p(\lambda) \rvert$, the minimum over real $p$
with $\deg p \le q$, $p(0) = 1$. Every other bound
of this file follows from it by bounding the minimax value. For each $\mathbf{A}$ some
$\mathbf{b}$ attains it (Greenbaum):
`Matrix.PosDef.exists_re_quadForm_sub_cgIterate_eq_residualMinimax_sq_mul` and
`Matrix.PosDef.isGreatest_re_quadForm_sub_cgIterate_div` in
`NLAlib.Krylov.LinearSystems.WorstCase`. its proof gives this bound, with the maximum over the eigenvalues,
before passing to an interval, for real symmetric $\mathbf{A}$.
:::
