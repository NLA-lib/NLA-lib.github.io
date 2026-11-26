---
kind: statement
id: lanczos-fa-uniform-bound
uid: ba9a80b1-12cc-5be5-b98c-0834104cd8f5
---

::: theorem result:lanczos-fa-uniform-bound name="Polynomial approximation controls the error"
Let $\mathbf{A}$ be Hermitian with spectrum in $[a,b]$, and let $f$ be continuous on that interval. With $q+1$ mathematical [Lanczos steps](/explore/statements/d9e8ae48-2c48-5c42-9da5-0bd6cdd8f239/),

$$\|f(\mathbf{A})\mathbf{b}-\mathsf{lanczosfa}(\mathbf{A},f,\mathbf{b},q+1)\|_2\le2E_q(f;[a,b])\|\mathbf{b}\|_2,$$

where $E_q$ is the best uniform approximation error among polynomials of degree at most $q$. A good low-degree approximation to $f$ therefore gives an accurate matrix-function action.
:::
