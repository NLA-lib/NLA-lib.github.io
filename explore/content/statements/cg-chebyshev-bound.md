---
kind: statement
id: cg-chebyshev-bound
uid: 845426ae-8454-5066-81fd-41b93a3e12c0
---

::: theorem result:cg-chebyshev-bound name="Chebyshev convergence"
Let $\mathbf{A}$ be Hermitian with eigenvalues in $[a,a^{\prime}]$, where $a>0$,
and let $\mathbf{x}_\star$ solve $\mathbf{A}\mathbf{x}_\star=\mathbf{b}$.
Starting from an arbitrary initial guess $\mathbf{x}_0$, let $\mathbf{x}_k$ be
the $k$-th [conjugate gradient (CG)](/explore/algorithms/conjugate-gradient/)
iterate in exact arithmetic. Then, for every integer $k\ge0$,

$$\|\mathbf{x}_\star-\mathbf{x}_k\|_\mathbf{A}^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2k}\|\mathbf{x}_\star-\mathbf{x}_0\|_\mathbf{A}^2,\qquad\kappa=\frac{a^{\prime}}a.$$

Here $\|\mathbf{v}\|_\mathbf{A}^2=\mathbf{v}^{\mathsf{H}}\mathbf{A}\mathbf{v}$
is the squared energy norm.
:::
