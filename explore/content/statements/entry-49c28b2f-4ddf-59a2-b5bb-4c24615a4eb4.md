---
kind: statement
id: entry-49c28b2f-4ddf-59a2-b5bb-4c24615a4eb4
uid: 49c28b2f-4ddf-59a2-b5bb-4c24615a4eb4
---
::: theorem result:inverse-polynomial-approx name="Polynomial approximation of the inverse"
For $0<a<b$, there is a polynomial of degree
less than $q$ such that
$$\left\lvert p(x)-x^{-1}\right\rvert\le\frac2a
\left(\frac{\sqrt b-\sqrt a}{\sqrt b+\sqrt a}\right)^q\quad(x\in[a,b]).$$
This is a scalar inverse-approximation corollary, obtained by factoring $1-r_q=Xp$. The `WithBot` degree includes $q=0$:
the zero polynomial has degree $\bot<0$, and error at most $1/a\le2/a$.
:::
