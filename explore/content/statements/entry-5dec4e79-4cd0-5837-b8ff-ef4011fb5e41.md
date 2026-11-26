---
kind: statement
id: entry-5dec4e79-4cd0-5837-b8ff-ef4011fb5e41
uid: 5dec4e79-4cd0-5837-b8ff-ef4011fb5e41
---
::: theorem result:perturbed-truncation name="Perturbed truncation"
For any $\mathbf{C}$, $\mathbf{E}$ and any best rank-$k$
approximation $\mathbf{Y}$ of $\mathbf{C} + \mathbf{E}$,
$$\|\mathbf{C} - \mathbf{Y}\|_{\mathsf{F}} \le
\|\mathbf{C} - \llbracket\mathbf{C}\rrbracket_k\|_{\mathsf{F}} +
2\,\|\llbracket\mathbf{E}\rrbracket_{2k}\|_{\mathsf{F}}\,:$$
truncating a perturbed matrix pays only the $2k$ leading singular values of the perturbation. In
the Frobenius norm it dominates the constant-two lemma
(`NLAlib.IsBestRankApprox.matrixNorm_sub_le_add_two_mul`), since
$\|\llbracket\mathbf{E}\rrbracket_{2k}\|_{\mathsf{F}} \le \|\mathbf{E}\|_{\mathsf{F}}$.
Proved without a literature source; the input is von Neumann's trace inequality. The statement is
related to the cited Proposition 6.1.
:::
