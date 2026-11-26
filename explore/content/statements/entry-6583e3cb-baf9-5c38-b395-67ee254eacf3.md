---
kind: statement
id: entry-6583e3cb-baf9-5c38-b395-67ee254eacf3
uid: 6583e3cb-baf9-5c38-b395-67ee254eacf3
---
::: theorem result:randomized-kaczmarz name="$O(\\|\\mathbf{A}\\|_{\\mathsf{F}}^2\\|\\mathbf{A}^{+}\\|_2^2\\log(1/\\varepsilon))$ iterations suffice for randomized Kaczmarz"
There are absolute constants $C, \varepsilon_0 > 0$ such that
for $\mathbf{A}\mathbf{x}_\star = \mathbf{b}$, $\mathbf{x}_\star - \mathbf{x}_0$ in the row space
of $\mathbf{A}$, rows drawn independently from the squared-row-norm law, row $i$ with probability
$\|\mathbf{a}_i\|^2/\|\mathbf{A}\|_{\mathsf{F}}^2$ ($\mathbf{a}_i$ the rows of $\mathbf{A}$),
$0 < \varepsilon \le \varepsilon_0$ and
$q \ge C\|\mathbf{A}\|_{\mathsf{F}}^2\|\mathbf{A}^{+}\|_2^2\log(1/\varepsilon)$,
$$\mathbb{E}\|\mathbf{x}_\star - \mathsf{kaczmarzIterate}(\mathbf{A}, \iota, \mathbf{b},
\mathbf{x}_0, q)\|^2 \le \varepsilon\|\mathbf{x}_\star - \mathbf{x}_0\|^2\,.$$
The constants come before every dimension. Proved from
`NLAlib.integral_norm_sub_kaczmarzIterate_sq_le_mul_of_hasLaw_iidSequence_of_mul_log_le`
with $C = 1$ and
$\varepsilon_0 = 1$. The cited bound counts $2\kappa(\mathbf{A})^2\log(1/\varepsilon)$ steps for the unsquared error.
Asymptotic: NLAlib.integral_norm_sub_kaczmarzIterate_sq_le_mul_of_hasLaw_iidSequence_of_mul_log_le
:::
