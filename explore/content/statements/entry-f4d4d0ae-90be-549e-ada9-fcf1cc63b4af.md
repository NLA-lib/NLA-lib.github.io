---
kind: statement
id: entry-f4d4d0ae-90be-549e-ada9-fcf1cc63b4af
uid: f4d4d0ae-90be-549e-ada9-fcf1cc63b4af
---
::: theorem result:spectral-bisection-diagonalization-bits name="The bit count of Hermitian diagonalization"
(Theorem 4.2, in bits): let the machine meet
`NLAlib.FloatMachine.IsAccurate` with $u > 0$, monotone $\mu_{\mathrm{MM}}, \mu_{\mathrm{QR}} \ge
0$, $c_{\mathrm N} \ge 0$ and samplers with measurable fibres and countable ranges; let the stored
$n \times n$ input $\mathbf{A}$, $n \ge 1$, be Hermitian with $\|\mathbf{A}\|_2 \le R_0$, $R_0 > 0$,
$0 < \varepsilon \le 2^{-15}$, $0 < \theta \le 1$ and $\ell \ge$ `NLAlib.bisectionDepth`
$\varepsilon$; let $m = \min(n, \ell + 1)$, $\nu = 4\mu_{\mathrm{MM}}(n) + 10 + 10\sqrt n$,
$N_* =$ `NLAlib.newtonSchulzSteps` $(\theta/(12n\ell(\ell + 1)))\,(\beta/(16n))$ be at most the
step limit, the floor $0 \le \tau$ with $100n^{3/2}\tau \le \min(\sqrt{\theta/(8nm)},
\varepsilon\min(R_0, 1))$, the range $16(2R_0 + n + 2\ell + \hat T) \le \Omega$, the ideal samples
of the nodes independent with law `NLAlib.eighSampleLaw` $n$, the accuracy within $1 + 2^{-6}$
of its bound, $\hat\beta/(1 + 2^{-6}) \le \beta \le \hat\beta = (\ell - 1)^2\varepsilon\sqrt\theta/
(52\ell^2(2\ell - 1)\sqrt{nm\min(n, e)}\,\hat T)$, and
$$\begin{aligned}\log_2\frac1u \ge{}& \log_2\frac1\varepsilon + \frac32\log_2\frac1\theta +
\log_2\bigl(n(4\mu_{\mathrm{MM}}(n) + 10 + 10\sqrt n)\bigr) +
\tfrac12\log_2\bigl(n\min(n, \ell + 1)\min(n, e)\bigr) \\ &+ \log_2\hat T + \log_2(\ell(\ell + 1)) +
\log_2\frac{\ell^2(2\ell - 1)}{(\ell - 1)^2} + 13 \,,\end{aligned}$$
$\hat T = 2\sqrt2\sqrt n + \sqrt{\log(96n\min(n, \ell + 1)/\theta)}$, together with the
condition $\log_2(1/u) \ge \log_2(1/\beta) + \log_2(2048(n + N_* + 1)\nu +
16(4\mu_{\mathrm{QR}}(n) + 4\sqrt n(c_{\mathrm N} + 1) + 2\mu_{\mathrm{MM}}(n) + 1))$, the
probability that $\mathsf{eigh}(\mathbf{A}, \varepsilon, \theta)$, the decoded output of
`NLAlib.eigh`, is not an approximate diagonalization with residual $2\varepsilon R_0$ and
singular values within $\varepsilon/3$ of $1$ is at most $\theta$. This is
$\log_2(1/\varepsilon) + \tfrac32\log_2(1/\theta) + O(\log n + \log\log(1/\varepsilon))$ bits,
with the polynomial factor $n^{2.5}\max(\mu_{\mathrm{MM}}, \sqrt n)$ for $n \le \ell$; at
$\mu_{\mathrm{MM}} = \mu_{\mathrm{QR}} = 1$, $c_{\mathrm N} = \sqrt2$,
$\ell = \lceil\log_2(1/\varepsilon)\rceil + 5$ it asks for 49.1, 58.6, 74.9 and 105.4 bits at
$(n, \varepsilon, \theta) = (1, 2^{-15}, 1)$, $(10, 2^{-15}, 1)$, $(1000, 2^{-15}, 1)$,

Note: $(1000, 2^{-40}, 1/2)$. The cited theorem requires
$\log_2(1/\varepsilon) + \log_2\max(n^{1.5}\mu_{\mathrm{QR}}, n^2c_{\mathrm N},
n^{4.5}\mu_{\mathrm{MM}}) + 2\log_2\log_2(1/\varepsilon) + 1.5\log_2(1/\theta) +
\log_2\log_2(n\log_2(1/\varepsilon)/\theta) + 23$ (48.3, 63.6, 94.5, 124.0 bits at the same
points); the third power of $\ell$ comes from the corrected shift-avoidance probability.
:::
