---
kind: statement
id: entry-bcacf146-da41-5661-af89-a0cdb2acd901
uid: bcacf146-da41-5661-af89-a0cdb2acd901
---
::: theorem result:gauss-lobatto-remainder name="The Gauss–Lobatto remainder"
for a finite measure $\mu$ supported in $[a, b]$, $a < b$,
every $k$, and $f$ continuous on $[a, b]$ and $C^{2k+2}$ on $(a, b)$, there is $\xi \in (a, b)$
with
$$\int f\,d\mu - \int f\,d\,\mathsf{lobattoQuadrature}(\mu, a, b, k) =
\frac{f^{(2k+2)}(\xi)}{(2k+2)!}\int(x - a)(x - b)\,\hat\pi_k(x)^2\,d\mu(x)\,,$$
$\hat\pi_k$ the monic orthogonal polynomial of degree $k$ of `lobattoMeasure μ a b`.
The source locators require checking.
:::
