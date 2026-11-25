---
kind: statement
id: nlalib-isbasisextensionerr-fb78aa8d
uid: fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393
---

::: definition decl:NLAlib.IsBasisExtensionErr name="Rounded extension of a basis by a block"
For a matrix $\mathbf{Q}$, let $\mathbf{D}(\mathbf{Q})=\mathbf{Q}^{\mathsf{T}}\mathbf{Q}-\operatorname{diag}(\mathbf{s})$ be its Gram defect on the support, where $s_j=0$ at a zero column and $s_j=1$ otherwise. A rounded extension of $\mathbf{Q}$ by a block $\mathbf{W}$ of $\ell$ columns, with parameters $(\eta_0,\mu,\varepsilon)$, consists of $\mathbf{Q}'$, $\mathbf{H}$, and an upper triangular $\mathbf{R}$ such that a zero column of $\mathbf{W}$ gives a zero column of $\mathbf{Q}'$ and, whenever $\mathbf{Q}$ lies in the window

$$\sqrt{\|\mathbf{D}(\mathbf{Q})\|_{\mathrm{F}}^2+3\ell\mu^2}\le\eta_0,$$

1. $\|\mathbf{W}-\mathbf{Q}\mathbf{H}-\mathbf{Q}'\mathbf{R}\|_{\mathrm F}\le\varepsilon\|\mathbf{W}\|_{\mathrm F}$;
2. every column $\mathbf{q}'_c$ of $\mathbf{Q}'$ is zero, or satisfies $\bigl|\|\mathbf{q}'_c\|^2-1\bigr|\le\mu$ and $\|\mathbf{Q}^{\mathsf{T}}\mathbf{q}'_c\|^2+\sum_{c'<c}(\mathbf{q}'_{c'}\cdot\mathbf{q}'_c)^2\le\mu^2$.

The bound on a kept column is absolute, so the scheme owns the decision to drop a column.
:::
