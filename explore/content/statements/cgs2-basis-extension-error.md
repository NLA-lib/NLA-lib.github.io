---
kind: statement
id: cgs2-basis-extension-error
uid: 3f4f0fa3-7a5c-5871-83e4-2b9fceb23147
---

::: theorem result:cgs2-basis-extension-error name="Column guarantees give the rounded contract"
Let $\mathbf{Q}$ be a real basis, $\mathbf{W}$ the block, $\mathbf{W}'$ the reduced block, $\mathbf{Q}'$ the new block, and $\mathbf{H}$, $\mathbf{R}$ the coefficients, with $\mathbf{R}$ upper triangular. For every column $c$ assume:

1. the step from $\mathbf{w}_c$ to $\mathbf{w}'_c$, with coefficients $(\mathbf{H}_c,\mathbf{R}_{<c,c})$, meets the single-vector guarantee on the support with parameters $(\eta_0,\varepsilon_1,\varepsilon_2,\varepsilon_3)$ for the basis $\mathbf{V}_c=[\mathbf{Q},\mathbf{Q}'_{<c}]$: whenever the Gram defect on the support of $\mathbf{V}_c$ has spectral norm at most $\eta_0$, $\|\mathbf{w}_c-\mathbf{V}_c\mathbf{h}-\mathbf{w}'_c\|\le\varepsilon_2\|\mathbf{w}_c\|$ and $\|\mathbf{V}_c^{\mathsf{T}}\mathbf{w}'_c\|\le\varepsilon_1\|\mathbf{w}'_c\|+\varepsilon_3\|\mathbf{w}_c\|$;
2. a zero $\mathbf{w}_c$ gives a zero $\mathbf{w}'_c$;
3. the computed norms satisfy $|\nu_c-\|\mathbf{w}_c\||\le E\|\mathbf{w}_c\|$ and $|\beta_c-\|\mathbf{w}'_c\||\le E\|\mathbf{w}'_c\|$;
4. either the column is dropped, with $\beta_c\le\tfrac32\tau\nu_c$, $\mathbf{q}'_c=\mathbf 0$, and $r_{cc}=0$; or it is kept, with $\tfrac12\tau\nu_c<\beta_c$, $r_{cc}=\beta_c$, and $\|\beta_c\mathbf{q}'_c-\mathbf{w}'_c\|\le E\|\mathbf{w}'_c\|$.

If $\eta_0\le1/100$, $0\le\varepsilon_1,\varepsilon_2,\varepsilon_3\le1/10$, $0\le E\le1/100$, and $\tau>0$, then $(\mathbf{Q}',\mathbf{H},\mathbf{R})$ is a rounded extension of $\mathbf{Q}$ by $\mathbf{W}$ with window $\eta_0$ and parameters

$$\mu=2\varepsilon_1+\frac{4\varepsilon_3}{\tau}+5E,\qquad\varepsilon=\varepsilon_2+2E+2\tau.$$

The two thresholds in the fourth assumption allow for rounding in the deflation test.
:::
