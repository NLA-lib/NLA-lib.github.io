---
kind: statement
id: nlalib-cgs2-cgs2extendroutine-af080b3b
uid: af080b3b-42f5-5b70-adba-76b80f20b48b
---

::: definition decl:NLAlib.CGS2.cgs2ExtendRoutine name="Column-wise two-pass classical Gram–Schmidt with threshold deflation" id=algorithm
The dimensions are $[n,k,\ell]$; the inputs are the stored basis $\mathbf{Q}$ and the block $\mathbf{W}$; the outputs are the new block $\mathbf{Q}'$, the reduced block (overwriting $\mathbf{W}$), and the coefficient block $\mathbf{C}$ with $k+\ell$ rows. The threshold $\tau$ is a rational literal of the implementation. The new block is stored directly after the basis, so the basis and the new columns already written form one contiguous block.

For each column $c=0,\ldots,\ell-1$:

1. Save $\nu=\|\mathbf{w}_c\|$.
2. Set rows $k,\ldots,k+\ell-1$ of column $c$ of $\mathbf{C}$ to zero.
3. First pass: compute the coefficients of $\mathbf{w}_c$ against the $k+c$ stored columns, write them to rows $0,\ldots,k+c-1$ of column $c$ of $\mathbf{C}$, and reduce $\mathbf{w}_c$ in place.
4. Second pass: compute coefficients against the same columns into scratch and reduce $\mathbf{w}_c$ in place again.
5. Add the second coefficients to the first.
6. Compute $\beta=\|\mathbf{w}_c\|$ for the reduced column.
7. If $\beta\le\tau\nu$, store a zero column $\mathbf{q}'_c$ and leave the diagonal coefficient zero.
8. Otherwise store $\mathbf{q}'_c=\mathbf{w}_c/\beta$ and the diagonal coefficient $C_{k+c,c}=\beta$.

At $\tau=0$ the test is the exact zero guard. A dropped column remains a zero column of the basis. The scratch is $k+\ell$ coefficient cells and three scalar cells.
:::
