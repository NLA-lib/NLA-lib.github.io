---
kind: statement
id: entry-5f90ea70-40c1-54dd-9dc5-83fd2ea6fda8
uid: 5f90ea70-40c1-54dd-9dc5-83fd2ea6fda8
---
::: theorem result:hermitian-diagonalization-precision-lower-bound name="Hermitian diagonalization needs $\\log_2(1/\\varepsilon) + \\tfrac12\\log_2 n - 2$ bits"
(Proposition 1.1): for $t \ge 1$, $0 < \varepsilon < 1$ and $n = 2^b$, any method that maps the
input rounded to nearest with $t$ significant bits (`Real.roundNearest`) of every real symmetric
$n \times n$ matrix $\mathbf{A}$ to $(\mathbf{U}, \mathbf{d})$ with
$\|\mathbf{A} - \mathbf{U}\operatorname{diag}(\mathbf{d})\mathbf{U}^{\mathsf{H}}\|_2 \le
\varepsilon\|\mathbf{A}\|_2$ has
$$t \ge \log_2\frac1\varepsilon + \frac b2 - 2 + \log_2(1 - \varepsilon) \,.$$
The cited result omits the term $\log_2(1 - \varepsilon)$, which comes from
$\|\mathbf{H} \pm \delta\mathbf{J}\|_2 \ne \|\mathbf{H}\|_2$.
:::
