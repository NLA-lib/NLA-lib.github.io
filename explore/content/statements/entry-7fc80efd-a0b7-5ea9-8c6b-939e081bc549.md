---
kind: statement
id: entry-7fc80efd-a0b7-5ea9-8c6b-939e081bc549
uid: 7fc80efd-a0b7-5ea9-8c6b-939e081bc549
---
::: theorem result:minres-two-interval-sharp name="MINRES attains the two-interval value"
for $0 < a < a'$ and every $q$, with
$k = \lfloor q/2 \rfloor$, the two-interval matrix and right-hand side give
$$\|\mathbf{w} - \mathbf{A}\,\mathsf{gmresIterate}(\mathbf{A}, \mathbf{w}, \mathbf{0}, q)\| =
T_k\Bigl(\frac{a'^2 + a^2}{a'^2 - a^2}\Bigr)^{-1}\|\mathbf{w}\| \,,$$
which is $2\rho_2^k/(1 + \rho_2^{2k})$ with $\rho_2 = (a'/a - 1)/(a'/a + 1)$, against the
bound $2\rho_2^k$. Odd steps gain nothing: the data are symmetric, so the least-squares residual
polynomial is even. For a residual $p$ of degree at most $q$ and $u = p(\sqrt{\xi_j})$,
$v = p(-\sqrt{\xi_j})$, $\lvert u \rvert^2 + \lvert v \rvert^2 \ge 2\lvert (u + v)/2 \rvert^2$, and
$(u + v)/2 = P(\xi_j)$ for the even part $P(x^2)$ of $p$, of degree at most $\lfloor q/2 \rfloor$;
so the residual is at least the interval value on $[a^2, a'^2]$, which the even Chebyshev residual
attains.
:::
