---
kind: statement
id: nlalib-cgs2-cgs2extendroutine-meets
uid: 4e574a88-17af-5903-a933-df1cef419a4e
---

::: theorem decl:NLAlib.CGS2.cgs2ExtendRoutine_meets name="The program meets the rounded contract" id=rounded-execution
Assume the standard model of rounded arithmetic with unit roundoff $u$, the level-one contracts with dot-product error $e_d(n)$, update error $e_a$, square-root error $e_s$, and scaling error $e_c$, with $e_a,e_s\ge0$, and exact comparisons. Let $0\le\eta_0\le1/100$, $c\le1/100$, $u\ge0$, $4u\le c$, $0\le E\le1/100$, and let $\tau>0$ be the rational threshold of the implementation. At every admitted dimension $(n,k,\ell)$ assume that the level-one operations admit the length $n$, that $e_d(n)\ge0$, that the pass budget of $k+\ell$ columns holds,

$$(k+\ell+1)\,e_d(n)(1+\eta_0)^2+\bigl((1+e_a)^{k+\ell}-1\bigr)\bigl(1+(k+\ell)(1+e_d(n))(1+\eta_0)^2\bigr)\le c,$$

and that the computed norms are accurate to $E$: $e_d(n)+e_s(1+e_d(n))\le E$. Assume also $e_c\le E$. Then the implementation runs on all admitted operands and its decoded output is a rounded extension with window $\eta_0$ and parameters

$$\mu=4c+\frac{8(\eta_0+c)^2}{\tau}+5E,\qquad\varepsilon=3c+2E+2\tau.$$

Here $c$ is the budget of one classical pass against all stored columns and $E$ the relative accuracy of the computed norms and of the scaling. The bound on a kept column is absolute, so the guarantee covers every returned column.
:::
