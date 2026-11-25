---
kind: statement
id: nlalib-floatmachine-isaccurate-measurereal-not-isapproxdiagonalization-eigh-bisectiondepth-le-of-logb-le-of-haslaw-eighsamplelaw
uid: 0510eeec-6054-5ba1-8745-0037739c3d9a
---

::: theorem decl:NLAlib.FloatMachine.IsAccurate.measureReal_not_isApproxDiagonalization_eigh_bisectionDepth_le_of_logb_le_of_hasLaw_eighSampleLaw name="Precision in bits" id=precision
Let $\mathbf{A}\in\mathbb C^{n\times n}$ be Hermitian, with $n\ge1$ and $\|\mathbf{A}\|_2\le R_0$, where $R_0>0$. Given an accuracy target $0<\varepsilon\le2^{-15}$ and failure probability $0<\theta\le1$, write

$$\Lambda=\log_2\frac1\varepsilon+\log_2\frac1\theta+\log_2 n.$$

For arithmetic with unit roundoff $u=2^{-p}$, the numerical reference has the accuracy guarantee below if

$$p\ge\log_2\frac1\varepsilon+\frac32\log_2\frac1\theta+\frac72\log_2 n+4\log_2\Lambda+24.$$

Use depth $L=\lceil\log_2(1/\varepsilon)\rceil+5$, sign-iteration cap $c\ge\lceil4\Lambda\rceil$, and a stored parameter satisfying

$$\frac{\varepsilon\sqrt\theta}{2048(n\Lambda)^{3/2}}\le\beta\le\frac{\varepsilon\sqrt\theta}{1024(n\Lambda)^{3/2}}.$$

The arithmetic must meet the primitive accuracy contracts with $\mu_{\mathrm{MM}}(d)=\mu_{\mathrm{QR}}(d)=2d$ and $c_{\mathrm N}=\sqrt2$. Its absolute-error floor $\tau\ge0$ and range $\Omega$ must satisfy

$$300n^3\tau\le\varepsilon\theta\min(R_0,1),\qquad64(R_0+n+\Lambda)\le\Omega.$$

With independent node samples having the prescribed uniform/Gaussian law and the theorem's sampler measurability assumptions, the reference output satisfies

$$\|\mathbf{A}-\mathbf{U}\operatorname{diag}(\mathbf{d})\mathbf{U}^{\mathsf{H}}\|_2\le2\varepsilon R_0,$$

$$(1-\varepsilon/3)^2\mathbf{I}\preceq\mathbf{U}^{\mathsf{H}}\mathbf{U}\preceq(1+\varepsilon/3)^2\mathbf{I}$$

with probability at least $1-\theta$. Thus sufficient precision grows logarithmically with dimension, inverse tolerance, and inverse failure probability. For example, $n=1000$, $\varepsilon=2^{-15}$ and $\theta=1/100$ require 104 bits by this bound, giving a success probability of at least $99\%$ under the stated assumptions.
:::
