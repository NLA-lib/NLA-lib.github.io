---
kind: statement
id: entry-dbd5fda4-ab5b-5d5f-87e1-de0a920f424e
uid: dbd5fda4-ab5b-5d5f-87e1-de0a920f424e
---
::: theorem result:jacobi-complementary-minors name="Jacobi's complementary minor formula"
Let the bijections $e_r, e_c : p \oplus q \simeq n$
split the index type of an invertible $\mathbf{A}$ into a selected part $p$ and its complement
$q$, for rows and for columns. The minor of $\mathbf{A}^{-1}$ on rows $e_c(q)$ and columns
$e_r(q)$ is the minor of $\mathbf{A}$ on rows $e_r(p)$ and columns $e_c(p)$, times the sign of the
permutation $e_r^{-1} \circ e_c$ (`ec.trans er.symm`), divided by $\det \mathbf{A}$.
Horn and Johnson state the formula for increasing index sets with sign $(-1)^s$, where $s$ is
the sum of the selected indices; this version applies to any finite index types over any field.
:::
