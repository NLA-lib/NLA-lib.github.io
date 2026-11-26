---
kind: statement
id: cg-chebyshev-bound
uid: 845426ae-8454-5066-81fd-41b93a3e12c0
references:
  - key: Saad2003
    locator: (6.128)
---

::: theorem result:cg-chebyshev-bound name="Chebyshev convergence"
If the eigenvalues of $\mathbf{A}$ lie in $[a,a^{\prime}]$, $a>0$, then

$$\|\mathbf{x}_\star-\mathbf{x}_k\|_\mathbf{A}^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2k}\|\mathbf{x}_\star-\mathbf{x}_0\|_\mathbf{A}^2,\qquad\kappa=\frac{a^{\prime}}a.$$

The positive spectral interval controls the rate. The implementation pages connect this mathematical result to stored solver outputs.
:::
