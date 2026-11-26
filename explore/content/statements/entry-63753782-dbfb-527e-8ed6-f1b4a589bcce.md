---
kind: statement
id: entry-63753782-dbfb-527e-8ed6-f1b4a589bcce
uid: 63753782-dbfb-527e-8ed6-f1b4a589bcce
---
::: theorem result:girard-hutchinson-tail name="Girard–Hutchinson: tail bound for sub-Gaussian probes"
If the entries of
the real $n \times m$ test matrix $\mathbf{\Omega}$ are independent, each satisfies the
sub-Gaussian moment generating function bound with variance proxy $c$ (`HasSubgaussianMGF`) and
has second moment $1$, then for every real square $\mathbf{B}$ and every
$\tau \ge 0$, <!-- value hansonWrightConstant -->
$$\mathbb{P}\bigl[\lvert \operatorname{tr}\mathbf{B} -
\mathsf{girardHutchinson}(\mathbf{B}, \mathbf{\Omega}) \rvert \ge \tau\bigr] \le
2\exp\Bigl(-\frac{1}{196}\min\Bigl(
\frac{m\tau^2}{c^2\|\mathbf{B}\|_{\mathsf{F}}^2}, \frac{m\tau}{c\|\mathbf{B}\|_2}\Bigr)\Bigr)\,;$$
the constant is `hansonWrightConstant`. No symmetry of $\mathbf{B}$ is needed. Junk cases: with no
columns ($m = 0$) the estimate is $0$ and the bound is $2$; a zero denominator makes its fraction
$0$, and the bound is again $2$.

Note: The proof is Hanson–Wright
(`NLAlib.measureReal_abs_quadForm_sub_integral_ge_le`) for
$m \cdot \mathsf{girardHutchinson}(\mathbf{B}, \mathbf{\Omega}) =
\operatorname{vec}(\mathbf{\Omega})^{\mathsf{T}}(\mathbf{I}_m \otimes \mathbf{B})
\operatorname{vec}(\mathbf{\Omega})$, whose matrix has squared Frobenius norm
$m\|\mathbf{B}\|_{\mathsf{F}}^2$ and spectral norm $\|\mathbf{B}\|_2$.
The cited result has unspecified constants and is stated in the
sample-size form $m = O(\log(1/\delta)/\varepsilon^2)$ for
$\lvert \cdot \rvert \le \varepsilon\|\mathbf{B}\|_{\mathsf{F}}$.
:::
