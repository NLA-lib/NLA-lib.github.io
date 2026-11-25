---
kind: statement
id: nlalib-isbasisextension-12a7ec72
uid: 12a7ec72-6c64-59e6-b7de-7aff8d055ba2
---

::: definition decl:NLAlib.IsBasisExtension name="Exact extension of a basis by a block"
Let $\mathbf{Q}$ be a stored basis with $n$ rows and $\mathbf{W}$ a block of $\ell$ columns. A new block $\mathbf{Q}'$ with coefficients $\mathbf{H}$ and $\mathbf{R}$ is an exact extension of $\mathbf{Q}$ by $\mathbf{W}$ when

1. $\mathbf{W}=\mathbf{Q}\mathbf{H}+\mathbf{Q}'\mathbf{R}$ with $\mathbf{R}$ upper triangular;
2. the columns of $\mathbf{Q}'$ are combinations of the columns of $\mathbf{Q}$ and $\mathbf{W}$;
3. a zero column of $\mathbf{W}$ gives a zero column of $\mathbf{Q}'$;
4. the rows of $\mathbf{H}$ and $\mathbf{R}$ at zero columns of $\mathbf{Q}$ and $\mathbf{Q}'$ are zero;
5. if the nonzero columns of $\mathbf{Q}$ are orthonormal, so are the nonzero columns of $[\mathbf{Q},\mathbf{Q}']$.

This is a relation, not a function: the scheme decides which columns of $\mathbf{Q}'$ are zero, so dependent columns may be dropped. No condition is imposed on $\mathbf{Q}$ itself.
:::
