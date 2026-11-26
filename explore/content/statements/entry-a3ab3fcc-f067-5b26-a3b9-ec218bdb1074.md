---
kind: statement
id: entry-a3ab3fcc-f067-5b26-a3b9-ec218bdb1074
uid: a3ab3fcc-f067-5b26-a3b9-ec218bdb1074
---
::: theorem result:beta-subgaussian name="Beta laws are sub-Gaussian with proxy $1/(4(\\alpha+\\beta+1))$"
For
$X \sim \mathrm{Beta}(\alpha, \beta)$ with $\alpha, \beta > 0$, the centred variable
$X - \alpha/(\alpha+\beta)$ satisfies
$$\mathbb{E}\,e^{t(X - \alpha/(\alpha+\beta))} \le \exp\Bigl(\frac{t^2}{8(\alpha+\beta+1)}\Bigr)$$
for every real $t$, the moment generating function bound with variance proxy
$1/(4(\alpha+\beta+1))$. The proxy equals the variance when $\alpha = \beta$ and exceeds it
otherwise; it improves Hoeffding's dimension-free proxy $1/4$ on $[0, 1]$
(`ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc`).

Note: The proof here is a comparison for the Riccati equation of
$(\log\mathrm{mgf})'$, not the source's (series comparison when $\alpha = \beta$, a second-order
analysis of Kummer's equation otherwise).
:::
