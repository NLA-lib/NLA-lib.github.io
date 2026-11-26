---
kind: statement
id: entry-2dab2e99-9e62-57a3-ac24-badfa56b765f
uid: 2dab2e99-9e62-57a3-ac24-badfa56b765f
---
::: theorem result:least-squares-perturbation name="Perturbation of a least-squares solution"
Let $\mathbf{A}$ have full column rank and
$\|\mathbf{A}^{+}\|_2 \|\mathbf{E}\|_2 < 1$. If $\mathbf{x}$ solves the problem
$(\mathbf{A}, \mathbf{b})$ and $\mathbf{y}$ solves
$(\mathbf{A} + \mathbf{E}, \mathbf{b} + \mathbf{f})$, then
$$\begin{aligned}
  \|\mathbf{y} - \mathbf{x}\| &\le \|(\mathbf{A} + \mathbf{E})^{+}\|_2
  \bigl(\|\mathbf{f}\| + \|\mathbf{E}\|_2 \|\mathbf{x}\| \\
  &\qquad + \|\mathbf{A}^{+}\|_2 \|\mathbf{E}\|_2 \|\mathbf{b} - \mathbf{A}\mathbf{x}\|\bigr).
\end{aligned}$$

:::
