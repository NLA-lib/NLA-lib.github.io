---
kind: statement
id: cg-chebyshev-bound
uid: 845426ae-8454-5066-81fd-41b93a3e12c0
---

::: theorem result:cg-chebyshev-bound name="Chebyshev convergence"
If the eigenvalues of $A$ lie in $[a,a^{\prime}]$, $a>0$, then

$$\|x_\star-x_k\|_A^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2k}\|x_\star-x_0\|_A^2,\qquad\kappa=\frac{a^{\prime}}a.$$

The positive spectral interval controls the rate. The implementation pages connect this mathematical result to stored solver outputs.
:::
