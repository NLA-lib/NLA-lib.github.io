---
kind: statement
id: entry-15d7bec3-ee64-5f60-acbb-238ec72c6ae6
uid: 15d7bec3-ee64-5f60-acbb-238ec72c6ae6
---
::: theorem result:newton-schulz-sign-accuracy name="Accuracy of the Newton–Schulz sign algorithm"
(Theorem 2.6): under the arithmetic contract
`NLAlib.FloatMachine.IsArithAccurate` $u$ $\tau$ $\Omega$ with product constant $\mu$,
$\mu(n) \ge 0$, $u \ge 0$, $0 \le \tau$, $2n\tau \le 1$ and $9(n + 1) \le \Omega$, let the
stored $\mathbf{A}$ have Hermitian decoding (written $\mathbf{A}$) with
$\|\mathbf{A}\|_2 \le b$ and every eigenvalue of modulus at least $a > 0$, for stored $b$ and
$\varepsilon$ with $0 < \varepsilon \le 1/2$ (decoded values). With $N_0 = N(a/(2b),
\varepsilon/(16n))$ (`NLAlib.newtonSchulzSteps`), if
$$640\, n^{3/2}\,(8 + \mu(n))\,(N_0 + 1)\,u \le \frac{a}{b}\,\varepsilon$$
and the step limit is at least $N_0$, then
$$\|\operatorname{sign}(\mathbf{A}) - \mathsf{newtonSchulzSign}(\mathbf{A}, \varepsilon, b)\|_2 \le
\varepsilon \,,$$
$\mathsf{newtonSchulzSign}$ the algorithm `NLAlib.newtonSchulzSign`. The cited Theorem 2.6 assumes
$u \le (a/b)\varepsilon/(4\max(N n\mu_g(n, 1.1), n^2))$, $N = N(a/b, \varepsilon/(8n))$ and
the contour bound of Lemma 2.2; here the perturbation bound is dimension-free and the factor
$n^{3/2}$ comes from the Hermitian rounding and the stopping test.
:::
