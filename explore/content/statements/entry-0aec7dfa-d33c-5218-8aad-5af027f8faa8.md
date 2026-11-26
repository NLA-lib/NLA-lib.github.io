---
kind: statement
id: entry-0aec7dfa-d33c-5218-8aad-5af027f8faa8
uid: 0aec7dfa-d33c-5218-8aad-5af027f8faa8
---
::: theorem result:minres-chebyshev-bound name="The Chebyshev bound for MINRES"
For $\kappa = a'/a$, if Hermitian $\mathbf{A}$ has spectrum in $[a, a']$ and $0 < a$,
$$\|\mathbf{b} - \mathbf{A}\,\mathsf{gmresIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, q)\| \le
2\Bigl(\frac{\sqrt{a'/a} - 1}{\sqrt{a'/a} + 1}\Bigr)^q\|\mathbf{r}_0\| \,.$$
:::
